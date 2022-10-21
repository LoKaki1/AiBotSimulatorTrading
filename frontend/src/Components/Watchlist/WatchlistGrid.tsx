import { DataGrid, GridColumns } from "@mui/x-data-grid";
import { useCallback, useEffect } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { useTicker } from "../../Hooks/Context/TickerContext";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { COLUMNS } from "../Data/Constants/WatchlistColumns";
import { getUserWatchlist } from "./WatchlistCommon";
import "./WatchlistGrid.css";
import {
  IMessageEvent,
  w3cwebsocket,
} from "websocket";
import { YAHOO_WEB_SOCKET } from "../../Common/URLS";
import protobuf from "protobufjs";
import { onClose, onMessage, onOpen } from "./WebSocketWatchlist/YahooSubscribeListeners";


const columns: GridColumns = COLUMNS;

export default function WatchlistGrid() {
  const { watchlist, setWatchlist } = useWatchlist();
  const { setTicker } = useTicker();

  const subscribeTicker = async (watchlistResulted: Ticker[]) => {
    const tickers = watchlistResulted.map((tickerObject: Ticker) => tickerObject.ticker);
    const socket = new w3cwebsocket(YAHOO_WEB_SOCKET);
    protobuf.load("./YPricingData.proto", function (err, root) {
      if (err) {
        return err;
      }
      const Yaticker = root?.lookupType("yaticker");
      socket.onopen = () => onOpen(tickers, socket);
      socket.onmessage = (message: IMessageEvent) => onMessage(message, Yaticker, setWatchlist)
      socket.onclose = () => onClose(socket, tickers);
    });
  };
  const firstCall = async () => {
    const watchlistResulted = await getUserWatchlist(setWatchlist);
    console.log(`watchlist=${watchlistResulted}`);
    await subscribeTicker(watchlistResulted);
  }
  useEffect(() => {
    firstCall();
  }, []);
 
  return (
    <div className="watchlist">
      <DataGrid
        style={{
          fontSize: 18,
        }}
        rows={watchlist}
        columns={columns}
        autoHeight
        rowsPerPageOptions={[-1]}
        pagination={undefined}
        hideFooter={true}
        onRowClick={(row) => {
          setTicker(row.row.ticker);
        }}
      />
    </div>
  );
}
