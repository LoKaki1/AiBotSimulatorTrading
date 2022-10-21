from typing import Callable


class IEventListener:

    def connect_ticker_to_listener(self, ticker: str, event: Callable):
        """
        Function to connect tickers to the event loop, when a price comes or something happens
        in the ticker data, it will call the function
        :param ticker:
        :param event:
        :return:
        """
        pass
