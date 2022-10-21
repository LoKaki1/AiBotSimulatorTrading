import datetime as dt

from Common.Constants.FormatConstants import DATE_FORMAT
from Common.DataCommon import ModelDataHandler

START = dt.datetime(2020, 7, 1).strftime(DATE_FORMAT)
END = (dt.datetime.now() - dt.timedelta(days=0)).strftime(DATE_FORMAT)
TEST_END = (dt.datetime.now() - dt.timedelta(days=2)).strftime(DATE_FORMAT)
TEST_START = START
X_VALUES = ModelDataHandler.X_VALUES
DEFAULT_PREDICTION_DAY = 1
DEFAULT_PREDICTION_DAYS = 21
DEFAULT_EPOCHS = 25
DEFAULT_UNITS = 50
DROPOUT_UNITS = 0.2
BATCH_SIZE = 32
OPEN_PREDICTION = 0
LOW_PREDICTION = 1
HIGH_PREDICTION = 2
CLOSE_PREDICTION = 3
UNITS = 'units'
EPOCHS = 'epochs'
ACTIVATION = 'activation'
PREDICTION_DAYS = 'prediction_days'
MODEL_PARAMETERS = {
  "epochs": 28,
  "units": 57,
  "prediction_days": 14,
  "layers": [
    {
      "Dense": {
        "units": 57,
        "activation": "tanh"
      }
    },
    {
      "Dense": {
        "units": 25,
        "activation": "relu"
      }
    },
    {
      "Dropout": {
        "units": 0.2,
        "activation": "softsign"
      }
    },
    {
      "LSTM": {
        "units": 7,
        "activation": "relu"
      }
    }
  ]
}