import datetime
from typing import Dict, Union

from BL.MachineLogic.PredictionLogic.Abstracts.IMachinePredictionLogic import IMachinePredictionLogic
from BL.PredictingData.Factory.Abstracts.IStockPredictionFactory import IStockPredictionFactory
from Common.Constants.DataConstant import PREDICTED_PRICE, DATE
from Common.Constants.FormatConstants import DATE_FORMAT
from Common.Logger import Logger
from Common.ModelCommon import FactoryCommon
from DAL.Machine.Prediction.Abstracts.IMachinePredictionSaver import IMachinePredictionSaver


class MachinePredictionLogic(IMachinePredictionLogic):

    def __init__(self, prediction_dal: IMachinePredictionSaver, prediction_factory: IStockPredictionFactory):
        self.prediction_dal = prediction_dal
        self.prediction_data = self.prediction_dal.get_prediction_data()
        self.prediction_factory = prediction_factory

    def get_prediction_data(self) -> Dict[str, Dict[str, Union[float, str]]]:
        return self.prediction_data

    def predict_ticker(self, ticker, **kwargs) -> float:
        try:
            if ticker not in self.prediction_data or self.is_relevant_prediction(ticker):
                prediction = self.prediction_factory.predict_stock(ticker, **kwargs)
                prediction_date_result = FactoryCommon.create_ticker_object(prediction)
                self.prediction_data[ticker] = prediction_date_result
                self.prediction_dal.save_prediction(ticker, prediction)

            return self.prediction_data[ticker][PREDICTED_PRICE]

        except KeyError:
            Logger.error("Can't get data from yahoo api")

            return -1

    def is_relevant_prediction(self, ticker):
        date = datetime.datetime.strptime(self.prediction_data[ticker][DATE], DATE_FORMAT).date()
        today = datetime.datetime.today().date()

        return date < today
