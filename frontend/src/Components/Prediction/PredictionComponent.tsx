import React from "react";
import Loader from "../Loader/Loader";
import PredictionButton from "./PredictionParts/PredictionButton";
import PredictionTickerInput from "./PredictionParts/PredictionTickerInput";

export default function PredictionComponent() {
  return (
    <div style={{paddingBottom: 5,  display: 'flex', justifyContent: 'space-between', maxWidth: '24%'}}>
      <PredictionTickerInput />
      <PredictionButton />
      <Loader/>
    </div>
  );
}
