import { useEffect } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { DataGrid, GridColumns } from "@mui/x-data-grid";
import "./WatchlistGrid.css";
import axios from "axios";
import { WATCHLIST_URL } from "../../Common/URLS";
import { headers } from "../../Common/headers";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";

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
  const {watchlist, setWatchlist} = useWatchlist();

  const getUserWatchlist = async () => {
    try {
      const response = await axios.get(WATCHLIST_URL, { headers: headers });
      const watchlist = response.data.watchlist;
      setWatchlist(watchlist);
    }
    catch(err) {
      console.log(`Something went wrong in getting watchlist, ${err}`)
    }
  };

  useEffect(() => {
    getUserWatchlist();
  }, []);

  return (
    <div className="watchlist">
      <DataGrid
        style={{
          fontSize: 18,
          border: "none",
          minHeight: '600px'
        }}
        rows={watchlist}
        columns={columns}
        autoHeight
        rowsPerPageOptions={[-1]}
        pagination={undefined}
        hideFooter={true}
      />
    </div>
  );
}
