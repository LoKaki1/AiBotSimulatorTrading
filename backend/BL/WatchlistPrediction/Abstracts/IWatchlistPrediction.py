

class IWatchlistPrediction:

    def predict_ticker(self, user: str, ticker: str, **kwargs) -> dict:
        """
        Function to predict ticker and update to watchlist if ticker is missing
        :param user:
        :param ticker:
        :param kwargs:
        :return:
        """
        pass

    def get_predicted_watchlist(self, user: str) -> list:
        """
        Function to predict all watchlist using function in machine logic and users logic for cache memo
        :param user:
        :return:
        """