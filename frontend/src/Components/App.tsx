import FatherHook from "../Hooks/FatherHook";
import "./App.css";
import Chart from "./CandleChart/Chart";
import PredictionWatchlist from "./PredictionWatchlist/PredictionWatchlist";

function App() {
  return (
    <FatherHook>
      <div>
        <PredictionWatchlist />
      </div>
    </FatherHook>
  );
}

export default App;
