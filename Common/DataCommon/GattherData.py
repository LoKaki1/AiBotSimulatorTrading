import pandas as pd
from yahoofinancials import YahooFinancials
from Common.Logger import Logger
from Common.Common import is_float_number

""" My Constants """
X_VALUES = ['open', 'low', 'high', 'close']


def get_historical_data(ticker, start, end):
    try:
        return get_data_from_yahoo(ticker, start, end)
    except OSError as e:
        Logger.error(f'In networking while truinh to get data - {e}')
        raise OSError("Problem in getting data please try to reconnect")


def get_data_from_yahoo(ticker, start, end):
    return (pd.DataFrame(
        YahooFinancials(ticker).get_historical_price_data(
            start_date=start,
            end_date=end,
            time_interval='daily')[
            ticker]['prices']).drop('date', axis=1)
            .set_index('formatted_date'))


def one_array_data(data):
    first = list(data.keys())[0]
    return [
        data[state][index] for index, stock_price in enumerate(data[first]) for state in data
    ]
