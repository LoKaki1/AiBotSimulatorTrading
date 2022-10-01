from selenium.common.exceptions import NoSuchElementException
from PredictingData.Logs.ApiLogs import FAIL_GET_DATA_FROM_HTML
from Logger import Logger
from PullingData.YahooApi import LiveData


def get_current_price(ticker: str):
    try:
        live_data = LiveData(ticker)
        current_price = live_data.get_live_price()
        return current_price
    except NoSuchElementException:
        Logger.error(FAIL_GET_DATA_FROM_HTML.format(ticker=ticker))
        return -1
