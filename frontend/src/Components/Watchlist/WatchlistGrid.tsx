import { DataGrid, GridColumns } from "@mui/x-data-grid";
import { useCallback, useEffect } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { useTicker } from "../../Hooks/Context/TickerContext";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { COLUMNS } from "../Data/Constants/WatchlistColumns";
import { getUserWatchlist } from "./WatchlistCommon";
import "./WatchlistGrid.css";
import {
  client,
  connection,
  IMessageEvent,
  Message,
  w3cwebsocket,
} from "websocket";
import { YAHOO_WEB_SOCKET } from "../../Common/URLS";
import protobuf from "protobufjs";

const { Buffer } = require("buffer/");

const columns: GridColumns = COLUMNS;

export default function WatchlistGrid() {
  const { watchlist, setWatchlist } = useWatchlist();
  const { setTicker } = useTicker();
  const subscribeTicker = useCallback(() => {
    const tickers = ["NIO", "TSLA", "BIG", "XPEV", "LI", "AAPL"];
    const socket = new w3cwebsocket(YAHOO_WEB_SOCKET);
    protobuf.load("./YPricingData.proto", function (err, root) {
      if (err) {
        console.log(err);
        return err;
      }
      console.log(root);
      const Yaticker = root?.lookupType("yaticker");
      console.log(Yaticker);
      socket.onopen = () => {
        socket.send(
          JSON.stringify({
            subscribe: tickers,
          })
        );
      };
      socket.onmessage = (message: IMessageEvent) => {
        console.log("comming data");
        const result: any = Yaticker?.decode(
          new Buffer(message.data, "base64")
        );
        const price = result?.price.toFixed(2);
        const ticker = result?.id;
        setWatchlist((oldWatchlist: Ticker[]) => {
          const tickerIndex = oldWatchlist.findIndex(
            (tickerObject) => tickerObject.ticker == ticker
          );
          const tickerObject = {
            ...oldWatchlist[tickerIndex],
            price: price,
          };
          const newWatchlist = [...oldWatchlist];
          newWatchlist[tickerIndex] = tickerObject;
          return newWatchlist;
        });
        console.log(`${ticker}, ${price}`);
      };
      socket.onclose = () => {
        socket.send(
          JSON.stringify({
            unsubscribe: tickers,
          })
        );
      };
    });
  }, [watchlist]);

  useEffect(() => {
    getUserWatchlist(setWatchlist)
    // .then(() => {
    //   subscribeTicker();
    // });
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
