import React from "react";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import { useInterval } from "../../Hooks/Context/IntervalsContext";

export default function IntervalsButton() {
  const { setHistoricalData } = useHistoricalData();
  const { setInterval } = useInterval();

  const intervals = ["1d", "5m", "1m"];
  useEffect(() => {
    
  })
  return (
    <div>
      {intervals.map((interval) => (
        <button onClick={() => setInterval(interval)}> {interval}📈 </button>
      ))}
    </div>
  );
}
