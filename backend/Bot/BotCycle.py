from Bot import Logic, IntegrationApi
from Bot.Prediction import Prediction
from Bot.Watchlist import Watchlist

WATCHLIST = ['NIO', 'XPEV', 'TSLA', 'LI',  'BIG', 'RIVN', 'LCID', 'BABA']
QUANTITY = 100


def main():
    watchlist = Watchlist(WATCHLIST)
    logic = Logic.very_simple_logic
    while True:
        prediction_watchlist = Prediction(watchlist.never_opened)
        predicted_prices_result = prediction_watchlist.predict_prices()
        predict_logic_result = Logic.logic_on_prediction_result(predicted_prices_result, logic)
        IntegrationApi.tranaction_to_logic(predict_logic_result, QUANTITY)
        opened_trades: list = IntegrationApi.get_open_postions()
        watchlist.open_trade(opened_trades)


if __name__ == '__main__':
    main()
