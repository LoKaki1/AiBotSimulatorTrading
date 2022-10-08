import FatherHook from "../Hooks/FatherHook";
import PredictionComponent from "./Prediction/PredictionComponent";
import WatchlistGrid from "./Watchlist/WatchlistGrid";
import "./App.css";
import Chart from "./CandleChart/Chart";
import PredictionWatchlist from "./PredictionWatchlist/PredictionWatchlist";

function App() {
  return (
    <FatherHook>
      <div>
        <PredictionWatchlist />
        {/* <Chart /> */}
      </div>
    </FatherHook>
  );
}

export default App;
