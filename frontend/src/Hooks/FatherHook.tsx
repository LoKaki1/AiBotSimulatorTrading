import axios from "axios";
import { headers } from "../Common/headers";
import { HistoricalDataContextProvider } from "./Context/HistoricalDataContext";
import { IntervalContextProvider } from "./Context/IntervalsContext";
import { LoaderContextProvider } from "./Context/LoaderContext";
import { TickerProvider } from "./Context/TickerContext";
import { WatchlistProvider } from "./Context/WatchlistContext";

export default function FatherHook({ children }: { children: any }) {
  const setHeaders = function () {
    axios.defaults.headers.common["Authorization"] = headers.username;
  };
  setHeaders();
  return (
    <>
      <TickerProvider>
        <WatchlistProvider>
          <LoaderContextProvider>
            <HistoricalDataContextProvider>
              <IntervalContextProvider>{children}</IntervalContextProvider>
            </HistoricalDataContextProvider>
          </LoaderContextProvider>
        </WatchlistProvider>
      </TickerProvider>
    </>
  );
}
