import time
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from dateutil.relativedelta import relativedelta


class MLP:
    def __init__(self, df, n_steps):
        # define 'n_steps' as the size of each training group
        self.df = df
        self.n_steps = n_steps
        self.future_months = []  # recorded months of predictions in the future
        self.predictions = []  # predicted numbers of sunspots

    # split a training dataset into groups with size of 'n_steps'
    def create_training_set(self, dataset):
        x, y = list(), list()
        for i in range(len(dataset)):
            # find the final index of this group
            end_index = i + self.n_steps
            # break the loop if end_index reaches the final element
            if end_index > len(dataset) - 1:
                break
            # each group has 'steps' input data followed by one output data
            # the output data will be the last input data in the next group
            x_train, y_train = dataset[i:end_index], dataset[end_index]
            x.append(x_train)
            y.append(y_train)
        return np.array(x), np.array(y)

    def mlp_predict(self, x_train, y_train, n_months):
        start_t = time.time()
        for i in range(n_months):
            # build an MLP model with input dimension 'n_steps'
            model = Sequential()
            model.add(Dense(100, activation='relu', input_dim=self.n_steps))
            model.add(Dense(100, activation='relu'))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mse')
            # fit MLP model with 10% validation data
            model.fit(x_train, y_train, verbose=0, validation_split=0.1)
            # append the last training group and the last output data
            # as the new testing group for prediction
            x_test = np.append(x_train[-1][1:self.n_steps], y_train[-1])
            x_test = x_test.reshape((1, self.n_steps))
            # predict the number of sunspots in the next month
            y_test = np.round(model.predict(x_test, verbose=0), 2)
            x_train = np.vstack([x_train, x_test])
            y_train = np.append(y_train, y_test)
            # demonstrate prediction with its datetime
            if self.future_months:
                new_month = self.future_months[-1] + relativedelta(months=1)
            else:
                new_month = self.df['Month'].to_list()[-1] + relativedelta(months=1)
            print('The predicted number of sunspots at', new_month,
                  'will be:', y_test[0][0])
            self.future_months.append(new_month)
            self.predictions.append(y_test[0][0])
        print('Time consumed for MLP training and predicting:',
              round(time.time() - start_t, 2), 's')
        return round(self.predictions[-1], 2)

    def plot_predictions(self):
        # plot the existing dataset and predictions for the future
        plt.plot(self.df['Month'], self.df['Sunspots'], label='Existing data')
        plt.plot(self.future_months, self.predictions, label='Predicted data')
        plt.xlabel('Date')
        plt.ylabel('Number of Sunspots')
        plt.legend(loc='best')
        plt.show()
