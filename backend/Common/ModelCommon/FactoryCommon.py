from typing import Union, Dict
import datetime as dt

from Common.Constants.DataConstant import PREDICTED_PRICE, DATE
from Common.Constants.FormatConstants import DATE_FORMAT


def create_ticker_object(predicted_price: float) -> Dict[str, Union[float, str]]:
    today = dt.datetime.now().strftime(DATE_FORMAT)
    return {PREDICTED_PRICE: predicted_price, DATE: today}
