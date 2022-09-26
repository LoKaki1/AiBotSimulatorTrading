import { useTicker } from "../../../../Hooks/Context/TickerContext";
import "../../Prediction.css";

export default function PredictionTickerInput() {
  const { ticker, setTicker } = useTicker();
  return (
    <input
      className="prediction-input"
      value={ticker}
      onChange={(e) => setTicker(e.target.value.toUpperCase())}
      placeholder={"Enter Ticker.."}
    ></input>
  );
}
