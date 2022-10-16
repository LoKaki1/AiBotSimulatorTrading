from BL.PredictingData.StockPredictionAi import StockPrediction
from BL.PredictingData.Factory.Abstracts.IStockPredictionFactory import IStockPredictionFactory
from Common.DataCommon.ModelDataHandler import format_price


class StockPredictionFactory(IStockPredictionFactory):

    def predict_stock(self, ticker, **kwargs):
        stock_prediction_ai = StockPrediction(ticker, **kwargs)
        predicted_price = stock_prediction_ai.predict_next_price()
        return format_price(predicted_price)
