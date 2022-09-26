import React from "react";
import { useTicker } from "../../../Hooks/Context/TickerContext";
import axios from "axios";
import { TICKER_OBJECT_PREDICTION, WATCHLIST_URL } from "../../../Common/URLS";
import "../Prediction.css";
import { headers } from "../../../Common/headers";
import { useWatchlist } from "../../../Hooks/Context/WatchlistContext";

export default function PredictionButton() {
  const { ticker } = useTicker();
  const { setWatchlist } = useWatchlist();

  const sendToPrediction = async () => {
    console.log(`sending ${ticker} to prediction🛸`);
    await axios.get(TICKER_OBJECT_PREDICTION, {
      headers: headers,
      params: {
        ticker: ticker,
      },
    });
  }

  const getWatchlistAfterPrediction = async () => {
    console.log(`getting watclist after prediction 😚`)
    const watchlistReponse = await axios.get(WATCHLIST_URL, {
      headers: headers,
    });
    const watchlist = watchlistReponse.data.watchlist;
    console.log(`result data from server ${watchlist}`)
    setWatchlist(watchlist);
  }

  const predictTicker = async () => {
    try {
        await sendToPrediction();
        await getWatchlistAfterPrediction();
    }
    catch(err) {
      console.log(`Something went wrong with getting prediction result from server, ${err}`)
    }
  }

  return (
    <button className="prediction-button" onClick={predictTicker}>
      Predict🚀
    </button>
  );
}
