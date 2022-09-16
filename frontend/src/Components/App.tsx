import React from "react";
import { TickerProvider } from "../Hooks/Context/TickerContext";
import FatherHook from "../Hooks/FatherHook";
import PredictionComponent from "./Prediction/PredictionComponent";

function App() {
  return (
    <FatherHook>
      <div>
        <PredictionComponent/>
      </div>
    </FatherHook>
  );
}

export default App;
