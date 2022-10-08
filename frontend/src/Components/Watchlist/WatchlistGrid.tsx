import { DataGrid, GridColumns } from "@mui/x-data-grid";
import axios from "axios";
import { useEffect } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { CURRENT_PRICE_URL } from "../../Common/URLS";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { useTicker } from "../../Hooks/Context/TickerContext";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { getUserWatchlist } from "./WatchlistCommon";
import "./WatchlistGrid.css";

const columns: GridColumns = [
  {
    headerName: "Ticker 📊",
    field: "ticker",
    align: "center",
    headerAlign: "center",
    flex: 1,
  },
  {
    headerName: "Price 💰",
    field: "price",
    align: "center",
    headerAlign: "center",
    flex: 1,
  },
  {
    headerName: "Predicted Price🚀",
    field: "predictedPrice",
    align: "center",
    headerAlign: "center",
    flex: 2,
  },
  { field: "id", headerName: "ID", hide: true },
];

export default function WatchlistGrid() {
  const { watchlist, setWatchlist } = useWatchlist();
  const { setHistoricalData } = useHistoricalData();
  const { setTicker } = useTicker();
  const updateWatchlist = () => {
    const tickers = watchlist.map((ticker: Ticker) => ticker.ticker);
    const prices = tickers.map(async (ticker: string) => {
      const response = await axios.get(`${CURRENT_PRICE_URL}?ticker=${ticker}`);
      return response.data.currentPrice;
    });
    console.log(prices);
  };
  useEffect(() => {
    console.log("really wating twice🎈");
    getUserWatchlist(setWatchlist);
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
        onRowClick={(row) => setTicker(row.row.ticker)}
      />
    </div>
  );
}
