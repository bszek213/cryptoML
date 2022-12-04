#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble time series forecasters
@author: brianszekely
Run analysis on these cryptos: BTC, ETH, DOGE, LTC, TRON, LINK, BCH, MANA, RLC
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
from prophet import Prophet
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
        mape_best,mape = float("inf"),float("inf")
        filterwarnings("ignore")
        for inst in tqdm(param_arima):
            try:
                mape = self.error_arima(inst)
            except:
                continue
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
    def convert_to_prophet(self):
        cum_sum_close = self.data['Close'].cumsum()
        cum_sum_close.dropna(inplace=True)
        # df = DataFrame(list(zip(inst_data.Close,inst_data.index,inst_data.Volume,inst_data.Open,inst_data.Low,inst_data.High)),columns = ['y', 'ds','Volume','Open','Low','High'])
        self.prophet_data = DataFrame(list(zip(cum_sum_close,self.data.index)),columns = ['y', 'ds'])
    def model_tuning(self,df,crypt):
        param_grid = {  
        'changepoint_prior_scale': arange(0.0001, 0.015, 0.005),
        'seasonality_prior_scale': arange(0.01, 10, 2),
        'seasonality_mode': ['additive', 'multiplicative'],
        'holidays_prior_scale': arange(0.01, 10, 2)
        }
        
        # Generate all combinations of parameters
        all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
        error_list = []  # Store the RMSEs for each params here
        param_list = []
        train = int(len(df) * 0.90)
        test = int(len(df) * 0.10)
        #plot trainig and test data
        # plt.plot(df['ds'].iloc[0:train],df['y'].iloc[0:train],'r',label='training')
        # plt.plot(df['ds'].iloc[-test:-1],df['y'].iloc[-test:-1],'b',label='test')
        # plt_name = crypt +'_training_test_set'
        # plt.title(plt_name)
        # plt.xlabel('Dates')
        # plt.ylabel('Prices')
        # plt.legend()
        # direct = os.getcwd()
        # name = 'test_train_data_'+crypt + '.png'
        # check_folder = os.path.join(direct,'forecast_ML',crypt)
        # if os.path.exists(check_folder):
        #     final_dir = os.path.join(check_folder, name)
        # else:
        #     os.mkdir(check_folder)
        #     final_dir = os.path.join(check_folder, name)
        # plt.savefig(final_dir,dpi=250)
        # plt.close()
        #hyperparameter tuning
        #TODO: parallelize this better
        # pool = mp.Pool(mp.cpu_count())
        # results = [pool.apply(tuning,args=(df,train,test,params)) for params in tqdm(all_params)]
        # error_list = results
        # param_list = all_params
        for params in tqdm(all_params): 
            print('=================')
            print(f'TUNING: {crypt}')
            print('=================')
            errorV = tuning(df,train,test,params) #Process(target=(tuning(df,train,test,params)))
            error_list.append(errorV)
            param_list.append(params)
            del errorV
        # for params in tqdm(all_params):
        #     # with suppress_stdout_stderr():
        #     m = Prophet(**params)
        #     m.add_country_holidays(country_name='US')
        #     m.fit(df.iloc[0:train])
        #     forecast_test = m.predict(df.iloc[-test:-1])
        #     mape_values = mean((abs(df['y'].iloc[-test:-1].values - forecast_test['yhat'].values) / df['y'].iloc[-test:-1].values) * 100)
        #     error_list.append(mape_values)
        #     param_list.append(params)
            
        tuning_results = DataFrame(param_list)
        tuning_results['error'] = error_list
        min_loc = tuning_results[['error']].idxmin()
        change = tuning_results['changepoint_prior_scale'].iloc[min_loc]
        season = tuning_results['seasonality_prior_scale'].iloc[min_loc]
        error = tuning_results['error'].iloc[min_loc].values
        season_mode = tuning_results['seasonality_mode'].iloc[min_loc].values
        holiday = tuning_results['holidays_prior_scale'].iloc[min_loc]
        tuning_results = tuning_results.sort_values(by=['error'])
        #save tuning results
        file_name = crypt +'_tuning_results.csv'
        final_dir = os.path.join(check_folder,file_name)
        tuning_results.to_csv(final_dir)
    def tuning(self, df,train,test,params):
        m = Prophet(**params)
        m.add_country_holidays(country_name='US')
        m.fit(df)
        forecast_test = m.predict(df)
        mape_values = abs(mean((abs(df['y'].values - forecast_test['yhat'].values)
                            / df['y'].values) * 100))
        # m.fit(df.iloc[0:train])
        # forecast_test = m.predict(df.iloc[-test:-1]) #CHECK THIS I THINK ITS ALSO COMPARING THE FUTURE PREDICTIONS
        # mape_values = mean((abs(df['y'].iloc[-test:-1].values - forecast_test['yhat'].values)
        #                     / df['y'].iloc[-test:-1].values) * 100)
        del m, forecast_test
        return mape_values
    def run_object(self):
        self.get_data(sys.argv[1])
        self.transform()
        self.convert_to_prophet()
        # self.tune_arima()
        # self.ARIMA_model()
def main():
    ensembleTS().run_object()
if __name__ == "__main__":
    main()