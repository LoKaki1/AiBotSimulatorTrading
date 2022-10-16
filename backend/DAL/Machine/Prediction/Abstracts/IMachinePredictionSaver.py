from typing import Dict


class IMachinePredictionSaver:

    def save_prediction(self, ticker: str, predicted_price: float, ):
        """
        :param ticker: ticker name
        :param predicted_price:
        :return:
        """
        pass

    def is_ticker_predicted(self, ticker: str) -> bool:
        """
        :param ticker:
        :return: true if ticker is in database
        """
        pass

    def get_ticker_prediction(self, ticker: str) -> float:
        """
        :param ticker:
        :return:
        """
        pass

    def get_prediction_data(self) -> Dict[str, float]:
        """
        :return:
        """

        pass
