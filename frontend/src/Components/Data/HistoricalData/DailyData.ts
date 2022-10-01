import { GridRowParams } from "@mui/x-data-grid";
import axios from "axios";
import { Dispatch, SetStateAction } from "react";
import { CandleType } from "../../../Common/Types/CandleType";
import { TICKER_DAILY_CAHRT } from "../../../Common/URLS";
import { START_DAY } from "../Constants/StartDay";



export const getDailyData = async (
    ticker: string,
    setHistoricalData: Dispatch<SetStateAction<CandleType>>
  ) => {
    console.log(`Getting from server data about ${ticker} ⚡`);
    const chartResponnse = await axios.get(
      `${TICKER_DAILY_CAHRT}?ticker=${ticker}&start_day=${START_DAY}`
    );
    const chartData = chartResponnse.data.dailyData;
    setHistoricalData(chartData);
    return chartData;
  };
  