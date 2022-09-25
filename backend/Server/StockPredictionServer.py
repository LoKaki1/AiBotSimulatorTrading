import json

from PredictingData import PredictingDataForServer
from PredictingData.Factory import TickerObjectFactory
from PredictingData.Factory.PredictionFactory import predict_data_for_stock
from flask import Flask, request, Response
from flask_cors import CORS
from Logger import Logger
from PredictingData.PredictingDataForServer import update_watchlist
from ServerKeysConstants import USERNAME, DEFAULT_STOCK, TICKER, DEFAULT_USER

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.before_request
def check_authentication():
    Logger.info(f"checking authentication.. {request.headers.get(USERNAME, DEFAULT_USER)}")


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
    username = request.headers.get(USERNAME, DEFAULT_USER)
    Logger.info(f"Getting watchlist for user {username}")
    user_watchlist = PredictingDataForServer.predicting_user_watchlist(username)
    return {'watchlist': user_watchlist}


@app.route('/stock/chart/daily', methods=['GET'])
def get_stock_daily_chart():
    stock = request.args.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"Getting daily chart for stock {stock}")
    return f"daily prices for stock - {stock}"


@app.route('/stock/chart/interday', methods=['GET'])
def get_stock_interday_chart():
    stock = request.args.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"Getting interday chart for stock {stock}")
    return f"interday prices for stock - {stock}"


@app.route('/stock/current_price', methods=['GET'])
def get_stock_current_price():
    stock = request.args.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"current price for stock  {stock}")
    return {"currentPrice": 6}


@app.route('/prediction/ticker_object')
def get_stock_object():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    username = request.headers.get(USERNAME, DEFAULT_USER)
    ticker_object = TickerObjectFactory.create_ticker_object(ticker)
    update_watchlist(username, ticker_object)
    return ticker_object



if __name__ == '__main__':
    app.run()
