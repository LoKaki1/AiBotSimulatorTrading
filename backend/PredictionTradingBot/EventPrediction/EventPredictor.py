from typing import Dict, Callable

from PredictionTradingBot.EventPrediction.Abstracrts.IEventListener import IEventPredictor, IEventListener


class EventPredictor(IEventListener):

    def __init__(self, data_listener):
        self.data_listener = data_listener

    def connect_tickers_to_listener(self, tickers_functions: Dict[str, Callable]):
        for ticker, event in tickers_functions:
            self.connect_ticker_to_listener(ticker, event)

    def connect_ticker_to_listener(self, ticker: str, event: Callable):
        """
        Function to connect tickers to the event loop, when a price comes or something happens
        in the ticker data, it will call the function
        :param ticker:
        :param event:
        :return:
        """
        self.data_listener.subscribe(ticker, event)