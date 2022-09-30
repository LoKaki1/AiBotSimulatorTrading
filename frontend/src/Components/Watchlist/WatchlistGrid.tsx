import { useEffect } from "react";
import { DataGrid, GridColumns, GridRowParams } from "@mui/x-data-grid";
import "./WatchlistGrid.css";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { getUserWatchlist } from "./WatchlistCommon";
import axios from "axios";
import { TICKER_DAILY_CAHRT } from "../../Common/URLS";

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

const getDailyData = async (tickerRow: GridRowParams) => {
  const ticker = tickerRow.row.ticker;
  console.log(`Getting from server data about ${ticker} ⚡`);
  const chartResponnse = await axios.get(
    `${TICKER_DAILY_CAHRT}?ticker=${ticker}`
  );
  const chartData = chartResponnse.data;
  console.log(chartData);
};

export default function WatchlistGrid() {
  const { watchlist, setWatchlist } = useWatchlist();

  useEffect(() => {
    getUserWatchlist(setWatchlist);
  }, [setWatchlist]);

  return (
    <div className="watchlist">
      <DataGrid
        style={{
          fontSize: 18,
          border: "none",
          minHeight: "400px",
        }}
        rows={watchlist}
        columns={columns}
        autoHeight
        rowsPerPageOptions={[-1]}
        pagination={undefined}
        hideFooter={true}
        onRowClick={getDailyData}
      />
    </div>
  );
}
