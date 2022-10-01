import { useEffect } from "react";
import { DataGrid, GridCellParams, GridColumns } from "@mui/x-data-grid";
import "./WatchlistGrid.css";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { getUserWatchlist } from "./WatchlistCommon";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { getDailyData } from "../Data/HistoricalData/DailyData";
import { useTicker } from "../../Hooks/Context/TickerContext";

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
  useEffect(() => {
    getUserWatchlist(setWatchlist);
  }, [setWatchlist]);

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
