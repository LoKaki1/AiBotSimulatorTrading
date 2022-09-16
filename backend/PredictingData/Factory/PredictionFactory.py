from PredictingData.StockPredictionAi import StockPrediction


def predict_data_for_stock(ticker, **kwargs):
    """
    Add kwargs to stockPrediction
    """
    stock_predictor = StockPrediction(ticker, **kwargs)
    return stock_predictor.predict_next_price()
