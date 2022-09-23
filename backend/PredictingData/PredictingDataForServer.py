from Common.DataCommon.ModelDataHandler import open_json

WATCHLIST_PATH = '../Data/watchlist.json'


def _get_user_watchlist(user: str):
    json_data = open_json(WATCHLIST_PATH)

    return __get_user_watchlist(json_data, user)


def predicting_user_watchlist(user: str):

    # Todo Literly predict the data
    return _get_user_watchlist(user)


def _add_id(obj):
    obj['id'] = id(obj)
    return obj


def __get_user_watchlist(watchlist_data, user):
    user_watchlist = dict(list(filter(lambda x: x['username'] == user, watchlist_data))[0])['watchlist']
    user_watchlist = [_add_id(ticker) for ticker in user_watchlist]
    return user_watchlist

