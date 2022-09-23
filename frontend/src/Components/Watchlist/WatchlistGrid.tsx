import { useState, useEffect } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { DataGrid, GridColumns } from "@mui/x-data-grid";
import "./WatchlistGrid.css";
import axios from "axios";
import { WATCHLIST_URL } from "../../Common/URLS";
import { headers } from "../../Common/headers";

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
  const [tableContent, settableContent] = useState<Ticker[]>([]);

  const getUserWatchlist = async () => {
    const response = await axios.get(WATCHLIST_URL, { headers: headers });
    const watchlist = response.data.watchlist;
    console.log(response);
    console.log(watchlist);
    settableContent(watchlist);
  };

  useEffect(() => {
    getUserWatchlist();
  }, []);
  return (
    <div className="watchlist">
      <DataGrid
        style={{ fontSize: 18 }}
        rows={tableContent}
        columns={columns}
        autoHeight
      />
    </div>
  );
}
