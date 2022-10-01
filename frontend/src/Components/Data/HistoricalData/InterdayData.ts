import axios from "axios";
import { Dispatch, SetStateAction } from "react";
import { CandleType } from "../../../Common/Types/CandleType";
import { TICKER_INTERDAY_CAHRT } from "../../../Common/URLS";


export const getInterdayData = async (
    ticker: string,
    interval: string,
    range: string,
    setHistoricalData: Dispatch<SetStateAction<CandleType>>
  ) => {
    console.log(`Getting from server data about ${ticker} ⚡`);
    console.log(ticker, interval, range)
    const chartResponnse = await axios.get(
      `${TICKER_INTERDAY_CAHRT}?ticker=${ticker}&interval=${interval}&range=${range}`
    );
    const chartData = chartResponnse.data.interdayData;
    setHistoricalData(chartData);
    return chartData;
  };
  