from typing import Union, Dict, List

from InvestopediaApi import ita

QUANTITY = 100

with open('./SecretData/InvestopediaUser.txt', 'r') as file:
    username, password = (result := file.read().split('\n'))[0], result[1]
    print(username)
    print(password)
client = ita.Account(username, password)

api_transcations_name = {
    'buy': ita.Action.buy,
    'sell': ita.Action.sell,
    'short': ita.Action.short,
    'cover': ita.Action.cover,
}

close_transactions = {
    'buy': 'sell',
    'short': 'cover'
}


def create_transaction(ticker_prediction_logic_result: Dict[str: Union[str, float]], quantity):
    ticker = ticker_prediction_logic_result['ticker']
    transaction_type = close_transactions[ticker_prediction_logic_result['type']]
    close_price = ticker_prediction_logic_result['close']
    stop_price = ticker_prediction_logic_result['stoploss']
    client.trade(ticker, transaction_type, quantity)
    client.trade(ticker, transaction_type, quantity, priceType='Limit', price=close_price)
    client.trade(ticker, transaction_type, quantity, priceType='Stop', price=stop_price)

# Todo create a function that iterates on logic results and call to create transaction
# Todo create a function that get open close that can be returned to watchlist class


def tranaction_to_logic(prediction_logic_reslt: List[Dict[str: Union[str, float]]], quantity=QUANTITY):
    for ticker_preiction_logic_result in prediction_logic_reslt:
        create_transaction(ticker_preiction_logic_result, quantity)


def get_open_postions():
    return client.get_open_trades()
