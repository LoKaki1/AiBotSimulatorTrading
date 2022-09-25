from PredictingData.Factory.CurrentPriceFactory import get_current_price
from PredictingData.Factory.PredictionFactory import predict_data_for_stock


def create_ticker_object(ticker: str):
    return {
        "ticker": ticker,
        "price": get_current_price(ticker),
        "predictedPrice": predict_data_for_stock(ticker),
        "id": id(ticker)
    }