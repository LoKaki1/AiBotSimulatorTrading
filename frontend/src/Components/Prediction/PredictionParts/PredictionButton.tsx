import React from "react";
import { useTicker } from "../../../Hooks/Context/TickerContext";
import axios from "axios";
import { PREDICTION_URL } from "../../../Common/URLS";
import "../Prediction.css";
import { headers } from "../../../Common/headers";

export default function PredictionButton() {
  const { ticker } = useTicker();
  const predictTicker = async () => {
    console.log(`sending ${ticker} to prediction🛸`);
    const response = await axios.get(PREDICTION_URL, {
      headers,
      params: {
        ticker: ticker,
      },
    });
    console.log(`Server sent ${response.data}`);
  };
  return (
    <button className="prediction-button" onClick={predictTicker}>
      Predict🚀
    </button>
  );
}
