import React from 'react'
import { useTicker } from '../../../Hooks/Context/TickerContext'
import axios  from 'axios';
import { PREDICTION_URL } from '../../../Common/URLS';

export default function PredictionButton() {
    const { ticker } = useTicker();
    const predictTicker = async () => {
        console.log(`sending ${ticker} to prediction🛸`);
        const response = await axios.get(PREDICTION_URL, {
            headers: {
                ticker: ticker
            }
        });
        console.log(`Server sent ${response.data}`);
    }
    return (
        <button onClick = {predictTicker}> Predict🚀 </button>
    )
}