import FatherHook from "../Hooks/FatherHook";
import PredictionComponent from "./Prediction/PredictionComponent";
import WatchlistGrid from "./Watchlist/WatchlistGrid";
import "./App.css";
import Chart from "./CandleChart/Chart";

function App() {
  return (
    <FatherHook>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          height: "100%"
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            width: "20%",
            position: 'relative',
            // alignItems: 'center',
            right: '10%'
          }}
        >
          <PredictionComponent />
          <WatchlistGrid />
        </div>
        <Chart />
      </div>
    </FatherHook>
  );
}

export default App;
