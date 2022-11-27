#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LSTM price predictions
Should this be on the price or the cumulative log transform?
@author: bszekely
"""
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import krakenex
from pykrakenapi import KrakenAPI
import yfinance as yf
from pandas import DataFrame, to_datetime, date_range, Timedelta
import sys
import os
from numpy import isnan, array, mean, nan, log2, column_stack
import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.python.keras.layers import CuDNNLSTM
from tensorflow.keras.models import Sequential
from keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, BatchNormalization, Dropout, Bidirectional
# from keras.models import Sequential
# from keras.utils import Sequence
# from keras.layers import CuDNNLSTM
from time import sleep
import matplotlib.pyplot as plt
# from fitter import Fitter
"""
TODO: add more features: volume, close price, opem, close, and maybe technical
indicators like RSI/
"""
SAMPLE_RATE = 1440
DROPOUT = 0.2 #Prevent overfitting
LOOKBACK = 60
FORECAST = 7
WINDOW_SIZE = FORECAST - 1
BATCH_SIZE = 32
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
        print('yahoo price data: ',self.data)
    def preprocess(self):
        #get features
        self.features = ['Close','High']
        self.input_data = self.data[self.features]#.values.reshape(-1,1)
        # volume_reshape = self.data.Volume.values.reshape(-1,1)
        #min max scale
        self.scaler1 = MinMaxScaler()
        # self.scaler2 = MinMaxScaler()
        self.input_data[self.features[0]] = self.input_data[self.features[0]].pct_change() #normalization
        self.input_data[self.features[0]] = self.input_data[self.features[0]].bfill()
        self.scaled_price = self.input_data[self.features[0]].to_numpy().reshape(-1, 1) #No scaling
        # self.scaled_price = self.scaler1.fit_transform(self.input_data[self.features[0]].to_numpy().reshape(-1, 1)) #Scale
        # self.scaled_volume = self.scaler2.fit_transform(self.input_data[features[1]].to_numpy().reshape(-1, 1))
        # self.scaled_data = column_stack((self.scaled_price,self.scaled_volume))
        self.scaled_data = self.scaled_price[~isnan(self.scaled_price)] 
        self.scaled_data = self.scaled_data.reshape(-1,1)
        #standard scale
        # self.scaler = FunctionTransformer(log2,validate=True)
        # self.scaled_data = self.scaler.fit_transform(close_price_reshape)
        # self.scaled_data = self.scaled_data[~isnan(self.scaled_data)]
        # self.scaled_data = self.scaled_data.reshape(-1,1)
        # #log transform scale
        # self.scaled_data_log = log(close_price_reshape)
        # self.scaled_data_log = self.scaled_data_log[~isnan(self.scaled_data_log)]
        # self.scaled_data_log = self.scaled_data_log.reshape(-1,1)
        # find_hist = Fitter(close_price_reshape)
        # find_hist.fit()
        # print(find_hist.get_best(method='ks_pvalue'))
        # plt.figure()
        # find_hist.summary()
        # plt.show()
        # plt.legend(['minMax','l2','log2'])
    def split_data(self):
        self.sequences()
        # num_train = int(0.95 * self.sequence_data.shape[0])
        # self.x_train = self.sequence_data[:num_train,:-1,:]
        # self.y_train = self.sequence_data[:num_train,-1,:]
        # self.x_test = self.sequence_data[num_train:,:-1,:]
        # self.y_test = self.sequence_data[num_train:,-1,:]
    def sequences(self):
        X = []
        Y = []
        for i in range(LOOKBACK, len(self.scaled_data) - FORECAST + 1):
            X.append(self.scaled_data[i - LOOKBACK: i, 0:self.input_data.shape[1]])
            Y.append(self.scaled_data[  i+FORECAST-1:i+FORECAST,0]) #may need to change idx to [i+future-1:i+future,0]
        self.x_train = array(X)
        self.y_train = array(Y) 
        print(self.x_train.shape)
        print(self.y_train.shape)
        # d = []
        # for index in range(len(self.scaled_data)-SEQ_LEN):
        #     d.append(self.scaled_data[index: index + SEQ_LEN])
        # self.sequence_data = array(d)
    def machine(self):
        self.model = Sequential()
        #LSTM
        # self.model.add((LSTM(units=30, return_sequences=True, activation='relu', input_shape=(LOOKBACK, self.x_train.shape[-1]))))
        self.model.add(LSTM(units=10, return_sequences=True, activation='relu', input_shape=(self.x_train.shape[1], self.x_train.shape[2])))
        self.model.add(Dropout(rate=DROPOUT))
        self.model.add((LSTM(units=10,activation='softmax',return_sequences=True)))
        # self.model.add(Dropout(rate=DROPOUT))
        # self.model.add((LSTM(units=10, activation='relu',return_sequences=True)))
        # self.model.add(Dropout(rate=DROPOUT))
        # self.model.add((LSTM(units=5, activation='relu',return_sequences=True)))
        # self.model.add(Dropout(rate=DROPOUT))
        # self.model.add((LSTM(units=5, activation='relu')))
        self.model.add(Dropout(rate=DROPOUT))
        self.model.add(Dense(FORECAST))
        # self.model.add(Activation('softmax'))
        self.model.compile(loss='mse',optimizer='adam',metrics=[tf.keras.metrics.RootMeanSquaredError()])
        es = tf.keras.callbacks.EarlyStopping(monitor='loss',patience=10,restore_best_weights=True)
        self.model.summary()
        print(f'length of data: {self.x_train.shape}. Make sure the num of parameters is not larger than samples')
        self.history = self.model.fit(
            self.x_train,
            self.y_train,
            epochs=50,
            batch_size=BATCH_SIZE,
            shuffle=False,
            validation_split=0.1,
            callbacks=[es])
        #Predict Forecast
        X_ = self.scaled_data[-LOOKBACK:]  # last available input sequence
        # X_ = X_.reshape(1, LOOKBACK, 1)
        X_ = X_.reshape(1, self.x_train.shape[1],self.x_train.shape[2])
        self.Y_ = self.model.predict(X_).reshape(-1, 1)
        # self.Y_ = self.scaler1.inverse_transform(self.Y_) #inverse transform back if MinMaxScaler is used
        # print(self.Y_.flatten())
        # self.Y_ = 2**self.Y_
        # self.model.evaluate(self.x_test,self.y_test)
        # self.y_hat = self.model.predict(self.x_test)
        # self.y_test_price = self.scaler.inverse_transform(self.y_test)
        # self.y_hat_price = self.scaler.inverse_transform(self.y_hat)
    def plot_loss(self):
        plt.plot(self.history.history["loss"])
        plt.plot(self.history.history["val_loss"])
        plt.title("Loss")
        plt.xlabel('epoch')
        plt.ylabel("loss")
        plt.legend(["train","test"])
        plt.show()
    def plot_data(self):
        # organize the results in a data frame
        df_past = self.input_data
        # df_past = self.data[['Close']].reset_index()
        # df_past['Close'] = df_past['Close'].pct_change()
        df_past.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
        df_past.drop(columns=[self.features[1]],inplace=True)
        df_past['Date'] = to_datetime(df_past.index)
        df_past['Forecast'] = nan
        df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1]
        #Future
        df_future = DataFrame(columns=['Date', 'Actual', 'Forecast'])
        df_future['Date'] = date_range(start=df_past['Date'].iloc[-1] + Timedelta(days=1), periods=FORECAST)
        print(self.Y_.flatten())
        offset = int(input('10 or 100?'))
        df_future['Forecast'] = self.Y_.flatten() * offset
        df_future['Actual'] = nan
        results = df_past.append(df_future).set_index('Date')
        csv_save = f"{sys.argv[1]}_future_lstm.csv"
        # results.drop(index=results.index[-1],axis=0,inplace=True) 
        print(results)
        results.to_csv(os.path.join(os.getcwd(),'lstm_data',csv_save))
        ax = results.plot()
        ax.set_ylabel('Close Price pct change ($)')
        ax.set_xlabel('Date')
        plt.show()
        self.save_forecast = results
        # print(f'length of test: {len(self.y_test_price)}')
        # print(f'length of yhat: {len(self.y_hat_price)}')
        # mape_error = abs(mean((abs(self.y_test_price - self.y_hat_price) / self.y_test_price) * 100))
        # plt.plot(self.y_test_price)
        # plt.plot(self.y_hat_price)
        # title_name = f"Prediction vs Actual. MAPE: {round(mape_error,4)}"
        # plt.title(title_name)
        # plt.xlabel('Time')
        # plt.ylabel("Price")
        # plt.legend(["Test","Prediction"])
        # plt.show()
    def convert_pct_change_to_price(self):
        close_data = self.data.Close
        fore_pct_change = self.save_forecast['Forecast'].dropna()
        save_predicted_price = []
        for i in range(len(fore_pct_change)):
            if i == 0:
                temp = close_data.iloc[-1] 
                print(f'zero start: {temp + (temp * fore_pct_change[i])}, {fore_pct_change[i]}')
                save_predicted_price.append(temp + (temp * fore_pct_change[i]))
            else:
                print(f'zero start: {save_predicted_price[i-1]}')
                save_predicted_price.append(save_predicted_price[i-1] + (save_predicted_price[i-1] * fore_pct_change[i]))
        plt.plot(self.data.index,self.data.Close,marker="o")
        plt.plot(fore_pct_change.index,save_predicted_price,marker="o"  )
        plt.show()
                
    def run_analysis(self):
        self.get_ohlc(sys.argv[1])
        self.preprocess()
        self.split_data()
        self.machine()
        self.plot_loss()
        self.plot_data()
        self.convert_pct_change_to_price()
def main():
    lstmPrediction().run_analysis()
if __name__ == "__main__":
    main()  