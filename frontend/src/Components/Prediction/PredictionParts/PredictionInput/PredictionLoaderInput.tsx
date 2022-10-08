import React from "react";
import Loader from "./Loader/Loader";
import PredictionTickerInput from "./PredictionTickerInput";

export default function PredictionLoaderInput() {
  return (
    <div style={{width: '50%'}}>
      <PredictionTickerInput />
      <Loader />
    </div>
  );
}
