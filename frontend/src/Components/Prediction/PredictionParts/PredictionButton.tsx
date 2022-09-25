import React from "react";
import { useTicker } from "../../../Hooks/Context/TickerContext";
import axios from "axios";
import { TICKER_OBJECT_PREDICTION } from "../../../Common/URLS";
import "../Prediction.css";
import { headers } from "../../../Common/headers";
import { useWatchlist } from "../../../Hooks/Context/WatchlistContext";
import { Ticker } from "../../../Common/Types/TickerType";

export default function PredictionButton() {
  const { ticker } = useTicker();
  const { setWatchlist } = useWatchlist();
  const predictTicker = async () => {
    try {
      console.log(`sending ${ticker} to prediction🛸`);
      const predictionResult = await axios.get(TICKER_OBJECT_PREDICTION, {
        headers,
        params: {
          ticker: ticker,
        },
      });
      console.log(`Got result from server ${predictionResult.data}`)
      setWatchlist((lastWatchlist: Ticker[]) => [
        ...lastWatchlist,
        predictionResult.data
      ]);
    }
    catch(err) {
      console.log(`Something went wrong with getting prediction result from server, ${err}`)
    }
  };
  return (
    <button className="prediction-button" onClick={predictTicker}>
      Predict🚀
    </button>
  );
}
