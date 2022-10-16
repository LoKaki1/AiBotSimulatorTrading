from typing import List, Dict

from Common.DataCommon.JsonCommon import open_json, write_json
from DAL.Users.Watchlist.Abstracts.IUserWatchlist import IUserWatchlist


class UserWatchlistJsonImplementation(IUserWatchlist):

    def __init__(self, path):
        self.path = path

    def load_users_watchlist(self) -> Dict[str, List[str]]:
        users_watchlist = open_json(self.path)
        return users_watchlist

    def load_user_watchlist(self, user: str) -> List[str]:
        """
        :param user: username or user id (identify of the user)
        :return: user watchlist, list of tickers ["abc", ...]
        """
        users_watchlist = open_json(self.path)
        return users_watchlist[user]

    def update_user_watchlist(self, user: str, watchlist: List[str]):
        """
        :param user:  user: username or user id (identify of the user)
        :param watchlist: user watchlist, list of tickers ["abc", ...]
        """
        users_watchlist: dict = open_json(self.path)
        users_watchlist[user] = watchlist
        write_json(self.path, users_watchlist)