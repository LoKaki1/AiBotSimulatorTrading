from typing import Union, Dict, List, Any, Tuple

from keras import Sequential
from keras.layers import Dense, LSTM, Dropout

from Common.Constants.MachineConstants import ACTIVATION, UNITS

MODEL_LAYERS_NAME_MODEL = {
    "Dense": Dense,
    "LSTM": LSTM,
    "Dropout": Dropout
}


def build_model_layers(layers: List[Dict[str, Dict[str, Union[str, float]]]],
                       input_shape: Tuple[Any, int]) -> Sequential:
    """
    :param layers:
    :param input_shape:
    :return: Layers model using strings that describe its behavior
    """
    first_layer = build_first_layer(layers[0], input_shape)
    model_layers = [build_layer(layer) for layer in layers]
    model_layers[0] = first_layer
    return Sequential(model_layers)


def get_layer_init(layer: Dict[str, Dict[str, Union[str, float]]]) -> Union[LSTM, Dense, Dropout]:
    return MODEL_LAYERS_NAME_MODEL[__get_the_first_key(layer)]


def build_layer(layer: Dict[str, Dict[str, Union[str, float]]]):
    layer_parameters = layer[(layer_name := __get_the_first_key(layer))]
    (units, activation) = (layer_parameters[UNITS], layer_parameters[ACTIVATION])
    layer_init = get_layer_init(layer)
    if layer_name == 'Dropout':
        return layer_init(rate=units)
    return layer_init(units=units, activation=activation)


def build_first_layer(first_layer: Dict[str, Dict[str, Union[str, float]]],
                      input_shape: Tuple[Any, int]):
    first_layer_init: Union[LSTM, Dense, Dropout] = get_layer_init(first_layer)
    first_layer_parameters = first_layer[__get_the_first_key(first_layer)]
    (units, activation) = (first_layer_parameters[UNITS], first_layer_parameters[ACTIVATION])
    return first_layer_init(units=units, activation=activation, input_shape=input_shape)


def __get_the_first_key(layers_dictionary: dict) -> Any:
    return next(iter(layers_dictionary))
