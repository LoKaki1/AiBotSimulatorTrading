from random import random, randint

import requests
import numpy as np
import pandas as pd
from yahoofinancials import YahooFinancials

from Common.DataCommon.YahooConstants import YAHOO_INTERDAY_API, USER_AGENT, USER_AGENT_VALUE
from Common.DateCommon import generate_dates_between_two_dates
from Common.Logger import Logger

""" My Constants """
X_VALUES = ['open', 'low', 'high', 'close']
FAIL_TO_PREPARE_DATA_MESSAGE = "data found was not expected in index {i}"


def get_historical_data(ticker, start, end):
    try:
        return get_data_from_yahoo(ticker, start, end)
    except OSError as e:
        Logger.error(f'In networking while truinh to get data - {e}')
        raise OSError("Problem in getting data please try to reconnect")


def get_interday_data(ticker, interval, _range):
    data = requests.get(YAHOO_INTERDAY_API.format(ticker=ticker, interval=interval, _range=_range),
                        headers={USER_AGENT: USER_AGENT_VALUE})
    data = data.json()['chart']['result'][0]['indicators']['quote'][0]
    current_candle = {"y": ['0'], "x": 0}
    data = [(current_candle := {"y": [handle_none(data[key][index], current_candle["y"][0])
                                      for key in X_VALUES], "x": index}) for index, _ in enumerate(data['close'])]
    return data


def get_last_price(ticker):
    try:
        data = requests.get(YAHOO_INTERDAY_API.format(ticker=ticker, interval='1m', _range='1d'),
                            headers={USER_AGENT: USER_AGENT_VALUE})
        return format_price(data.json()['chart']['result'][0]['indicators']['quote'][0]['close'][-1])
    except [OSError, TypeError]:
        Logger.error("Can't access to internet, data is not right")
        return randint(0, 300)


def handle_none(price, price_before):
    return format_price(price) if price is not None else format_price(price_before)


def format_price(price) -> float:
    return float(str(price)[:5])


def candle_data_from_raw_data(data: pd.DataFrame, start_date, end_date):
    dates = generate_dates_between_two_dates(start_date, end_date)
    return [
        {"y": [float(str(data[candle_part][index])[:5])
               for candle_part in X_VALUES], "x": dates[index]}
        for index, _ in enumerate(data[X_VALUES[0]])
    ]


def daily_candle_prices(ticker, start_date, end_date):
    historical_data = get_historical_data(ticker, start_date, end_date)
    return candle_data_from_raw_data(historical_data, start_date, end_date)


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
        data[state][index] for index, stock_price in enumerate(data[first]) for state in X_VALUES
    ]


def check_prepared_data_for_model(x_train, y_train, predict_constant=1):
    for i in range(0, len(x_train) - predict_constant):
        assertion = y_train[i] == x_train[i + predict_constant][-1]
        "Hope som much it works that way "
        assert assertion, FAIL_TO_PREPARE_DATA_MESSAGE.format(i=i)


def reshape_trains(x_train, y_train):
    x_train, y_train = np.array(x_train), np.array(y_train).reshape(-1, 1)
    """  x_train.shape[0] = the length of the array, x_train.shape[1] =  prediction days 
     means to create a shape with length of x_train.len and width of prediction days on one dimension
    """
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    return x_train, y_train
