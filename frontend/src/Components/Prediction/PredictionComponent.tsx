import PredictionButton from "./PredictionParts/PredictionButton";
import PredictionLoaderInput from "./PredictionParts/PredictionInput/PredictionLoaderInput";

export default function PredictionComponent() {
  return (
    <div className='prediction-input-button-container'>
      <PredictionLoaderInput />
      <PredictionButton />
    </div>
  );
}
