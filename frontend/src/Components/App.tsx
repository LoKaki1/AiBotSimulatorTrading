import React from "react";
import { TickerProvider } from "../Hooks/Context/TickerContext";
import FatherHook from "../Hooks/FatherHook";
import PredictionComponent from "./Prediction/PredictionComponent";
import WatchlistGrid from "./Watchlist/WatchlistGrid";
import "./App.css";

function App() {
  return (
    <FatherHook>
      <PredictionComponent />
      <WatchlistGrid />
    </FatherHook>
  );
}

export default App;
