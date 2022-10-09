from typing import List, Dict, Union

from PredictingData.Factory.TickerObjectFactory import create_ticker_object


class Prediction:

    def __init__(self, watchlist: List[str]):
        self.watchlist = watchlist

    def predict_prices(self) -> List[Dict[str: Union[str, float]]]:
        return [
            create_ticker_object(ticker) for ticker in self.watchlist
        ]
