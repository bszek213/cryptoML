#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble time series forecasters
@author: brianszekely
Run analysis on these cryptos: BTC, ETH, DOGE, LTC, TRON, LINK, BCH, MANA, RLC
"""
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_predict
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
from prophet_forecast import set_data
from numpy import log, exp
import matplotlib.pyplot as plt
from pandas import DataFrame
from time import sleep
from sklearn.metrics import mean_squared_error
from tqdm import tqdm
from warnings import filterwarnings
from sys import argv
from itertools import product
class ensembleTS():
    def __init__(self):
        print('instantiate ensembleTS object')
        self.arima_train_size = 0.95
    def get_data(self,name):
        self.data = set_data(name)
        print(self.data)
    def transform(self):
        p_val = self.check_stationarity()
        if p_val > 0.05:
            print('Data are non-stationary. transform the data.')
            self.data['Close'] = self.data['Close'].pct_change().fillna(0)
            self.data['Open'] = self.data['Open'].pct_change().fillna(0)
    def ARIMA_model(self):
        #log data before running alg    
        # decomposition = seasonal_decompose(s[0, 1, 2]elf.data['Close']) [0, 1, 2]
        self.arima_params = [0, 1, 2]
        model = ARIMA(self.data['Close'], order=(self.arima_params))
        model_out = model.fit()
        
        self.data['Close_prediction'] = model_out.predict(start = int(len(self.data['Close'])*self.arima_train_size),
                                                          end= len(self.data['Close']), dynamic= True)
        print(model_out.summary())
        print(self.data[['Close','Close_prediction']])
        self.data[['Close','Close_prediction']].plot()
        plt.show()
    def tune_arima(self):
        # p_values = [0, 2, 6, 8]
        # d_values = [0,1,2,3]
        # q_values = [0,1,2,3]
        #TODO: save params for each crypto in a file that you reference and 
        #then use sys.argv[] to tune a crypto or not
        #Don't like the asymmetry
        param_arima = [[0, 0, 0],[0, 0, 1],[0, 0, 2],[0, 0, 3],[0, 1, 0],[0, 1, 1],
         [0, 1, 2],[0, 1, 3],[0, 2, 0],[0, 2, 1],[0, 2, 2],[0, 2, 3],
         [0, 3, 0],[0, 3, 1],[0, 3, 2],[0, 3, 3],[2, 0, 0],[2, 0, 1],
         [2, 0, 2],[2, 0, 3],[2, 1, 0],[2, 1, 1],[2, 1, 2],[2, 1, 3],
         [2, 2, 0],[2, 2, 1],[2, 2, 2],[2, 2, 3],[2, 3, 0],[2, 3, 1], 
         [2, 3, 2],[2, 3, 3]]
        # param_arima = [[0, 0, 0],[0, 0, 1],[0, 0, 2],[0, 0, 3],[0, 1, 0],[0, 1, 1],
        #  [0, 1, 2],[0, 1, 3],[0, 2, 0],[0, 2, 1],[0, 2, 2],[0, 2, 3],
        #  [0, 3, 0],[0, 3, 1],[0, 3, 2],[0, 3, 3],[2, 0, 0],[2, 0, 1],
        #  [2, 0, 2],[2, 0, 3],[2, 1, 0],[2, 1, 1],[2, 1, 2],[2, 1, 3],
        #  [2, 2, 0],[2, 2, 1],[2, 2, 2],[2, 2, 3],[2, 3, 0],[2, 3, 1], 
        #  [2, 3, 2],[2, 3, 3],[6, 0, 0],[6, 0, 1],[6, 0, 2],[6, 0, 3],
        #  [6, 1, 0],[6, 1, 1],[6, 1, 2],[6, 1, 3],[6, 2, 0],[6, 2, 1],
        #  [6, 2, 2],[6, 2, 3],[6, 3, 0],[6, 3, 1],[6, 3, 2],[6, 3, 3],
        #  [8, 0, 0],[8, 0, 1],[8, 0, 2],[8, 0, 3],[8, 1, 0],[8, 1, 1],
        #  [8, 1, 2],[8, 1, 3],[8, 2, 0],[8, 2, 1],[8, 2, 2],[8, 2, 3],
        #  [8, 3, 0],[8, 3, 1],[8, 3, 2],[8, 3, 3]]
        mape_best,mape = float("inf"),float("inf")
        filterwarnings("ignore")
        for inst in tqdm(param_arima):
            try:
                mape = self.error_arima(inst)
            except:
                continue
            if mape < mape_best:
                mape_best = mape
                self.arima_params = inst
                print(f'curr best: {mape_best}, with parameters: {self.arima_params}')
    def error_arima(self,arima_order):
        	# prepare training dataset
        train_size = int(len(self.data['Close']) * self.arima_train_size)
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
        return mean_squared_error(test,predict,squared=False) #RMSE
    def SARIMA(self):
        """
        parameters_list
        d - integration order
        D - seasonal integration order
        s - length of season
        exog - the exogenous variable
        """
        self.SARIMAX_model = SARIMAX(self.data['Close'], 
                             order=(self.params_SARMA[0], 1, self.params_SARMA[1]), 
                             seasonal_order=(self.params_SARMA[2], 1, self.params_SARMA[3], 4)).fit(dis=-1)
        print(self.SARIMAX_model.summary())
        plt.figure()
        self.SARIMAX_model.plot_diagnostics(figsize=(15,12))
        plt.show()
    def tune_SARIMA(self):
        """
        Tunes based on AIC values
        """
        p = range(0, 4, 1)
        q = range(0, 4, 1)
        P = range(0, 4, 1)
        Q = range(0, 4, 1)
        self.parameters_SARIMA = list(product(p, q, P, Q))
        aic_init = float('inf')
        for param in tqdm(self.parameters_SARIMA):
            try: 
                model = SARIMAX(self.data['Close'].values, 
                                order=(param[0],1, 
                                       param[1]), 
                                seasonal_order=(param[2],1,param[3], 4)).fit(disp=-1)
                aic = model.aic
                #lower aic is better
                if aic < aic_init:
                    aic_init = aic
                    self.params_SARMA = param
            except:
                continue
    def check_stationarity(self):
        stationary = adfuller(self.data['Close'].values)
        # plot_acf(self.data['Close'].values)
        # plt.show()
        return stationary[1]
    def run_object(self):
        self.get_data(argv[1])
        self.transform()
        if argv[2] == "tune":
            self.tune_arima()
        self.ARIMA_model()
        self.tune_SARIMA()
        self.SARIMA()
def main():
    ensembleTS().run_object()
if __name__ == "__main__":
    main()