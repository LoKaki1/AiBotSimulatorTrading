import { useTicker } from "../../../Hooks/Context/TickerContext";
import axios from "axios";
import { TICKER_OBJECT_PREDICTION } from "../../../Common/URLS";
import "../Prediction.css";
import { useWatchlist } from "../../../Hooks/Context/WatchlistContext";
import { getUserWatchlist } from "../../Watchlist/WatchlistCommon";
import { useLoader } from "../../../Hooks/Context/LoaderContext";

export default function PredictionButton() {
  const { ticker, setTicker } = useTicker();
  const { setWatchlist } = useWatchlist();
  const { setLoader } = useLoader();

  const sendToPrediction = async () => {
    console.log(`sending ${ticker} to prediction🛸`);
    setLoader(true);
    await axios.get(`${TICKER_OBJECT_PREDICTION}?ticker=${ticker}`);
    setTicker("");
  };

  const predictTicker = async () => {
    try {
      await sendToPrediction();
      await getUserWatchlist(setWatchlist);
      setLoader(false);
    } catch (err) {
      console.log(
        `Something went wrong with getting prediction result from server, ${err}`
      );
      setLoader(false);
    }
  };

  return (
    <button className="prediction-button" onClick={predictTicker}>
      Predict🚀
    </button>
  );
}
