from typing import List

from BL.UsersLogic.UserWatchlist.Abstracts.IUserWatchlistLogic import IUserWatchlistLogic
from DAL.Users.Watchlist.Abstracts.IUserWatchlist import IUserWatchlist


class UserWatchlistLogic(IUserWatchlistLogic):

    def __init__(self, user_watchlist_dal: IUserWatchlist):
        self.user_watchlist_dal = user_watchlist_dal
        self.cache_watchlist = {}

    def get_user_watchlist(self, user: str) -> List[str]:
        """
        :param user:
        :return:
        """
        if user not in self.cache_watchlist:
            self.cache_watchlist[user] = self.user_watchlist_dal.load_user_watchlist(user)

        return self.cache_watchlist[user]

    def update_user_watchlist(self, user: str, ticker: str):
        """
        :param user:
        :param ticker:
        :return:
        """
        user_watchlist = self.get_user_watchlist(user)
        if ticker not in user_watchlist:
            user_watchlist.append(ticker)
            self.user_watchlist_dal.update_user_watchlist(user, user_watchlist)
