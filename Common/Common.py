import binascii
import json
import os

import datetime as dt
from typing import Union,  Any

import matplotlib.pyplot as plt
import ast
import pandas as pd
from functools import wraps
from yahoofinancials import YahooFinancials
from tensorflow.keras.models import load_model
from Trading.data_order_something import read_data, read_from_file
import yfinance as yf
import re
from flask import request

import time

X_VALUES = [['open', 'low', 'high', 'close'], ['Open', 'Low', 'High', 'Close']]
DATA_BASE_KEYS = ['watchlist', 'scanner', 'settings', 'active_watchlist', 'dates']

DATABASE_PATH = '../api/Databases/user_database.json'
TOKENS = '../api/Databases/tokens.json'

START = dt.datetime(2021, 4, 27).strftime('%Y-%m-%d')
END = dt.datetime.now().strftime('%Y-%m-%d')

DEFAULT_DICT = {'start': START, 'period': '1d', 'interval': '1m'}

ALLOWED_INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
ALLOWED_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']


def write_in_file(path, data):
    with open(path, 'a') as file:
        file.write(data)


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


def read_csv(path, ticker=None, other='3'):
    return pd.read_csv(path) if os.path.exists(path) else pd.read_csv(read_data(ticker, other=other))


def iterate_data(data, what=0):
    return [[float(p)
             for key in X_VALUES[what] if re.match('^[0-9/.]*$', str(p := data[key][index])) is not None]
            for index, i in enumerate(data['close'] if 'close' in data.keys() else data['Close'])]


def try_except(catch_except, func, *args):
    try:
        func(args[-1])
        return True
    except catch_except:
        return False


def load_model_from_file(classifiler_ai_stock_model):
    """
    Function to load model from saved model file
    """

    return load_model(
        path) if os.path.exists(
        (path := f'saved_model/'
                 f'{classifiler_ai_stock_model.ticker}_model/'
                 f'{classifiler_ai_stock_model.epochs}-'
                 f'{classifiler_ai_stock_model.units}-'
                 f'{classifiler_ai_stock_model.prediction_days}-'
                 f'{classifiler_ai_stock_model.prediction_day}')) else None


def get_historical_data(ticker, start, end):
    try:
        return (pd.DataFrame(
            YahooFinancials(ticker).get_historical_price_data(
                start_date=start,
                end_date=end,
                time_interval='daily')[
                ticker]['prices']).drop('date', axis=1)
                .set_index('formatted_date'))
    except OSError as e:
        print(f"can't connect to yahoo finanace api error - {e}")
        time.sleep(4)
        try:
            return (pd.DataFrame(
                YahooFinancials(ticker).get_historical_price_data(
                    start_date=start,
                    end_date=end,
                    time_interval='daily')[
                    ticker]['prices']).drop('date', axis=1)
                    .set_index('formatted_date'))
        except OSError:
            raise InterruptedError("Just no bro..")


def best_settings() -> (dict, float):
    father = open_json(r'../predicting_stocks/settings_for_ai/parameters_status.json')
    father = father[(last_ratio := f"{max([float(ratio) for index, ratio in enumerate(father)])}")]
    return father, last_ratio


def plot(data, pre_prices, ticker):
    plt.plot(data, color='blue')
    plt.plot(pre_prices, color='red')
    plt.title(f'{ticker} Share Price')
    plt.xlabel('Time')
    plt.ylabel(f'{ticker} Share Price')
    plt.legend()
    plt.show()


def write_in_json_file(path, data: dict, ticker=None):
    with open(path, 'r') as read_file:
        data = json.dumps(data)
        json_object = json.load(read_file)
        json_object[ticker] = ast.literal_eval(data)[ticker]
        with open(path, 'w') as write_file:
            json.dump(json_object, write_file,
                      indent=4,
                      separators=(',', ': ')
                      )


def return_json_data(ticker, json_path='../predicting_stocks/settings_for_ai/parameters_status.json'):
    # try:
    #     with open(json_path, 'r'):
    #         print(json_path)
    # except FileNotFoundError:
    #     print('did not find file', json_path, sep=', ')
    #     return [None for _ in range(4)]
    return [setting for setting in file[ticker]['settings'].values()]\
        if os.path.exists(json_path) and ticker in (file := open_json(json_path)) else [None for _ in range(4)]
    #
    # if not json_path:
    #     return None
    # with open(json_path, 'r') as json_file:
    #     p = json.load(json_file)
    #     if ticker in p:
    #         p = p[ticker]['settings']
    #         return [p['epochs'], p['units'], p['prediction_days'], p['prediction_day']]
    #     else:
    #         return [None for _ in range(4)]


def check_data(x_train, y_train, constant=1):
    for i in range(0, len(x_train) - constant):
        assert y_train[i] == x_train[i + constant][-1], "not good data"


def get_data_from_saved_file(ticker, ):
    """

    :param ticker: Ticker to get historical data from its file
    :return: dictionary of historical data of a stock that has been saved earlier using save_historical_data()

    Format - ticker name.txt in Data directory, otherwise it will not find the data
    """
    with open(f'./Data/{ticker}.txt', 'r') as file:
        data = file.read()
        return ast.literal_eval(data)


def get_data_from_file_or_yahoo(ticker):
    return iterate_data(ast.literal_eval(data), what=1) if (data := read_from_file(ticker)) is not None else \
        intraday_with_yahoo(ticker)


def no_iteration_interday_with_yahoo(ticker, other: Union[str, int] = '1d', interval='1m'):
    assert interval in ALLOWED_INTERVALS and other in ALLOWED_PERIODS,\
        f"{other} or {interval} are not allowed to use as period or interval"
    data = yf.download(tickers=ticker, period=str(other), interval=interval)
    dates = list(data['Open'].keys())
    return {date.strftime('%Y-%m-%d %H:%M'): [data[key][index]
                                              for key in X_VALUES[1]] for index, date in enumerate(dates)}


def intraday_with_yahoo(ticker, other: Union[str, int] = '2', interval='1m'):
    data = yf.download(tickers=ticker, period=f'{str(other)}d', interval=interval)
    with open(f'../Trading/Historical_data/{ticker}.txt', 'w') as file:
        data_dict = dict((key, [i for i in data[key]]) for key in ['Open', 'Close', 'Low', 'High'])
        file.write(str(data_dict))
    return iterate_data(data_dict, what=1)


def handle_with_time(ticker, json_object, ):
    today_str = dt.datetime.now().strftime('%Y-%m-%d')
    today = dt.datetime.strptime(today_str, '%Y-%m-%d')
    if ticker not in json_object:
        return today_str
    ticker_date = dt.datetime.strptime(json_object[ticker]['date'], '%Y-%m-%d')
    print(ticker_date, today)
    return today_str if today > ticker_date else float(json_object[ticker]['price'])


def _get_id_list(json_object):
    return [json_object[ticker]['id'] for ticker in json_object]


def get_last_id(json_object):
    id_list = _get_id_list(json_object)
    return id_list[-1] + 1 if len(id_list) else 1


def save_in_data_base(ticker, price, settings, date, _id):
    data = {
        ticker: {
            "id": _id,
            "price": price,
            "settings": settings,
            "date": date,
            "current_price": (t := str(get_last_price(ticker)))[0:6 if len(t) >= 6 else -1]
        }
    }
    write_in_json_file('../api/Databases/database.json', data, ticker)


def get_last_price(ticker):
    return get_historical_data(ticker, (dt.datetime.now() - dt.timedelta(days=5)).strftime('%Y-%m-%d'),
                               dt.datetime.now().strftime('%Y-%m-%d'), )['close'][-1]


def open_json(path: str) -> dict:
    with open(path, 'r') as file:
        json_data = json.loads(file.read())
    return json_data


def write_in_json(path: str, data: [dict, list]):
    with open(path) as fp:
        json_object = json.load(fp)

    json_object.update(data)

    write_json(path, json_object)


def generate_dates_between_dates(start, end):
    return pd.date_range(start, end, freq='d')


def generates_dates_times_between_to_dates(start, end):
    return [start + dt.timedelta(minutes=i) for i in range(int((end - start).seconds + 1) // 60)]


def generate_tokens(user):
    write_in_json(TOKENS, {user: (token := generate_uniq_id())})
    return token

def generate_uniq_id():
    return binascii.hexlify(os.urandom(20)).decode()


def token_checking(api_func):
    @wraps(api_func)
    def wrapper(*args, **kwargs):
        print(f'{request.get_json()}')
        database = open_json('../api/Databases/tokens.json')
        print(request.get_json().get('token', None))
        if request.get_json().get('token', None) not in list(database.values()):
            return json.dumps({'data': 'lost connection try to login again'})
        return json.dumps(api_func(*args, **kwargs))

    return wrapper


def get_from_interactive(**kwargs):
    kwargs['app'].disconnect()
    try:

        return open_json(kwargs['path'])[kwargs['ticker']][
            kwargs['key']] if 'ticker' and 'key' in kwargs else open_json(kwargs['path'])
    except [KeyError, FileNotFoundError] as e:
        print(e)
        return -1


def list_in_list(lst1, lst2) -> bool:
    return all(var in lst2 for var in lst1)


def token_authentication(client_headers, client_request, client_args):
    token = client_headers.get('token', False)
    user = client_headers.get('user', False)
    if not token or not user:
        return 'You are asking for element which requires authentication', \
               'No authentication, not allowed, 405', False
    user_tokens = open_json('Databases/tokens.json')
    if user not in user_tokens or token != user_tokens[user]:
        return 'You are asking for element which requires authentication', \
               'No authentication, not allowed, 405', False
    return {'request': client_request, 'args': client_args, 'headers': client_headers}, '200 ok', True


def write_json(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file,
                  indent=4,
                  separators=(',', ': '))


def add_to_database(client: str, data: Union[list, dict, bytes, str], key: str) -> Union[list, dict, bytes, str]:
    assert key in DATA_BASE_KEYS, f"The keys in {key} not in allowed keys"
    all_data = open_json(DATABASE_PATH)
    if client not in all_data:
        all_data[client] = {key: {} for key in DATA_BASE_KEYS}

    all_data[client][key].update(data)
    write_in_json(DATABASE_PATH, all_data)
    return all_data


def histrical_data_json_format(ticker, start, end=END):

    data = get_historical_data(ticker, start, end)
    data = iterate_data(data)
    dates = generate_dates_between_dates(start, end)
    return [{'x': date.strftime(
        '%Y-%m-%d'), 'y': [
        float(str(
            price)[0: 5])
        for price in prices]}
        for date, prices in zip(dates, data) if data[-1] != prices]


def interday_data_json_format(ticker, period, interval):
    data = no_iteration_interday_with_yahoo(ticker, period, interval)
    return [
        {
            'x': key,
            'y': [float(str(value)[0: 5]) for value in values]
        }
        for key, values in data.items()
    ]


def get_user_start_day(user, key):
    return data[user]['dates'].get(key, DEFAULT_DICT[key]) if user in (data := open_json(DATABASE_PATH)) else DEFAULT_DICT[key]


def found_in_list_of_dict(iterate: Union[list[dict], dict[dict]], key: str, value: str) -> (bool, Any):
    print(iterate)
    if not iterate:
        return False, None
    for target in iterate:
        if target[key] == value:
            return True, target
    return False, None


def remove_key_from_json(path: str, key):
    data = open_json(path)
    data.pop(key)
    write_json(path, data)
