from BL.MachineLogic.PredictionLogic.MachinePredictionLogic import MachinePredictionLogic
from BL.PredictingData.Factory.StockPredictionFactory import StockPredictionFactory
from BL.UsersLogic.UserWatchlist.UserWatchlistLogic import UserWatchlistLogic
from BL.WatchlistPrediction.WatchlistPrediction import WatchlistPrediction
from DAL.Machine.Prediction.MachinePredictionJsonImplementation import MachinePredictionJsonImplementation
from DAL.Users.Watchlist.UserWatchlistJsonImplementation import UserWatchlistJsonImplementation

PREDICTION_PATH = '../Data/prediction.json'
WATCHLIST_PATH = '../Data/watchlists.json'


def bootstrapper():

    machine_dal = MachinePredictionJsonImplementation(PREDICTION_PATH)
    watchlist_dal = UserWatchlistJsonImplementation(WATCHLIST_PATH)

    prediction_factory = StockPredictionFactory()
    machine_logic = MachinePredictionLogic(machine_dal, prediction_factory)
    watchlist_logic = UserWatchlistLogic(watchlist_dal)
    watchlist_prediction_manager = WatchlistPrediction(machine_logic, watchlist_logic)

    return watchlist_prediction_manager
