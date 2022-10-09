import json

from Common.ServerCommon.DataListeners import DataListener


class LiveDataUsers:

    def __init__(self):
        self.listener = DataListener(on_ticker=self.on_ticker)
        self.clients_tickers_sockets = {}

    def add_ticker(self, ws, ticker):
        if ticker not in self.clients_tickers_sockets:
            self.clients_tickers_sockets[ticker] = [ws]
            self.listener.add_ticker(ticker)
        else:
            self.clients_tickers_sockets[ticker] += ws

    def on_ticker(self, _, message):
        ticker = message['id']
        users = self.clients_tickers_sockets[ticker]
        map(lambda user: user.send(json.dumps(ticker)), users)
