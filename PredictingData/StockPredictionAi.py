import datetime as dt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from Common.DataCommon import GattherData
from Common.Logger import Logger

""" My Constants """
START = dt.datetime(2020, 4, 15).strftime('%Y-%m-%d')
END = (dt.datetime.now() - dt.timedelta(days=0)).strftime('%Y-%m-%d')


class StockPrediction:

    def __init__(self, ticker):
        self.scalar = None
        self.ticker = ticker
        self.start = START
        self.end = END

    def get_data_for_fitting(self):
        """
        :return: Historical data of a stock and divide it into lists that each contains [[open, close, high, low], [...], ...]
        """
        return GattherData.get_data_from_yahoo(self.ticker, self.start, self.end)

    def scale_data(self, one_array_data_to_train: list):
        """
            func that sets the data to be between 0 and 1 means (40, 10) = (0.123, 0.01) something like that
            :returns the data after fitting it into numbers between 0 and 1
        """
        """ Making data without lists because scaled data cant
         use lists so data before = [[1, 2, 3, ...], [2, 3, 4, ...] ...] data after = [1, 2, 3, 2, 3, 4 ...] """

        data = np.array(one_array_data_to_train).reshape(-1, 1)

        "Reshape so it matches with scalar api"
        self.scalar = MinMaxScaler(feature_range=(0, 1))
        """ Fits x values of data (now it makes the real values ) """

        scaled_data = self.scalar.fit_transform(data)
        Logger.info('finish fitting data to scalar 😀')
        return scaled_data

    def build_data(self):
        plain_data = self.get_data_for_fitting()
        scaled_data = self.scale_data(plain_data)
        return scaled_data

    def prepare_data_for_model(self, sacled_data):
        """
        Good luck 😀
        :param sacled_data:
        :return:
        """

