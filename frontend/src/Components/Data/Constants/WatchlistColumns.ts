import { GridColumns } from "@mui/x-data-grid";

export const COLUMNS: GridColumns =  [
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
      ]
