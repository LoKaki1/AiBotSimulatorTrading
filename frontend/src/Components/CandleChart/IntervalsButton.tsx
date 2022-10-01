import { Button } from "@mui/material";
import { useEffect, useState } from "react";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { useTicker } from "../../Hooks/Context/TickerContext";
import { getDailyData } from "../Data/HistoricalData/DailyData";
import { getInterdayData } from "../Data/HistoricalData/InterdayData";
import './CandleChart.css'

export default function IntervalsButton() {
  const [ interval, setInterval ]  = useState<string>('1d');
  const { ticker } = useTicker();
  const { setHistoricalData } = useHistoricalData();
  const intervals = ["1d", "5m", "1m"];

  useEffect(() => {
    if (interval == "1d") {
      getDailyData(ticker, setHistoricalData);
    }
    else {
      getInterdayData(ticker, interval, '1d', setHistoricalData);
    }
  }, [interval, ticker]);

  return (
    <div style={{marginBottom: '5px',  justifyContent: 'space-around'}}>
      {intervals.map((intervalInList, index) => (
        <button onClick={() => setInterval(intervalInList)} key={index} className={'interval-button'}>{intervalInList}</button>
      ))}
    </div>
  );
}
