#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LSTM price predictions
Should this be on the price or the cumulative log transform?
@author: bszekely
"""
from sklearn.preprocessing import MinMaxScaler
import krakenex
from pykrakenapi import KrakenAPI
import yfinance as yf
from pandas import DataFrame
import sys
from numpy import isnan, array, mean
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.python.keras.layers import CuDNNLSTM
from tensorflow.keras.models import Sequential
from keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, BatchNormalization, Dropout, Bidirectional
# from keras.models import Sequential
# from keras.utils import Sequence
# from keras.layers import CuDNNLSTM
from time import sleep
import matplotlib.pyplot as plt
SAMPLE_RATE = 1440
SEQ_LEN = 100
DROPOUT = 0.2 #Prevent overfitting
WINDOW_SIZE = SEQ_LEN - 1
BATCH_SIZE = 64
class lstmPrediction():
    def __init__(self):
        print("initialize lstm class")
        api = krakenex.API()
        api.load_key('key.txt')
        self.kraken = KrakenAPI(api)
    def get_ohlc(self,crypt):
        self.data = DataFrame()
        # crypt_name = sys.argv[1] + '-USD'
        crypt_name = crypt + '-USD'
        temp = yf.Ticker(crypt_name)
        self.data = temp.history(period = 'max', interval="1d")
    def preprocess(self):
        close_price_reshape = self.data.Close.values.reshape(-1,1)
        self.scaler = MinMaxScaler()
        self.scaled_data = self.scaler.fit_transform(close_price_reshape)
        self.scaled_data = self.scaled_data[~isnan(self.scaled_data)]
        self.scaled_data = self.scaled_data.reshape(-1,1)
    def split_data(self):
        self.sequences()
        num_train = int(0.95 * self.sequence_data.shape[0])
        self.x_train = self.sequence_data[:num_train,:-1,:]
        self.y_train = self.sequence_data[:num_train,-1,:]
        self.x_test = self.sequence_data[num_train:,:-1,:]
        self.y_test = self.sequence_data[num_train:,-1,:]
    def sequences(self):
        d = []
        for index in range(len(self.scaled_data)-SEQ_LEN):
            d.append(self.scaled_data[index: index + SEQ_LEN])
        self.sequence_data = array(d)
    def machine(self):
        self.model = Sequential()
        self.model.add(Bidirectional(LSTM(WINDOW_SIZE, return_sequences=True),
                                input_shape=(WINDOW_SIZE,self.x_train.shape[-1])))
        self.model.add(Dropout(rate=DROPOUT))
        self.model.add(Bidirectional(LSTM(WINDOW_SIZE*2, return_sequences=True)))
        self.model.add(Dropout(rate=DROPOUT))
        self.model.add(Bidirectional(LSTM(WINDOW_SIZE, return_sequences=False)))
        self.model.add(Dense(units=1))
        self.model.add(Activation('linear'))
        self.model.compile(loss='mean_squared_error',optimizer='adam')
        self.history = self.model.fit(
            self.x_train,
            self.y_train,
            epochs=50,
            batch_size=BATCH_SIZE,
            shuffle=False,
            validation_split=0.1)
        self.model.evaluate(self.x_test,self.y_test)
        self.y_hat = self.model.predict(self.x_test)
        self.y_test_price = self.scaler.inverse_transform(self.y_test)
        self.y_hat_price = self.scaler.inverse_transform(self.y_hat)
    def plot_loss(self):
        plt.plot(self.history.history["loss"])
        plt.plot(self.history.history["val_loss"])
        plt.title("Loss")
        plt.xlabel('epoch')
        plt.ylabel("loss")
        plt.legend(["train","test"])
        plt.show()
    def plot_data(self):
        print(f'length of test: {len(self.y_test_price)}')
        print(f'length of yhat: {len(self.y_hat_price)}')
        mape_error = abs(mean((abs(self.y_test_price - self.y_hat_price) / self.y_test_price) * 100))
        plt.plot(self.y_test_price)
        plt.plot(self.y_hat_price)
        title_name = f"Prediction vs Actual. MAPE: {round(mape_error,4)}"
        plt.title(title_name)
        plt.xlabel('Time')
        plt.ylabel("Price")
        plt.legend(["Test","Prediction"])
        plt.show()
    def run_analysis(self):
        self.get_ohlc(sys.argv[1])
        self.preprocess()
        self.split_data()
        self.machine()
        self.plot_loss()
        self.plot_data()
def main():
    lstmPrediction().run_analysis()
if __name__ == "__main__":
    main()
        