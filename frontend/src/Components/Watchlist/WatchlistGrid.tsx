import { useEffect } from "react";
import { DataGrid, GridColumns } from "@mui/x-data-grid";
import "./WatchlistGrid.css";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";
import { getUserWatchlist } from "./WatchlistCommon";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { getDailyData } from "../Data/HistoricalData/DailyData";

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
  useEffect(() => {
    getUserWatchlist(setWatchlist);
  }, [setWatchlist]);

  return (
    <div className="watchlist">
      <DataGrid
        style={{
          fontSize: 18,
          border: "none",
          minHeight: "900px",
        }}
        rows={watchlist}
        columns={columns}
        autoHeight
        rowsPerPageOptions={[-1]}
        pagination={undefined}
        hideFooter={true}
        onRowClick={(row) => getDailyData(row.row.ticker, setHistoricalData)}
      />
    </div>
  );
}
