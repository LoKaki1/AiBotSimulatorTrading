from typing import List


class IUserWatchlist:

    def load_user_watchlist(self, user: str) -> List[str]:
        """
        :param user: username or user id (identify of the user)
        :return: user watchlist, list of tickers ["abc", ...]
        """
        pass

    def update_user_watchlist(self, user: str, watchlist: List[str]):
        """
        :param user:  user: username or user id (identify of the user)
        :param watchlist: user watchlist, list of tickers ["abc", ...]
        """
        pass
