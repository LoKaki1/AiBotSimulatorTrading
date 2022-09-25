from PullingData.YahooApi import LiveData


def get_current_price(ticker: str):
    live_data = LiveData(ticker)
    return live_data.get_live_price()
