from typing import Dict


class IMachinePredictionLogic:

    def get_prediction_data(self) -> Dict[str, float]:
        """
        :return:
        """
        pass

    def update_prediction_data(self, ticker: str, price: float):
        """
        :param ticker:
        :param price:
        :return:
        """
        pass

    def predict_ticker(self, ticker, **kwargs) -> float:
        """
        :param ticker:
        :return:
        """
        pass


