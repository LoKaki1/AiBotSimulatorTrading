import numpy as np
import pandas as pd
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.backend import clear_session
from Common import Common as Cm
# from Trading.data_order_something import read_data
import re
from typing import Union
from Trading.yahoo_api import LiveData

TICKER = 'NIO'
X_VALUES = ['open', 'low', 'high', 'close', ]
START = dt.datetime(2020, 4, 15).strftime('%Y-%m-%d')
END = (dt.datetime.now() - dt.timedelta(days=0)).strftime('%Y-%m-%d')
TEST_END = (dt.datetime.now() - dt.timedelta(days=2)).strftime('%Y-%m-%d')
TEST_START = START
PREDICTION_DAYS = 21
UNITS = 50
PREDICTION_DAY = 1
DENSE_UNITS = 0.2
EPOCHS = 12
BATCH_SIZE = 64
PARAMETERS = [EPOCHS, UNITS, PREDICTION_DAYS, PREDICTION_DAY]


def _handle_first_layer(layer, units: Union[str, int], activation: str, input_shape: tuple, index: int):
    return layer(units=units,
                 activation=activation,
                 input_shape=input_shape) if index == 0 else \
        layer(units=units,
              activation=activation,
              )


class ClassifierAi:

    def __init__(self, ticker,
                 prediction_day=None,
                 prediction_days=None,
                 units=None,
                 epochs=None,
                 start_day=START,
                 end_day=END,
                 model_and_its_args=None,
                 daily=True,
                 load_model_from_local=False,
                 new_data=False,
                 load_data_from_local=False,
                 save_model=True,
                 test_start=TEST_START,
                 test_end=TEST_END,
                 other=1,
                 source='IBKR',
                 model_building_blocks=None,
                 use_best_found_settings=False):

        self.ticker = ticker

        self.save_model = save_model
        self.start_day = start_day
        self.end_day = end_day
        self.model_and_its_args = model_and_its_args
        self.daily = daily
        self.load_model_from_local = load_model_from_local
        self.new_data = new_data
        self.load_data_from_local = load_data_from_local
        self.other = str(other)
        self.scalar = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.test_start = test_start
        self.test_end = test_end
        self.real_prices = []
        self.predicted_prices = []
        self.scaled_data = None
        self.source = source
        self.model_building_blocks = model_building_blocks
        self.x_train = []
        self.ratio = None
        self.use_best_settings = use_best_found_settings
        self.last_price = LiveData(ticker).get_live_price() if not self.daily else Cm.get_last_price(ticker)
        if self.use_best_settings:
            self._generate_best_settings_from_file()
            self.prediction_day = 1  # need to work on that when add a support for multiple days on evloution
        else:
            self.epochs, self.units, self.prediction_days, self.prediction_day = self.generate_data(epochs,
                                                                                                    units,
                                                                                                    prediction_days,
                                                                                                    prediction_day)

    def live_last_price(self):
        return LiveData(self.ticker).get_live_price() if not self.daily else Cm.get_last_price(self.ticker)

    def _generate_best_settings_from_file(self):
        print('genrating best settings from file.. ')
        settings, ratio = Cm.best_settings()
        (self.epochs, self.units, self.prediction_days), self.model_building_blocks = list(settings.values())[0:3], {
            'layers':
                settings['layers'],
            'compiler':
                settings['compiler']
        }
        print(self.epochs, self.units, self.prediction_days, self.model_building_blocks, sep=' -> ')

    def generate_data(self, *args):
        json_data = Cm.return_json_data(self.ticker)
        for index, i in enumerate(json_data):
            if args[index] is not None:
                json_data[index] = int(args[index]) if re.match(r'^\d+$', str(args[index])) is not None else i
            if json_data[index] is None:
                json_data[index] = i if i is not None else PARAMETERS[index]
        return json_data

    def fit_data(self):
        """
            func that sets the data to be between 0 and 1 means (40, 10) = (0.123, 0.01) something like that
            :returns the data after fitting it into numbers between 0 and 1
        """
        if self.new_data is False and self.scaled_data is not None:
            return self.scaled_data()
        train_data = self.get_data()
        """ Making data without lists because scaled data cant
         use lists so data before = [[1, 2, 3, ...], [2, 3, 4, ...] ...] data after = [1, 2, 3, 2, 3, 4 ...] """

        data = np.array([t for i in train_data
                         for t in i]).reshape(-1, 1)

        "Reshape so it matches with scalar api"
        self.scalar = MinMaxScaler(feature_range=(0, 1))
        """ Fits x values of data (now it makes the real values ) """

        self.scaled_data = self.scalar.fit_transform(data)
        print('I fit data :)')
        return self.scaled_data

    def _get_data_from_interactive(self):
        return Cm.iterate_data(
            Cm.read_csv(f'../Trading/Historical_data/{self.ticker}.csv',
                        self.ticker, other=self.other))

    def get_data(self):
        """
        :return: Historical data of a stock and divide it into lists that each contains [open, close, high, low]
        """
        if self.daily:
            return Cm.iterate_data(Cm.get_historical_data(self.ticker, self.start_day, self.end_day))

        elif self.load_data_from_local:
            "Means it's not daily but also load from local (no way to get daily from local, meanwhile)"
            # source to choose whether you want ibkr or yahoo, ibkr contains premarket, Yahoo does not
            if self.source == 'IBKR':
                return self._get_data_from_interactive()
            try:
                return Cm.get_data_from_file_or_yahoo(self.ticker)
            except SyntaxError:
                return self._get_data_from_interactive()

        else:
            if self.source == 'IBKR':
                read_data(self.ticker, self.other)
                return self._get_data_from_interactive()
            try:
                return Cm.intraday_with_yahoo(self.ticker, self.other)
            except [Exception]:
                read_data(self.ticker, self.other)
                return self._get_data_from_interactive()

    def prepare_data(self, scaled_data):
        """ func to prepare data that in x_train it contains prediction_days values and in y_train the predicted
        price """
        x_train = []
        y_train = []
        print('prepare data :)..')
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
            y_train.append(scaled_data[x + 3: x + (self.prediction_day * length_const) + 3: length_const, 0][-1])
        """ Reshape the arrays that
        x_train.shape[0] = length of big array 

        x_train[n] = [x_train[n][0], x_train[n][1], ... x_train[n][prediction_days]]"""
        Cm.check_data(x_train, y_train, self.prediction_day)
        x_train, y_train = np.array(x_train), np.array(y_train).reshape(-1, 1)
        """  x_train.shape[0] = the length of the array, x_train.shape[1] =  prediction days 
         means to create a shape with length of x_train.len and width of prediction days on one dimension
        """
        self.x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        self.x_train = x_train
        return x_train, y_train

    def generate_fit_and_prepare_data(self):
        scaled_data = self.fit_data()
        if self.load_model_from_local and Cm.load_model_from_file(self) is not None:
            return scaled_data, None, None
        x_train, y_train = self.prepare_data(scaled_data=scaled_data)
        return scaled_data, x_train, y_train

    def preparation_for_machine(self):
        if self.load_model_from_local and Cm.load_model_from_file(self) \
                is not None and self.model_and_its_args is not None:
            return self.model_and_its_args
        self.scaled_data, x_train, y_train = self.generate_fit_and_prepare_data()

        self.model = model = self.build_model(x_train, y_train, )
        return model, self.scaled_data

    def build_model(self,
                    x_train,
                    y_train,
                    ):
        """ Build Model """
        """ Clear session """
        clear_session()

        """ Building The Model """
        if (self.load_model_from_local and (model := Cm.load_model_from_file(self))
                is not None):
            print('loading model from file..')
            return model
        if self.model is not None:
            print('No need to rebuild model :)')
            return self.model
        """ Last model was like this  (took more time but did the job not perfect)"""
        """Add layer with dropout that has dense_units with 0.2"""
        """ Add LSTM layer that is a short cut for layer short term memory which contains the data in the stm :) """
        # Create a blank model with 4 layers that each contains number of units which is the neurons of each layer
        if self.model_building_blocks is None:
            print(f'using the default model with  {self.epochs=} {self.units=}'
                  f' {self.prediction_days=} {self.prediction_day=}')
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
                Dropout(0.2),
                LSTM(50, return_sequences=True),
                Dropout(0.2),
                Dense(1)
            ])
            """ Returns only one value """

            model.compile(optimizer='adam', loss='mean_squared_error', )
            """ Fitting x_train to y_train, that makes
             a function that has x values and y values 
              example:  
                    x_train =  (23, 24, 25, 26, 123123 ... * (prediction_days)) * all_data
                    y_train = (1) ...* all_data - create a func that x[n] = y[n] for n in index   """
        else:
            layer_dict = {'Dense': Dense, 'LSTM': LSTM, 'Dropout': Dropout}
            model_list = []
            for index, layer in enumerate(self.model_building_blocks['layers']):
                layer_data = self.model_building_blocks['layers'][index]
                layer_t = list(layer_data.keys())[0]
                layer_data = self.model_building_blocks['layers'][index][layer_t]
                if not index or layer_t == 'Dense':
                    weights = _handle_first_layer(
                        layer=layer_dict['Dense'],
                        units=layer_data['units'],
                        activation=layer_data['activation'],
                        input_shape=(x_train.shape[1], 1),
                        index=index)
                elif layer_t == 'LSTM':
                    weights = LSTM(units=layer_data['units'], return_sequences=True)
                else:
                    weights = Dropout(rate=layer_data['units'])
                model_list.append(weights)
            if (new := Dense(units=1, activation='linear')) not in model_list:
                model_list.append(new)
            model = Sequential(model_list)
            model.compile(optimizer=(co := self.model_building_blocks['compiler'])['optimizer'],
                          loss=co['loss'],
                          )

        model.summary()
        model.fit(x_train, y_train,
                  epochs=self.epochs, batch_size=BATCH_SIZE, shuffle=False, verbose='auto', )

        if self.save_model:
            model.save(f'saved_model/{self.ticker}_model/'
                       f'{self.epochs}'
                       f'-{self.units}'
                       f'-{self.prediction_days}'
                       f'-{self.prediction_day}')
        self.model = model
        return model

    def predict_data(self, scaled_data):
        """ Setting model inputs to be equal to scaled data...
            reason for that is because I want to use the same training data to
            prediction data which makes the neural network gets smarter every day, because it uses new data
        """
        model_inputs = scaled_data
        """
        real_data = last prediction_days values of scaled data 
        """
        real_data = [model_inputs[len(model_inputs) -
                                  self.prediction_days * len(X_VALUES): len(model_inputs) + self.prediction_day, 0]]
        real_data = np.array(real_data)
        real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
        """ After we took the last prediction_days values, we give this x value 
        to predict function and returns the next value according
         to their value and the func it creates in the fit method """
        try:
            prediction = self.model.predict(real_data)
        except ValueError:
            raise ValueError("One of the parameters change please delete the last model or change the flag that won't "
                             "take the last model")
        try:
            prediction = self.scalar.inverse_transform(prediction)
        except ValueError as error:
            print(f'error ocured{error}')
            prediction = self.scalar.inverse_transform(
                np.reshape(
                    prediction, (real_data.shape[0], real_data.shape[1], 1)).reshape(-1, 1))
        return prediction

    def predict_stock_price_at_specific_day(self, print_ca=False):
        """ return predicted stock price in a specific day

            param
                ticker: name of the stock you predict
                prediction_day: what day from you predict
                prediction_days: how many days each prediction is based on
                units: how many units it based on
                dense_units: kill me now
                epochs: how many times it moves on the data
                start_day: from what day you want the data to be based on
                    each day y i


        """

        self.model_and_its_args = model, scaled_data, = self.preparation_for_machine()

        price = self.predict_data(scaled_data)
        if self.daily:
            end_day_predicted = (dt.datetime.strptime(
                self.end_day, '%Y-%m-%d') + dt.timedelta(days=(
                self.prediction_day if float(
                    dt.datetime.now().strftime(
                        '%H')) < 11 else self.prediction_day - 1))).strftime('%Y-%m-%d')
        else:
            end_day_predicted = dt.datetime.now() + dt.timedelta(minutes=self.prediction_day)
        Cm.write_in_file('prediction.txt', ''.join(['\n', (price := str(price[-1][-1])), ' ', str(end_day_predicted)]))
        if print_ca:
            # Make sure that print function is on my variables :)
            print_ca = print
            print_ca(f"The price is -> {price}", )
        return float(price)

    def return_test_data(self, ):
        test_data_time = (dt.datetime.strptime(self.test_start, '%Y-%m-%d') -
                          dt.timedelta(days=self.prediction_days)).strftime('%Y-%m-%d')
        self.test_start = test_data_time
        test_data = pd.DataFrame(self.get_data()).values
        actual_data = []
        model_inputs = test_data.reshape(-1, 1)
        x_test = []
        length = len(X_VALUES)
        delta = length * self.prediction_days
        model_inputs = self.scalar.transform(model_inputs)

        for i in range(delta, len(model_inputs) - ((self.prediction_day - 1) * length), length):
            x_test.append(model_inputs[i - delta: i, 0])
            actual_data.append(model_inputs[i - 6: i - 6 + (self.prediction_day * length): length, 0][0])
        return x_test, actual_data

    def test_model_func(self):
        """ Test Model
        This part is seeing how accuracy the model on a data that exists but wasn't on it's training"""
        x_test, actual_data = self.return_test_data()

        x_test = np.array(x_test)
        print('test model..')
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        actual_data = np.array(actual_data).reshape(-1, 1)
        actual_data = self.scalar.inverse_transform(actual_data)
        predicted_prices = self.model.predict(x_test)

        predicted_prices = [t for t in [self.scalar.inverse_transform(
            predicted_prices[i].reshape(
                -1, 1)) for i, _ in enumerate(
            predicted_prices)]]

        """ Check len of data is same in both of them """
        if len(predicted_prices) == len(actual_data):
            print_tf = print
            print_tf('test data is cool :)')

        self.predicted_prices, self.real_prices = np.array([i[-1] for i in predicted_prices]), actual_data
        return self.predicted_prices, self.real_prices

    def test_model(self):
        """
        function to test the model by making
        prediction on existing data that wasn't given for the model,
        it returns the real values of those days and the predicted values
        each prediction is predicted by the model and giving the model the x value which is the
        prediction_days before that day

        For example -
            prices = [1, 2, ... prediction_days]
            predicted_price = model.predict(prices)
        :returns -
            predicted_prices = [[first] [second]...[last]]
            actual_prices = [[first]
                             [second]
                              ...
                              [last]]
        """

        self.model_and_its_args = self.preparation_for_machine()
        return self.test_model_func()

    def build_model_for_multiple_prediction(self):
        """
        function to create model for multiple predictions the model here
         is automatically false because we can't create model from model
        """

        self.model_and_its_args = self.preparation_for_machine()
        return self.model_and_its_args

    def plot_two_graphs(self):
        """ func to graph the predicted prices vs the real prices of a stock,
            that way you can see visually how accuracy the model is :)
        """
        if len(self.predicted_prices) or len(self.real_prices):
            self.test_model()
        predicted_prices = np.array(self.predicted_prices) if self.predicted_prices is list else self.predicted_prices
        real_prices = np.array(self.real_prices) if self.real_prices is list else self.real_prices
        Cm.plot(predicted_prices, real_prices, self.ticker)

    def accuracy_ratio(self, ):
        try:
            self.ratio = sum([min(t / self.real_prices[i],
                                  self.real_prices[i] / t)
                              for i, t in enumerate(self.predicted_prices)]) / len(self.predicted_prices) \
                if self.ratio is None else self.ratio
            return self.ratio
        except ZeroDivisionError:
            raise ValueError("Not using the accuracy_ratio correctly run test_model before or run "
                             "test_model_and_return_accuracy_ratio() instead")

    def test_model_and_return_accuracy_ratio(self, ):
        if self.ratio is not None:
            return self.ratio
        self.test_model()
        return self.accuracy_ratio()[-1]

    def get_settings(self):
        return {'epochs': self.epochs,
                'units': self.units,
                'prediction_days': self.prediction_days,
                'prediction_day': self.prediction_day}

    def predict_price(self, **options):
        """
            :returns -
                (predicted_price, last_price, change, presnaage_change, **optional: accuracy_ratio)
        """
        data = {'predicted_price': (pp := self.predict_stock_price_at_specific_day()),
                'last_price': (lp := self.live_last_price()),
                'change': (change := pp - lp),
                'change_presentage': change / lp * 100}
        if options.get('ratio', False):
            data['ratio'] = self.test_model_and_return_accuracy_ratio()
        return data


def main():
    ticker = 'NIO'
    my_man = ClassifierAi(ticker, epochs=28, units=57, prediction_days=14, load_model_from_local=False,
                          use_best_found_settings=False)
    my_man.predict_stock_price_at_specific_day(True)
    print(my_man.test_model_and_return_accuracy_ratio())


if __name__ == '__main__':
    main()
