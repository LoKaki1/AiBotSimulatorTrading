from Common.DataCommon.ModelDataHandler import open_json

WATCHLIST_PATH = '../Data/watchlist.json'


def _get_user_watchlist(user: str):
    json_data = open_json(WATCHLIST_PATH)

    return __get_user_watchlist(json_data, user)


def predicting_user_watchlist(user: str):

    # Todo Literly predict the data
    return _get_user_watchlist(user)


def _add_id(obj):
    obj['id'] = id(obj) if 'id' not in obj else obj['id']
    return obj


def __get_user_watchlist(watchlist_data, user):
    user_watchlist = dict(list(filter(lambda x: x['username'] == user, watchlist_data))[0])['watchlist']
    user_watchlist = [_add_id(ticker) for ticker in user_watchlist]
    return user_watchlist


def update_watchlist(user, ticker_object):
    user_watchlist = _get_user_watchlist(user)
    user_watchlist = list(map(lambda x: ticker_object if x['ticker'] == ticker_object['ticker'] else x,
                         user_watchlist))
