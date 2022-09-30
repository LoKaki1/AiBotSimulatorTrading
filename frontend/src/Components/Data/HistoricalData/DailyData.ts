import { GridRowParams } from "@mui/x-data-grid";
import axios from "axios";
import { Dispatch, SetStateAction } from "react";
import { CandleType } from "../../../Common/Types/CandleType";
import { TICKER_DAILY_CAHRT } from "../../../Common/URLS";

export const getDailyData = async (
    tickerRow: GridRowParams,
    setHistoricalData: Dispatch<SetStateAction<CandleType>>
  ) => {
    const ticker = tickerRow.row.ticker;
    console.log(`Getting from server data about ${ticker} ⚡`);
    const chartResponnse = await axios.get(
      `${TICKER_DAILY_CAHRT}?ticker=${ticker}&start_day=2022-01-01`
    );
    const chartData = chartResponnse.data.dailyData;
     setHistoricalData(chartData);
    return chartData;
  };
  