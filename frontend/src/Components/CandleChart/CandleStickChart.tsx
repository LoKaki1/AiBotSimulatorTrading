import { useEffect, useState } from "react";
import { useHistoricalData } from "../../Hooks/Context/HistoricalDataContext";
import Chart from "react-apexcharts";
import "./CandleChart.css";

export default function CandleStickChart() {
  const { historicalData, setHistoricalData } = useHistoricalData();
  const [series, setSeries] = useState<any>([{ data: [] }]);
  useEffect(() => {
    setSeries([{ data: historicalData }]);
  }, [historicalData, setSeries, setHistoricalData]);

  return (
    <div
      style={{

      }}
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
