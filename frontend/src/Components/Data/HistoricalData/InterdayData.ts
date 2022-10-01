import { GridRowParams } from "@mui/x-data-grid";
import axios from "axios";
import { Dispatch, SetStateAction } from "react";
import { CandleType } from "../../../Common/Types/CandleType";
import { TICKER_DAILY_CAHRT, TICKER_INTERDAY_CAHRT } from "../../../Common/URLS";
import { START_DAY } from "../Constants/StartDay";



export const getInterdayData = async (
    ticker: string,
    setHistoricalData: Dispatch<SetStateAction<CandleType>>
  ) => {
    console.log(`Getting from server data about ${ticker} ⚡`);
    const chartResponnse = await axios.get(
      `${TICKER_INTERDAY_CAHRT}?ticker=${ticker}`
    );
    const chartData = chartResponnse.data.interdayData;
    setHistoricalData(chartData);
    return chartData;
  };
  