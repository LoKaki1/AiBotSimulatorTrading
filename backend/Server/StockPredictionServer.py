import json

from flask_socketio import SocketIO

from Common.DataCommon.ModelDataHandler import daily_candle_prices, get_interday_data, get_last_price
from flask import Flask, request, Response
from flask_cors import CORS
from Common.Logger import Logger
from ServerKeysConstants import DEFAULT_STOCK, TICKER, DEFAULT_USER, AUTHENTICATION, START_DAY, \
    DEFAULT_START_DAY, INTERVAL, DEFAULT_INTERVAL, RANGE, DEFAULT_RANGE
from Bootstrap.Bootstrapper import bootstrapper

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'
socketio = SocketIO(app, cors_allowed_origins="*")
prediction_watchlist_manager = bootstrapper()


@app.before_request
def check_authentication():
    Logger.info(f"checking authentication.. {request.headers.get(AUTHENTICATION, DEFAULT_USER)}")


@app.after_request
def parse_data(response: Response):
    result = Response(
        json.dumps(response.get_json())
    )
    return result


@app.route('/watchlist', methods=['GET'])
def get_user_watchlist():
    username = request.headers.get(AUTHENTICATION, DEFAULT_USER)
    Logger.info(f"Getting watchlist for user {username}")
    user_watchlist = prediction_watchlist_manager.get_predicted_watchlist(username)
    return {'watchlist': user_watchlist}


@app.route('/prediction/ticker_object')
def get_stock_object():
    ticker = request.args.get(TICKER, DEFAULT_STOCK)
    username = request.headers.get(AUTHENTICATION, DEFAULT_USER)
    ticker_object = prediction_watchlist_manager.predict_ticker(username, ticker)
    return ticker_object


if __name__ == '__main__':
    app.run()