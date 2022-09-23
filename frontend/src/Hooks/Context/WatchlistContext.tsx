import { useContext, useState, Dispatch, SetStateAction, createContext } from 'react'
import { Ticker } from '../../Common/Types/TickerType';

type ContextType = {
    watchlist: Ticker[],
    setWatchlist: Dispatch<SetStateAction<Ticker[]>>,
} | any

const WatchlistContext = createContext<ContextType>({});
export function WatchlistProvider({ children } : {children : any}) {
  const [watchlist, setWatchlist] = useState<Ticker[]>([]);
    return (
        <WatchlistContext.Provider value={{ watchlist, setWatchlist }}>
              {children}
        </WatchlistContext.Provider>
    );
}

export const useWatchlist = () => {
  const { watchlist, setWatchlist } = useContext(WatchlistContext);
  return {watchlist, setWatchlist };
}