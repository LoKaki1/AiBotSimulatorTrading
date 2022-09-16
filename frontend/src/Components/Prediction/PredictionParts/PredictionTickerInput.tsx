import React from "react";
import { useTicker } from "../../../Hooks/Context/TickerContext";

export default function PredictionTickerInput() {
  const { ticker, setTicker } = useTicker();
  return (
    <input
      value={ticker}
      onChange={(e) => setTicker(e.target.value.toUpperCase())}
      placeholder={"Enter Ticker.."}
    />
  );
}
