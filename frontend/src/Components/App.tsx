import FatherHook from "../Hooks/FatherHook";
import PredictionComponent from "./Prediction/PredictionComponent";
import WatchlistGrid from "./Watchlist/WatchlistGrid";
import "./App.css";
import CandleStickChart from "./CandleChart/CandleStickChart";

function App() {
  return (
    <FatherHook>
      <PredictionComponent />
      <WatchlistGrid />
      <CandleStickChart/>
    </FatherHook>
  );
}

export default App;
