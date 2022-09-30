import json
from typing import Union, Any

import numpy as np
import pandas as pd
from yahoofinancials import YahooFinancials
from Logger import Logger

""" My Constants """
X_VALUES = ['open', 'low', 'high', 'close']
FAIL_TO_PREPARE_DATA_MESSAGE = "data found was not expected in index {i}"


def get_historical_data(ticker, start, end):
    try:
        return get_data_from_yahoo(ticker, start, end)
    except OSError as e:
        Logger.error(f'In networking while truinh to get data - {e}')
        raise OSError("Problem in getting data please try to reconnect")


def candle_data_from_raw_data(data: pd.DataFrame):
    return [
        [data[candle_part][index] for candle_part in X_VALUES] for _, index in enumerate(data[X_VALUES[0]])
    ]


def daily_candle_prices(ticker, start_price, end_price):
    raw_data = get_historical_data(ticker, start_price, end_price)
    return candle_data_from_raw_data(raw_data)


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


def open_json(json_path: str):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)


def write_in_json(path: str, data: [dict, list]):
    json_object = open_json(path)
    json_object.update(data)
    write_json(path, json_object)


def update_json_where(path: str, relevant_key: str, value: Any, data: Union[dict, list, bytes]):
    file_data = open_json(path)
    result_data = list(
        map(
            lambda x: data if x[relevant_key] == value else x, file_data
        )
    )
    write_json(path, result_data)


def write_json(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file,
                  indent=4,
                  separators=(',', ': '))
