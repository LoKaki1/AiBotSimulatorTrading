from typing import Union, Dict, List, Callable, Any, Optional, Tuple

from PredictingData.Factory.CurrentPriceFactory import get_current_price


def logic_on_prediction_result(prediction_result: List[Dict[str, Union[str, float]]],
                               logic_injection: Callable[[str, float], Tuple[bool, Dict[str, Union[str, float]]]]) -> \
                                List[Dict[str, Union[str, float]]]:
    logic_result = []

    for ticker_prediction in prediction_result:
        ticker = ticker_prediction['ticker']
        predicted_price = ticker_prediction['predictedPrice']
        worth_trading, trading_data = logic_injection(ticker, predicted_price)

        if worth_trading:
            logic_result.append(logic_result)

    return logic_result


def very_simple_logic(ticker: str, predicted_price: float) -> Tuple[bool, Dict[str, Union[str, float]]]:
    current_price = get_current_price(ticker)
    result = {'ticker': ticker}
    if current_price > 1.05 * predicted_price:
        result['type'] = 'short'
        result['entry'] = current_price
        result['close'] = predicted_price
        result['stoploss'] = current_price * 1.07
    elif current_price < 1.05 * predicted_price:
        result['type'] = 'buy'
        result['entry'] = current_price
        result['close'] = predicted_price
        result['stoploss'] = current_price * 0.98
    else:
        return False, {}

    return True, result
