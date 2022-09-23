import { TickerProvider } from "./Context/TickerContext";
import { WatchlistProvider } from "./Context/WatchlistContext";

export default function FatherHook({ children }: { children: any }) {
  return (
    <>
      <TickerProvider>
        <WatchlistProvider>{children}</WatchlistProvider>
      </TickerProvider>
    </>
  );
}
