import yfinance as yf
import datetime
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from finta import TA
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout

"""
Defining some constants for data mining
"""

symbol = 'MSFT'      # Symbol of the desired stock
data_1 = yf.download(symbol, start='2021-01-01', end='2022-05-03', interval="1d")

fig = go.Figure(data=[go.Candlestick(x=data_1.index,
                open=data_1['Open'],
                high=data_1['High'],
                low=data_1['Low'],
                close=data_1['Close'])])


training_set = data_1.iloc[:,1:2].values
scaler = MinMaxScaler(feature_range=(0,1))
scaled_training_set = scaler.fit_transform(training_set)

x_train = []
y_train = []


for i in range(60, 335):
    x_train.append(scaled_training_set[i-60:i, 0])
    y_train.append(scaled_training_set[i, 0])

x_train = np.array(x_train)
y_train = np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

regressor = Sequential()

regressor.add(LSTM(units= 50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units= 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units= 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units= 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units= 1))

regressor.compile(optimizer="adam", loss= "mean_squared_error")
regressor.fit(x_train, y_train, epochs= 20, batch_size= 12)


dataset_test = yf.download(symbol, start='2022-05-04', end='2022-12-03', interval="1d")

actual_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((data_1["Open"], dataset_test["Open"]), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test)-60: 0].values

inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)

x_test = []
for i in range(60, 80):
    x_test.append(inputs[i-60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test.shape[0], x_test.shape[1], 1)

predicted_stock_price = regressor.predict(x_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)


plt.plot(actual_stock_price, color = "red", label = "Actual")
plt.plot(predicted_stock_price, color = "blue", label = "Prediction")
plt.title("Stock price prediction")
plt.xlabel("Time")
plt.ylabel("Stock price")
plt.legend()