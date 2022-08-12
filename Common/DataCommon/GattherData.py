import pandas as pd
from yahoofinancials import YahooFinancials
from time import sleep


def get_historical_data(ticker, start, end):
    try:
        return get_data_from_yahoo(ticker, start, end)
    except OSError as e:
        print(f"can't connect to yahoo finanace api error - {e}")
        sleep(4)
        try:
            return get_data_from_yahoo(ticker, start, end)
        except OSError:
            raise InterruptedError("Just no bro.. after reconnecting 2 times I cannot get data")


def get_data_from_yahoo(ticker, start, end):
    return (pd.DataFrame(
        YahooFinancials(ticker).get_historical_price_data(
            start_date=start,
            end_date=end,
            time_interval='daily')[
            ticker]['prices']).drop('date', axis=1)
            .set_index('formatted_date'))
