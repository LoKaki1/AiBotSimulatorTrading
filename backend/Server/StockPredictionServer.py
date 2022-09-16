import json
from typing import Union

from PredictingData.Factory.PredictionFactory import predict_data_for_stock
from flask import Flask, request, Response
from flask_cors import CORS
from Logger import Logger
from ServerKeysConstants import USERNAME, DEFAULT_STOCK, JSON_DATA, TICKER, DEFAULT_USER

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.before_request
def check_authentication():
    Logger.info(f"checking authentication.. {request.headers.get(USERNAME, DEFAULT_USER)}")


@app.after_request
def parse_data(response: Response):
    result = Response(json.dumps({
        JSON_DATA: response.data.decode()
    }))
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
    return f"Getting user watchlist {username}"


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
    stock = request.headers.get(TICKER, DEFAULT_STOCK)
    Logger.info(f"current price for stock  {stock}")
    return f"current price for stock  - {stock}"



if __name__ == '__main__':
    app.run()
