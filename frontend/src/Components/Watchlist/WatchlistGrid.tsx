import React, { useState } from "react";
import { Ticker } from "../../Common/Types/TickerType";
import { DataGrid, GridColumns } from "@mui/x-data-grid";
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
    
    flex: 1,
  },
  { field: "id", headerName: "ID", hide: true },
];

export default function WatchlistGrid() {
  const [tableContent, settableContent] = useState<Ticker[]>([
    {
      ticker: "NIO",
      predictedPrice: 6,
      price: 6,
      id: 1,
    },
  ]);

  return (
    <div className="watchlist">
      <DataGrid
        style={{ fontSize: 22 }}
        rows={tableContent}
        columns={columns}
        autoHeight
        
      />
    </div>
  );
}
