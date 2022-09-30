import { useEffect, useState } from "react";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import Chart from "react-apexcharts";
import "./CandleChart.css";
import { getDailyData } from "../Data/HistoricalData/DailyData";
import { useWatchlist } from "../../Hooks/Context/WatchlistContext";

export default function CandleStickChart() {
  const { historicalData, setHistoricalData } = useHistoricalData();
  const { watchlist } = useWatchlist();
  const [series, setSeries] = useState<any>([{ data: [] }]);
  
  useEffect(() => {
    console.log(watchlist)
    getDailyData(watchlist[0]?.ticker ?? 'NIO', setHistoricalData);
  }, []);

  useEffect(() => {
    setSeries([{ data: historicalData }]);
  }, [historicalData, setSeries, setHistoricalData]);

  return (
    <div
      className='chart-container'
    >
      <Chart
        className="chart"
        options={{
          chart: {
            id: "basic-bar",
          },
          xaxis: {
            labels: {
              formatter: (value) => {
                return "";
              },
            },
          },
        }}
        series={series}
        type="candlestick"
      />
    </div>
  );
}
