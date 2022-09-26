import PredictionButton from "./PredictionParts/PredictionButton";
import PredictionLoaderInput from "./PredictionParts/PredictionInput/PredictionLoaderInput";

export default function PredictionComponent() {
  return (
    <div style={{paddingBottom: 6,  display: 'flex',}}>
      <PredictionLoaderInput />
      <PredictionButton />
    </div>
  );
}
