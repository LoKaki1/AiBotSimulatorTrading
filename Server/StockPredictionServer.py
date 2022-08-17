import json

from flask import Flask, request
from flask_cors import CORS
from Logger import Logger

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.before_request
def check_authentication():
    Logger.info(f"checking authentication.. {request.headers.get('username')}")


@app.route('/predict', methods=['GET'])
def get_predict_data():
    Logger.info(f"predicting data for - {request.args}")
    return json.dumps({
        "data": f"Predicted data for ticker - {request.args.get('ticker')}"
    })


@app.route('/watchlist', methods=['GET'])
def get_user_watchlist():
    username = request.headers.get('username', 'default Shlomi')
    Logger.info(f"Getting watchlist for user {username}")
    return json.dumps({
        "data": f"Getting user watchlist {username}"
    })


@app.route('/stock/chart/daily', methods=['GET'])
def get_stock_daily_chart():
    stock = request.headers.get('stock', 'NIO')
    Logger.info(f"Getting daily chart for stock {stock}")
    return json.dumps({
        "data": f"daily prices for stock - {stock}"
    })


@app.route('/stock/chart/interday', methods=['GET'])
def get_stock_interday_chart():
    stock = request.headers.get('stock', 'NIO')
    Logger.info(f"Getting interday chart for stock {stock}")
    return json.dumps({
        "data": f"interday prices for stock - {stock}"
    })


@app.route('/stock/current_price', methods=['GET'])
def get_stock_current_price():
    stock = request.headers.get('stock', 'NIO')
    Logger.info(f"current price for stock  {stock}")
    return json.dumps({
        "data": f"current price for stock  - {stock}"
    })


if __name__ == '__main__':
    app.run()
