from typing import Dict

from Common.DataCommon.JsonCommon import open_json, write_json
from DAL.Machine.Prediction.Abstracts.IMachinePredictionSaver import IMachinePredictionSaver


class MachinePredictionJsonImplementation(IMachinePredictionSaver):

    def __init__(self, path: str):
        self.path = path

    def save_prediction(self, ticker: str, predicted_price: float):
        """
        :param ticker: ticker name
        :param predicted_price:
        :return:
        """
        ticker_data = open_json(self.path)
        ticker_data[ticker] = predicted_price
        write_json(self.path, ticker_data)

    def is_ticker_predicted(self, ticker: str) -> bool:
        """
        :param ticker:
        :return: true if ticker is in database
        """
        ticker_data = open_json(self.path)
        return ticker in ticker_data

    def get_ticker_prediction(self, ticker: str) -> float:
        """
        :param ticker:
        :return:
        """
        ticker_data = open_json(self.path)
        return ticker_data[ticker]

    def get_prediction_data(self) -> Dict[str, float]:
        return open_json(self.path)


