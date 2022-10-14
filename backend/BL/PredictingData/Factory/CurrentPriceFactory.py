from selenium.common.exceptions import NoSuchElementException

from Common.DataCommon.ModelDataHandler import get_last_price
from PredictingData.Logs.ApiLogs import FAIL_GET_DATA_FROM_HTML
from Logger import Logger
from PullingData.YahooApi import LiveData


def get_current_price(ticker: str):
    return get_last_price(ticker)
