#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble time series forecasters
@author: brianszekely
"""
from ml_with_yfinance import set_crypt_names, set_data, convert_to_panda
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
from numpy import log, exp
import sys
import matplotlib.pyplot as plt
from pandas import DataFrame
from time import sleep
from sklearn.metrics import mean_absolute_percentage_error
from tqdm import tqdm
from warnings import filterwarnings
class ensembleTS():
    def __init__(self):
        print('instantiate ensembleTS object')
    def get_data(self,name):
        self.data = set_data(name)
        print(self.data)
    def transform(self):
        p_val = self.check_statinarity()
        if p_val > 0.05:
            print('Data are non-stationary. transform the data.')
            self.data['Close'] = self.data['Close'].pct_change().fillna(0)
            self.data['Open'] = self.data['Open'].pct_change().fillna(0)
    def ARIMA_model(self):
        #log data before running alg    
        # decomposition = seasonal_decompose(self.data['Close']) 
        model = ARIMA(self.data['Close'], order=(1,1,2))
        model_out = model.fit()
        
        self.data['Close_prediction'] = model_out.predict(start = int(len(self.data['Close'])*.95),
                                                          end= len(self.data['Close']), dynamic= True)
        print(model_out.summary())
        self.data[['Close','Close_prediction']].plot()
        plt.show()
    def tune_arima(self):
        # p_values = [0, 2, 6, 8]
        # d_values = [0,1,2,3]
        # q_values = [0,1,2,3]
        #Don't like the asymmetry
        param_arima = [[0, 0, 0],[0, 0, 1],[0, 0, 2],[0, 0, 3],[0, 1, 0],[0, 1, 1],
         [0, 1, 2],[0, 1, 3],[0, 2, 0],[0, 2, 1],[0, 2, 2],[0, 2, 3],
         [0, 3, 0],[0, 3, 1],[0, 3, 2],[0, 3, 3],[2, 0, 0],[2, 0, 1],
         [2, 0, 2],[2, 0, 3],[2, 1, 0],[2, 1, 1],[2, 1, 2],[2, 1, 3],
         [2, 2, 0],[2, 2, 1],[2, 2, 2],[2, 2, 3],[2, 3, 0],[2, 3, 1], 
         [2, 3, 2],[2, 3, 3],[6, 0, 0],[6, 0, 1],[6, 0, 2],[6, 0, 3],
         [6, 1, 0],[6, 1, 1],[6, 1, 2],[6, 1, 3],[6, 2, 0],[6, 2, 1],
         [6, 2, 2],[6, 2, 3],[6, 3, 0],[6, 3, 1],[6, 3, 2],[6, 3, 3],
         [8, 0, 0],[8, 0, 1],[8, 0, 2],[8, 0, 3],[8, 1, 0],[8, 1, 1],
         [8, 1, 2],[8, 1, 3],[8, 2, 0],[8, 2, 1],[8, 2, 2],[8, 2, 3],
         [8, 3, 0],[8, 3, 1],[8, 3, 2],[8, 3, 3]]
        mape_best = float("inf")
        filterwarnings("ignore")
        for inst in tqdm(param_arima):
            mape = self.error_arima(inst)
            if mape < mape_best:
                mape_best = mape
                arima_save = inst
                print(f'curr best: {mape_best}, with parameters: {arima_save}')
    def error_arima(self,arima_order):
        	# prepare training dataset
        train_size = int(len(self.data['Close']) * 0.98)
        train = self.data['Close'].iloc[0:train_size]
        test = self.data['Close'].iloc[train_size:]
        predict = []
        history = [x for x in train]
        #make predictions
        for inst in range(len(test)):
            model = ARIMA(history, order=arima_order)
            model_fit = model.fit()
            yhat = model_fit.forecast(steps=1)[0]
            predict.append(yhat)
            history.append(test[inst])
        return mean_absolute_percentage_error(test,predict)
    def check_statinarity(self):
        # plot_acf(self.data['Close'].values)
        stationary = adfuller(self.data['Close'].values)
        # plt.show()
        return stationary[1]
    def run_object(self):
        self.get_data(sys.argv[1])
        self.transform()
        self.tune_arima()
        self.ARIMA_model()
def main():
    ensembleTS().run_object()
if __name__ == "__main__":
    main()