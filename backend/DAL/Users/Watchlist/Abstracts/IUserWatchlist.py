from typing import List, Dict


class IUserWatchlist:

    def load_users_watchlist(self) -> Dict[str, List[str]]:
        """
        :return:
        """
        pass

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
