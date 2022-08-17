import datetime as dt
import numpy as np
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.backend import clear_session
from Common.DataCommon import ModelDataHandler
from Logger import Logger
from PredictingData.Logs import MachineLogs

""" My Constants """

START = dt.datetime(2020, 4, 15).strftime('%Y-%m-%d')
END = (dt.datetime.now() - dt.timedelta(days=0)).strftime('%Y-%m-%d')
TEST_END = (dt.datetime.now() - dt.timedelta(days=2)).strftime('%Y-%m-%d')
TEST_START = START
X_VALUES = ModelDataHandler.X_VALUES
PREDICTION_DAY = 1
PREDICTION_DAYS = 21
EPOCHS = 25
UNITS = 50
DROPOUT_UNITS = 0.2
BATCH_SIZE = 32
OPEN_PREDICTION = 0
LOW_PREDICTION = 1
HIGH_PREDICTION = 2
CLOSE_PREDICTION = 3

""" Model """


class StockPrediction:

    def __init__(self, ticker):
        self.scalar = None
        self.ticker = ticker
        self.start = START
        self.end = END
        self.test_start = TEST_START
        self.test_end = TEST_END
        self.prediction_day = PREDICTION_DAY
        self.prediction_days = PREDICTION_DAYS
        self.epochs = EPOCHS
        self.units = UNITS
        self.batch_size = BATCH_SIZE
        self.predict_constant = CLOSE_PREDICTION
        self.model = None

    def get_data_for_fitting(self):
        """
        :return: Historical data of a stock and divide it into lists that each
         contains [[open, close, high, low], [...], ...]
        """
        return ModelDataHandler.get_historical_data(self.ticker, self.start, self.end)

    def scale_data(self, one_array_data_to_train: list):
        """
            func that sets the data to be between 0 and 1 means (40, 10) = (0.123, 0.01) something like that
            :returns the data after fitting it into numbers between 0 and 1
        """
        """ Making data without lists because scaled data cant
         use lists so data before = [[1, 2, 3, ...], [2, 3, 4, ...] ...] data after = [1, 2, 3, 2, 3, 4 ...] """

        data = np.array(one_array_data_to_train).reshape(-1, 1)

        "Reshape so it matches with scalar api"
        self.scalar = MinMaxScaler(feature_range=(0, 1))
        """ Fits x values of data (now it makes the real values ) """

        scaled_data = self.scalar.fit_transform(data)
        Logger.info('finish fitting data to scalar 😀')
        return scaled_data

    def build_data(self):
        plain_data = self.get_data_for_fitting()
        one_array_data = ModelDataHandler.one_array_data(plain_data)
        scaled_data = self.scale_data(one_array_data)
        return scaled_data

    def prepare_data_for_model(self, scaled_data):
        """
         func to prepare data that in x_train it contains prediction_days values and in y_train the predicted
        :param scaled_data:
        :return: x_train data set that prediction_days number * candle found in its cell of the array and in the
        same index in y_train found the number we try to predict
        """
        x_train = []
        y_train = []
        delta = len(X_VALUES) * self.prediction_days
        length_const = len(X_VALUES)
        """ Means to start counting from prediction_days index 'til the end """
        for x in range(delta, len(scaled_data) - ((self.prediction_day - 1) * length_const), length_const):
            """ x_train[0] = array[scaled_data[0], scaled_data[1], ... scaled_data[prediction_days]]
                x_train[1] = array[scaled_data[1], scaled_data[2], ... scaled_data[prediction_days + 1]]
                ...
                x_train[n] = array[scaled_data[n], scaled_data[n + 1] ... scaled_data[prediction_days + n] 

                we make the x_train data that for each y value there
                 prediction days values that it can base its prediction on
            """

            x_train.append(scaled_data[x - delta: x, 0])
            """ Remember I changed to discover open to match test model + 0 = open + 1 = low + 2 = high + 3 = close"""
            y_train.append(scaled_data[x + self.predict_constant:
                                       x + (self.prediction_day * length_const) + self.predict_constant:
                                       length_const, 0][-1])
        """ Reshape the arrays that
        x_train.shape[0] = length of big array 

        x_train[n] = [x_train[n][0], x_train[n][1], ... x_train[n][prediction_days]]"""
        return x_train, y_train

    def build_model_layers(self, x_train) -> Sequential:
        """ Build Model """
        """ Clear session """
        clear_session()
        model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=(x_train.shape[1], 1)),
            Dropout(DROPOUT_UNITS),
            LSTM(self.units, return_sequences=True),
            Dropout(DROPOUT_UNITS),
            Dense(self.prediction_day)
        ])
        # In the future please put the logs in different file
        Logger.info(MachineLogs.BUILD_MODEL_LAYERS)
        model.summary()
        return model

    def fit_model_x_y_trains(self, x_train: np.ndarray, y_train: np.ndarray, model: Sequential):
        model.fit(x_train, y_train,
                  epochs=self.epochs, batch_size=self.batch_size)
        Logger.info(MachineLogs.MODEL_FITTED)
        return model

    def build_model_for_prediction(self, scaled_data):
        if self.model is not None:
            return
        x_train, y_train = self.prepare_data_for_model(scaled_data)
        ModelDataHandler.check_prepared_data_for_model(x_train, y_train, self.prediction_day)
        x_train, y_train = ModelDataHandler.reshape_trains(x_train, y_train)
        model_before_fitting = self.build_model_layers(x_train)
        self.model = self.fit_model_x_y_trains(x_train, y_train, model_before_fitting)

    def _get_last_part_of_scaled_data(self, model_inputs):
        data_to_make_on_prediction = [model_inputs[len(model_inputs) -
                                                   self.prediction_days * len(X_VALUES): len(
                                                    model_inputs) + self.prediction_day, 0]]
        data_to_make_on_prediction = np.reshape((np_data := np.array(data_to_make_on_prediction)),
                                                (np_data.shape[0],
                                                 np_data.shape[1], 1))
        return data_to_make_on_prediction

    def predict_data_on_scaled_data(self, data_to_make_on_prediction):
        try:
            prediction_data_result = self.model.predict(data_to_make_on_prediction)
        except ValueError:
            raise ValueError(MachineLogs.VALUE_ERRPR_IN_PREDICTION)
        return prediction_data_result

    def inverse_scalar_prediction_result(self, prediction_data_result):
        try:
            prediction = self.scalar.inverse_transform(prediction_data_result)
        except ValueError as error:
            Logger.error(MachineLogs.INVERSING_SCALAR_ERROR.format(error=error))
            prediction = self.scalar.inverse_transform(
                np.reshape(
                    prediction_data_result, (prediction_data_result.shape[0],
                                             prediction_data_result.shape[1], 1)).reshape(-1, 1))
        return prediction

    def predict_data(self, model_inputs):
        """ Setting model inputs to be equal to scaled data...
            reason for that is because I want to use the same training data to
            prediction data which makes the neural network gets smarter every day, because it uses new data
        """
        data_to_make_on_prediction = self._get_last_part_of_scaled_data(model_inputs)
        """
        real_data = last prediction_days values of scaled data 
        """
        prediction_data_result = self.predict_data_on_scaled_data(data_to_make_on_prediction)
        """ After we took the last prediction_days values, we give this x value 
        to predict function and returns the next value according
         to their value and the func it creates in the fit method 
         """
        predicted_data_inverse_transform_result = self.inverse_scalar_prediction_result(prediction_data_result)
        """ data inversed """
        return predicted_data_inverse_transform_result

    def predict_next_price(self):
        scaled_data = self.build_data()
        self.build_model_for_prediction(scaled_data)
        predicted_price = self.predict_data(scaled_data)
        return predicted_price

    def generate_test_model_input(self):
        test_data = ModelDataHandler.get_data_from_yahoo(self.ticker, self.test_start, self.test_end)
        return self.scalar.transform(test_data.reshape(-1, 1))

    def get_test_data(self):
        model_inputs = self.generate_test_model_input()
        actual_data = []
        x_test = []
        length = len(X_VALUES)
        delta = length * self.prediction_days
        for i in range(delta, len(model_inputs) - ((self.prediction_day - 1) * length), length):
            x_test.append(model_inputs[i - delta: i, 0])
            actual_data.append(model_inputs[i - self.predict_constant * 2: i - self.predict_constant * 2 + (
                    self.prediction_day * length): length, 0][0])
        x_test, actual_data = ModelDataHandler.reshape_trains(x_test, actual_data)
        return x_test, actual_data

    def test_model(self):
        """ Test Model
        This part is seeing how accuracy the model on a data that exists but wasn't on it's training"""
        x_test, actual_data = self.get_test_data()
        actual_data = self.scalar.inverse_transform(actual_data)
        predicted_prices = self.model.predict(x_test)

        """ Check len of data is same in both of them """
        self.scalar.inverse_transform(predicted_prices), actual_data
        return predicted_prices, actual_data


def main():
    ticker = 'NIO'
    stock_prediction = StockPrediction(ticker)
    print(stock_prediction.predict_next_price())

if __name__ == '__main__':
    main()
