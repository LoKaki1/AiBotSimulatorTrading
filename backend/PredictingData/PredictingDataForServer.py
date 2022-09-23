from Common.DataCommon.ModelDataHandler import open_json

WATCHLIST_PATH = '../Data/watchlist.json'


def predicting_user_watchlist(user: str):
    json_data = open_json(WATCHLIST_PATH)
    user_watchlist = get_user_watchlist(json_data, user)
    # Todo Literly predict the data
    return user_watchlist


def get_user_watchlist(watchlist_data, user):
    return list(filter(lambda x: x['username'] == user, watchlist_data))[0]['watchlist']
