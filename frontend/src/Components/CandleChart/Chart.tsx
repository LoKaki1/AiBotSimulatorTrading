import CandleStickChart from "./CandleStickChart";
import IntervalsButton from "./IntervalsButton";

export default function Chart() {
  return (
    <div className='chart-buttons-container'>
      <IntervalsButton />
      <CandleStickChart />
    </div>
  );
}
