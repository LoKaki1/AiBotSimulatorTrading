from Common.DataCommon.ModelDataHandler import get_last_price


def get_current_price(ticker: str):
    return get_last_price(ticker)
