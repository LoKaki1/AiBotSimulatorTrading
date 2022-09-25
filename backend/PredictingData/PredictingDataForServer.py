from Common.DataCommon.ModelDataHandler import open_json, write_in_json

WATCHLIST_PATH = '../Data/watchlist.json'


def _get_user_watchlist(user: str):
    json_data = open_json(WATCHLIST_PATH)

    return __get_user_watchlist(json_data, user)


def predicting_user_watchlist(user: str):
    # Todo Literly predict the data
    return _get_user_watchlist(user)


def __get_user_watchlist(watchlist_data, user):
    user_watchlist = dict(list(filter(lambda x: x['username'] == user, watchlist_data))[0])['watchlist']
    return user_watchlist


def update_watchlist(user, ticker_object):
    user_watchlist = _get_user_watchlist(user)
    if not user_watchlist:
        user_data = {"username": user, 'watchlist': [ticker_object]}
    else:
        user_data = {"username": user,
                     'watchlist': list(map(lambda x: ticker_object if x['ticker'] == ticker_object['ticker'] else x,
                                                user_watchlist))}
    write_in_json(WATCHLIST_PATH, user_data)

