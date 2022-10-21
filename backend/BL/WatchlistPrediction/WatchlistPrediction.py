from BL.MachineLogic.PredictionLogic.Abstracts.IMachinePredictionLogic import IMachinePredictionLogic
from BL.UsersLogic.UserWatchlist.Abstracts.IUserWatchlistLogic import IUserWatchlistLogic
from BL.WatchlistPrediction.Abstracts.IWatchlistPrediction import IWatchlistPrediction
from Common.Constants.DataConstant import TICKER, PREDICTED_PRICE, CURRENT_PRICE, ID
from Common.DataCommon.ModelDataHandler import get_last_price


class WatchlistPrediction(IWatchlistPrediction):
    def __init__(self, machine_logic: IMachinePredictionLogic, users_watchlist_logic: IUserWatchlistLogic):
        self.machine_logic = machine_logic
        self.user_watchlist_logic = users_watchlist_logic

    def predict_ticker(self, user: str, ticker: str, **kwargs) -> dict:
        """
        Function to predict ticker and update to watchlist if ticker is missing
        :param user:
        :param ticker:
        :param kwargs:
        :return:
        """
        self.user_watchlist_logic.update_user_watchlist(user, ticker)
        return self.build_ticker_object(ticker, **kwargs)

    def get_predicted_watchlist(self, user: str) -> list:
        user_watchlist = self.user_watchlist_logic.get_user_watchlist(user)
        predicted_watchlist = [self.build_ticker_object(ticker) for ticker in user_watchlist]
        return predicted_watchlist

    def build_ticker_object(self, ticker, **kwargs):
        return {
                TICKER: ticker,
                PREDICTED_PRICE: self.machine_logic.predict_ticker(ticker, **kwargs),
                CURRENT_PRICE: get_last_price(ticker), ID: id(ticker)
            }
