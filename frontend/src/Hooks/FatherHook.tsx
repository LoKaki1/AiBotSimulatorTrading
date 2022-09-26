import axios from "axios";
import { headers } from "../Common/headers";
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
          <LoaderContextProvider>{children}</LoaderContextProvider>
        </WatchlistProvider>
      </TickerProvider>
    </>
  );
}
