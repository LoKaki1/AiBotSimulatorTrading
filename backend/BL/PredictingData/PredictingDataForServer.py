from Common.DataCommon.ModelDataHandler import open_json, write_in_json, update_json_where

WATCHLIST_PATH = '../Data/watchlist.json'


def _get_user_watchlist(user: str):
    json_data = open_json(WATCHLIST_PATH)

    return __get_user_watchlist(json_data, user)


def predicting_user_watchlist(user: str):
    # Todo Literly predict the data
    return _get_user_watchlist(user)


def __get_user_watchlist(watchlist_data, user) -> list:
    user_watchlist = dict(list(filter(lambda x: x['username'] == user, watchlist_data))[0])['watchlist']
    return user_watchlist


def update_watchlist(user, ticker_object):
    user_watchlist = _get_user_watchlist(user)
    if ticker_object['ticker'] in (tickers := get_ticker_in_watchlist(user_watchlist)):
        user_watchlist[tickers.index(ticker_object['ticker'])] = ticker_object
    else:
        user_watchlist.append(ticker_object)
    user_data = {
        "username": user,
        "watchlist": user_watchlist
    }

    update_json_where(WATCHLIST_PATH, 'username', user, user_data)


def get_ticker_in_watchlist(watchlist: list) -> list:
    return list(
        map(
         lambda ticker_object: ticker_object['ticker'], watchlist
        )
    )
