import React from "react";
import PredictionComponent from "../Prediction/PredictionComponent";
import WatchlistGrid from "../Watchlist/WatchlistGrid";
import "./PredictionWatchlist.css";

export default function PredictionWatchlist() {
  return (
    <div className="prediction-container">
      <PredictionComponent />
      <WatchlistGrid />
    </div>
  );
}
