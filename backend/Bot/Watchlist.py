from typing import Union


class Watchlist:
    def __init__(self, watchlist: list):
        self.watchlist = watchlist
        self.open_trades = []
        self.close_trades = []
        self.never_opened = [ticker for ticker in self.watchlist]

    def open_trade(self, ticker: Union[str, list]):
        if isinstance(ticker, str):
            self.open_trades.append(ticker)
            self.never_opened.remove(ticker)
        else:
            self.open_trades.extend(ticker)
            self.never_opened = [new_ticker for new_ticker in self.never_opened if new_ticker not in ticker]

    def close_trade(self, ticker):
        self.open_trades.remove(ticker)
        self.close_trades.append(ticker)
