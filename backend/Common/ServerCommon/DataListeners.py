from typing import Any, Callable

from yliveticker import YLiveTicker


def default_on_ticker(ws, data):
    print(ws, data, sep='\n')


class DataListener:

    def __init__(self, on_ticker: Callable[[Any, Any], Any] = default_on_ticker, tickers: list[str] = None):
        self.tickers = [] if tickers is None else tickers
        self.on_ticker = on_ticker
        self.yahoo_ticker_live = YLiveTicker(on_ticker=self.on_ticker, ticker_names=self.tickers)

    def add_ticker(self, ticker: str):
        self.tickers += ticker
        self.yahoo_ticker_live.ws.close()
        self.yahoo_ticker_live = YLiveTicker(on_ticker=self.on_ticker, ticker_names=self.tickers)

