import React from "react";
import Loader from "./Loader/Loader";
import PredictionTickerInput from "./PredictionTickerInput";

export default function PredictionLoaderInput() {
  return (
    <div style={{ height: "4rem" }}>
      <PredictionTickerInput />
      <Loader />
    </div>
  );
}
