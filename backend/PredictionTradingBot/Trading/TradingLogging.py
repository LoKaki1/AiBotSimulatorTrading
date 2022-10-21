from typing import Union

from Common.Logger import Logger
from PredictionTradingBot.Trading.Abstracts.ITrader import ITrader


def default_logger(order_type: str, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
    Logger.info(f"{order_type} {quantity} share of stock: {ticker} at price: {price}. \n type of order{typeof}")


class TradingLogging(ITrader):

    def buy(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        default_logger('buy', ticker, typeof, quantity, price)

    def sell(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        default_logger('sell', ticker, typeof, quantity, price)

    def short(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        default_logger('short', ticker, typeof, quantity, price)

    def cover(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        default_logger('cover', ticker, typeof, quantity, price)
