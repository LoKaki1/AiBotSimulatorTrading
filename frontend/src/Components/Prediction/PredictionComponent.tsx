import React from "react";
import PredictionButton from "./PredictionParts/PredictionButton";
import PredictionTickerInput from "./PredictionParts/PredictionTickerInput";

export default function PredictionComponent() {
  return (
    <div style={{paddingBottom: 5, alignContent: 'center'}}>
      <PredictionTickerInput />
      <PredictionButton />
    </div>
  );
}
