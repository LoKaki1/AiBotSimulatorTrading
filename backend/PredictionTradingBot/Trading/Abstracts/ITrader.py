from typing import Union


class ITrader:

    def buy(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        pass

    def sell(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        pass

    def short(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        pass

    def cover(self, ticker: str, typeof: str, quantity: Union[float, int], price: float = None):
        """
        :param ticker:
        :param typeof: [LMT, MKT, STOP, STOP LMT]
        :param quantity: number of shares
        :param price:
        :return:
        """
        pass
