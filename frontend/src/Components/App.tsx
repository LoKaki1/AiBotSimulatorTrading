import FatherHook from "../Hooks/FatherHook";
import "./App.css";
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
