import { Button } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { TICKER_INTERDAY_CAHRT } from "../../Common/URLS";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { useTicker } from "../../Hooks/Context/TickerContext";
import { getDailyData } from "../Data/HistoricalData/DailyData";
import { getInterdayData } from "../Data/HistoricalData/InterdayData";

export default function IntervalsButton() {
  const [ interval, setInterval ]  = useState<string>('1d');
  const { ticker } = useTicker();
  const { setHistoricalData } = useHistoricalData();
  const intervals = ["1d", "5m", "1m"];
  
  const test = async () => {
    console.log(`${TICKER_INTERDAY_CAHRT}?ticker=${ticker}&interval=${interval}&range=1d`)
    const chartResponnse = await axios.get(
      `${TICKER_INTERDAY_CAHRT}?ticker=${ticker}&interval=${interval}&range="1d"`
    );
    const chartData = chartResponnse.data.interdayData;
    setHistoricalData(chartData);
  }
  useEffect(() => {
    if (interval == "1d") {
      getDailyData(ticker, setHistoricalData);
    }
    else {
      test();
    }
  }, [interval, ticker]);

  return (
    <div style={{  }}>
      {intervals.map((intervalInList, index) => (
        <Button onClick={() => setInterval(intervalInList)} key={index}style={{backgroundColor: 'white', padding: 10}} > {intervalInList}📈 </Button>
      ))}
    </div>
  );
}
