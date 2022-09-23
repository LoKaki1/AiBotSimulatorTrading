import React from "react";
import { useTicker } from "../../../Hooks/Context/TickerContext";
import axios from "axios";
import { CURRENT_PRICE_URL, PREDICTION_URL } from "../../../Common/URLS";
import "../Prediction.css";
import { headers } from "../../../Common/headers";
import { useWatchlist } from "../../../Hooks/Context/WatchlistContext";
import { Ticker } from "../../../Common/Types/TickerType";

export default function PredictionButton() {
  const { ticker } = useTicker();
  const {setWatchlist} = useWatchlist();
  const predictTicker = async () => {
    console.log(`sending ${ticker} to prediction🛸`);
    const predictionResult = await axios.get(PREDICTION_URL, {
      headers,
      params: {
        ticker: ticker,
      },
    });
    const currentPriceResult = await axios.get(CURRENT_PRICE_URL, {
      headers
    });
    const currentPrice = currentPriceResult.data.currentPrice
    setWatchlist(( lastWatchlist: Ticker[] ) => [...lastWatchlist, {ticker: ticker, price: currentPrice, predictionPrice: predictionResult}]);

  };
  return (
    <button className="prediction-button" onClick={predictTicker}>
      Predict🚀
    </button>
  );
}
