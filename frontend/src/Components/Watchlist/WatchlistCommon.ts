import axios from "axios";
import { Ticker } from "../../Common/Types/TickerType";
import { WATCHLIST_URL } from "../../Common/URLS";

export const getUserWatchlist = async (setWatchlist: (watchlist: Ticker[]) => void) => {
    try {
      console.log('Waiting for watclist📋');
      const response = await axios.get(WATCHLIST_URL);
      const watchlist = response.data.watchlist;
      setWatchlist(watchlist);
      console.log(`got watchlist ${watchlist}`)
      return watchlist;
    } catch (err) {
      console.log(`Something went wrong in getting watchlist, ${err}`);
      return [];
    }
  };