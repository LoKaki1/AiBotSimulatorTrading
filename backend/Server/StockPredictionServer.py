import json
from Common.DataCommon.ModelDataHandler import daily_candle_prices, get_interday_data
from PredictingData import PredictingDataForServer
from PredictingData.StockPredictionAi import END
from PredictingData.Factory import TickerObjectFactory
from PredictingData.Factory.PredictionFactory import predict_data_for_stock
from flask import Flask, request, Response
from flask_cors import CORS
from Logger import Logger
from PredictingData.PredictingDataForServer import update_watchlist
from ServerKeysConstants import DEFAULT_STOCK, TICKER, DEFAULT_USER, AUTHENTICATION, START_DAY, \
    DEFAULT_START_DAY, INTERVAL, DEFAULT_INTERVAL, RANGE, DEFAULT_RANGE

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.before_request
def check_authentication():
    Logger.info(f"checking authentication.. {request.headers.get(AUTHENTICATION, DEFAULT_USER)}")


@app.after_request
def parse_data(response: Response):
    result = Response(
        json.dumps(response.get_json())
    )
    return result


@app.route('/predict', methods=['GET'])
def get_predict_data():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"predicting data for - {ticker}")
    predicted_price = predict_data_for_stock(ticker)
    return {"price": predicted_price}


@app.route('/watchlist', methods=['GET'])
def get_user_watchlist():
    username = request.headers.get(AUTHENTICATION, DEFAULT_USER)
    Logger.info(f"Getting watchlist for user {username}")
    user_watchlist = PredictingDataForServer.predicting_user_watchlist(username)
    return {'watchlist': user_watchlist}


@app.route('/stock/chart/daily', methods=['GET'])
def get_stock_daily_chart():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    start_day = request.args.get(START_DAY, DEFAULT_START_DAY)
    Logger.info(f"Getting daily chart for stock {ticker}")
    daily_data = daily_candle_prices(ticker, start_day, END)
    return {"dailyData": daily_data}


@app.route('/stock/chart/interday', methods=['GET'])
def get_stock_interday_chart():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    interval = request.args.get(INTERVAL, DEFAULT_INTERVAL)
    _range = request.args.get(RANGE, DEFAULT_RANGE)
    print(f"ticker = {ticker}", f"{interval=}", f"{_range}", sep='\n')
    Logger.info(f"Getting interday chart for stock {ticker}")
    interday_data = get_interday_data(ticker, interval, _range)
    return {"interdayData": interday_data}


@app.route('/stock/current_price', methods=['GET'])
def get_stock_current_price():
    stock = request.args.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"current price for stock  {stock}")
    return {"currentPrice": 6}


@app.route('/prediction/ticker_object')
def get_stock_object():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    username = request.headers.get(AUTHENTICATION, DEFAULT_USER)
    ticker_object = TickerObjectFactory.create_ticker_object(ticker)
    update_watchlist(username, ticker_object)
    return ticker_object


if __name__ == '__main__':
    app.run()
