#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yahoo finance to get stable coin price
better than Kraken as with kraken you can only use 
720 data points, with yfiance there is no limit
@author: brianszekely
"""
from prophet import Prophet
from sklearn.linear_model import LinearRegression
# from prophet.diagnostics import cross_validation, performance_metrics
# from prophet.plot import plot_cross_validation_metric
from prophet.plot import add_changepoints_to_plot
import matplotlib.pyplot as plt
import os
# import sys
from pandas import DataFrame, read_csv
import yfinance as yf
import itertools
from timeit import default_timer
from numpy import arange, mean, empty, nan, array, zeros, percentile
from tqdm import tqdm
# from multiprocessing import Process
# import multiprocessing as mp
from scipy.signal import savgol_filter
from urllib3 import PoolManager
"""
TODO
1. ensemble modeling - add arima and other forecasters as a well of getting 
the best picture
"""
def set_crypt_names():
    location = os.getcwd()
    df = read_csv(os.path.join(location,'crypto_trade_min.csv'))
    df.sort_values(by=['crypto'],inplace=True)
    return df['crypto']
                     
def set_data(crypt):
    # crypt_name = sys.argv[1] + '-USD'
    crypt_name = crypt + '-USD'
    temp = yf.Ticker(crypt_name)
    history = temp.history(period = 'max', interval="1d")
    # data = yf.download(tickers=crypt_name, period = 'max', interval = '1d') #columns = Index(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    return history

def convert_to_panda(inst_data):
    df = DataFrame(list(zip(inst_data['Close'],inst_data.index)),columns = ['y', 'ds'])
    return df

def macd(crypto_df_final):
    crypto_df_final['sma_1'] = crypto_df_final['y'].ewm(span=26,
                      min_periods=26-1).mean()
    crypto_df_final['sma_2'] = crypto_df_final['y'].ewm(span=12,
                     min_periods=12-1).mean()
    crypto_df_final['macd_diff'] = crypto_df_final['sma_2'] - crypto_df_final['sma_1']
    #filter the MACD diff line
    sav_data =  savgol_filter(crypto_df_final['macd_diff'].dropna().values, 3, 2)
    an_array = empty(len(crypto_df_final['macd_diff']))
    an_array[:] = nan
    an_array[len(crypto_df_final['macd_diff']) - len(sav_data):len(crypto_df_final['macd_diff'])] = sav_data
    crypto_df_final['macd_diff'] = an_array
    crypto_df_final['signal_line'] = crypto_df_final['macd_diff'].ewm(span=9,
                     min_periods=9-1).mean()
    #Calculate IQR
    #TODO: calculate a running IQR for better fitting
    q75 = zeros(2)
    q25 = zeros(2)
    q75[0], q25[0] = percentile(crypto_df_final['macd_diff'].iloc[0:int(len(crypto_df_final)/2)].dropna().values, 
                                [75 ,25])
    q75[1], q25[1] = percentile(crypto_df_final['macd_diff'].iloc[int(len(crypto_df_final)/2):-1].values, 
                                [75 ,25])
    # q75, q25 = percentile(crypto_df_final['macd_diff'].dropna().values, [75 ,25])
    return crypto_df_final, q25, q75

def model(inst_data, per_for, crypt, error, changepoint_prior_scale, seasonality_prior_scale, seasonality_mode, holiday):#holidays_prior_scale=10
    mod = Prophet(interval_width=0.95, daily_seasonality=True, 
                  changepoint_prior_scale=changepoint_prior_scale,
                  seasonality_prior_scale=seasonality_prior_scale,
                  holidays_prior_scale=holiday,
                  seasonality_mode=seasonality_mode)
    mod.add_country_holidays(country_name='US')
    final = mod.fit(inst_data)
    
    #Collect error - add ability to collect the average error across all horizons, then get the average error among all cryptos, if the error is below the average then buy crypto (it will be another condition)
    future = final.make_future_dataframe(periods=per_for, freq='D') #predict next 30 days
    forecast = final.predict(future)
    #plot the whole figure
    fig2 = final.plot(forecast)
    inst_data, q25, q75 = macd(inst_data)
    #check if macd is below the signal line
    # if inst_data['macd_diff'].iloc[-2] < inst_data['signal_line'].iloc[-2]:
    #     below_signal = True
    # else:
    #     below_signal = False
    if ((inst_data['macd_diff'].iloc[-1] < 0) and 
        (inst_data['macd_diff'].iloc[-2] < inst_data['signal_line'].iloc[-2]) and
        (inst_data['macd_diff'].iloc[-1] > inst_data['signal_line'].iloc[-1]) and 
        (inst_data['macd_diff'].iloc[-1] <= q25[1])):
        cross_point_buy = True
    else:
        cross_point_buy = False
        
    if ((inst_data['macd_diff'].iloc[-1] > 0) and 
        (inst_data['macd_diff'].iloc[-2] > inst_data['signal_line'].iloc[-2]) and
        (inst_data['macd_diff'].iloc[-1] < inst_data['signal_line'].iloc[-1]) and 
        (inst_data['macd_diff'].iloc[-1] >= q75[1])):
        cross_point_sell = True
    else:
        cross_point_sell = False
    #Linear Regression
    data_len = 60 #last 30 days + the 30 day prediction
    a_list = list(arange(len(forecast)-data_len,len(forecast)))
    X1 = array(a_list)
    X = X1.reshape(-1, 1)
    reg = LinearRegression().fit(X, forecast['yhat'].iloc[-data_len-1:-1].values)
    reg_arr = zeros(len(forecast['yhat']))
    for i in X1:
        reg_arr[i] = (reg.coef_ * i) + reg.intercept_
    reg_arr = [nan if x == 0 else x for x in reg_arr]
    #Plot data
    plt.plot(inst_data['ds'],inst_data['sma_1'],'r')
    plt.plot(inst_data['ds'],inst_data['sma_2'],'b')
    a = add_changepoints_to_plot(fig2.gca(), mod, forecast)
    str_combine = crypt +': change:' + str(changepoint_prior_scale) + ', season: ' + str(seasonality_prior_scale) +  ', error: ' + str(error) + ', mode: ' + str(seasonality_mode) + ', holiday: ' + str(seasonality_prior_scale)
    # plt.text(inst_data['ds'].iloc[0], inst_data['y'].max()/2, str_combine, fontsize=10)
    plt.title(str_combine)
    #make and check directories
    direct = os.getcwd()
    name = crypt + '.png'
    direct = os.getcwd()
    check_folder = os.path.join(direct,'forecast_ML',crypt)
    if os.path.exists(check_folder):
        final_dir = os.path.join(check_folder, name)
    else:
        os.mkdir(check_folder)
        final_dir = os.path.join(check_folder, name)
    plt.tight_layout()
    plt.savefig(final_dir,dpi=300)
    plt.close()
    #MACD line and regression
    fig, ax = plt.subplots(2,1,figsize=(16, 16), dpi=350) 
    ax[0].plot(inst_data['ds'],inst_data['macd_diff'],'r',label='MACD')
    ax[0].plot(inst_data['ds'],inst_data['signal_line'],'b',label='signal')
    ax[0].hlines(y = 0, xmin=inst_data['ds'].iloc[0], xmax=inst_data['ds'].iloc[-1])
    # ax[0].hlines(y = q25[0], xmin=inst_data['ds'].iloc[0], xmax=inst_data['ds'].iloc[-1],label='LowerBound_1st'
    #               ,color='black')
    # ax[0].hlines(y = q75[0], xmin=inst_data['ds'].iloc[0], xmax=inst_data['ds'].iloc[-1],label='UpperBound_1st',
    #               color='black')
    # ax[0].hlines(y = q25[1], xmin=inst_data['ds'].iloc[0], xmax=inst_data['ds'].iloc[-1],label='LowerBound_2nd'
    #               ,color='green')
    # ax[0].hlines(y = q75[1], xmin=inst_data['ds'].iloc[0], xmax=inst_data['ds'].iloc[-1],label='UpperBound_2nd',
    #               color='green')
    ax[0].fill_between(inst_data['ds'], q75[0], q25[0], color='red',
                      alpha=0.2,label='IQR range 1st half')
    ax[0].fill_between(inst_data['ds'], q75[1], q25[1], color='blue',
                      alpha=0.2,label='IQR range 2nd half')
    ax[0].legend()
    ax[0].set_xlabel('TIME')
    ax[0].set_ylabel('MACD Values')
    title_name= f'MACD | {crypt}'
    ax[0].set_title(title_name)
    ax[0].grid(True)
    # fig.set_size_inches(8.5, 8.5)
    title_name= f'Regression | {crypt} | Coef: {reg.coef_[0]}'
    ax[1].set_title(title_name)
    ax[1].plot(forecast['ds'],forecast['yhat'],'b',label='yhat')
    ax[1].plot(forecast['ds'],reg_arr,'r',label='regression',linewidth=3)
    # sub_arr_up = forecast['yhat_upper'].iloc[-120:-1]
    # sub_arr_low = forecast['yhat_lower'].iloc[-120:-1]
    # ax[1].set_ylim([min(sub_arr_low),max(sub_arr_up)])  
    ax[1].legend()
    ax[1].set_xlabel('TIME')
    ax[1].set_ylabel('Price Values')
    ax[1].grid(True)
    direct = os.getcwd()
    name = crypt + '_MACD.png'
    direct = os.getcwd()
    check_folder = os.path.join(direct,'forecast_ML',crypt)
    if os.path.exists(check_folder):
        final_dir = os.path.join(check_folder, name)
    else:
        os.mkdir(check_folder)
        final_dir = os.path.join(check_folder, name)
    plt.tight_layout()
    plt.savefig(final_dir,dpi=300)
    plt.close()
    #plot the last 3 months of data
    fig = final.plot(forecast)
    plt.plot(inst_data['ds'],inst_data['sma_1'],'r')
    plt.plot(inst_data['ds'],inst_data['sma_2'],'b')
    fig.set_size_inches(8.5, 8.5)
    # a = add_changepoints_to_plot(fig.gca(), mod, forecast)
    str_combine = 'change:' + str(changepoint_prior_scale) + ', season: ' + str(seasonality_prior_scale) +  ', error: ' + str(error)
    # plt.text(inst_data['ds'].iloc[0], inst_data['y'].max()/2, str_combine, fontsize=10)
    title_name = crypt +' last 3 months'
    plt.title(title_name)
    #make and check directories
    name = crypt + 'zoom' +'.png'
    check_folder = os.path.join(direct,'forecast_ML',crypt)
    if os.path.exists(check_folder):
        final_dir = os.path.join(check_folder, name)
    else:
        os.mkdir(check_folder)
        final_dir = os.path.join(check_folder, name)
    
    if len(forecast) > 90:
        plt.xlim([forecast['ds'].iloc[-90],forecast['ds'].iloc[-1]])
        sub_arr_up = forecast['yhat_upper'].iloc[-90:-1]
        sub_arr_low = forecast['yhat_lower'].iloc[-90:-1]
    else:
        plt.xlim([forecast['ds'].iloc[-60],forecast['ds'].iloc[-1]])
        sub_arr_up = forecast['yhat_upper'].iloc[-60:-1]
        sub_arr_low = forecast['yhat_lower'].iloc[-60:-1]
    plt.ylim([min(sub_arr_low),max(sub_arr_up)])    
    plt.savefig(final_dir,dpi=300)
    plt.close()
    # save_error = 0
    return forecast, cross_point_buy, cross_point_sell, reg.coef_[0]

def model_tuning(df,crypt):
    param_grid = {  
    'changepoint_prior_scale': arange(0.0001, 0.015, 0.005),
    'seasonality_prior_scale': arange(0.01, 10, 1),
    'seasonality_mode': ['additive', 'multiplicative'],
    'holidays_prior_scale': arange(0.01, 10, 1)
    }
    
    # Generate all combinations of parameters
    all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
    error_list = []  # Store the RMSEs for each params here
    param_list = []
    train = int(len(df) * 0.90)
    test = int(len(df) * 0.10)
    #plot trainig and test data
    plt.plot(df['ds'].iloc[0:train],df['y'].iloc[0:train],'r',label='training')
    plt.plot(df['ds'].iloc[-test:-1],df['y'].iloc[-test:-1],'b',label='test')
    plt_name = crypt +'_training_test_set'
    plt.title(plt_name)
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.legend()
    direct = os.getcwd()
    name = 'test_train_data_'+crypt + '.png'
    check_folder = os.path.join(direct,'forecast_ML',crypt)
    if os.path.exists(check_folder):
        final_dir = os.path.join(check_folder, name)
    else:
        os.mkdir(check_folder)
        final_dir = os.path.join(check_folder, name)
    plt.savefig(final_dir,dpi=250)
    plt.close()
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
    # # CROSS VALIDATION - MAYBE USE IT FOR THE FUTURE, IDK IF IT REALLY HELPS
    # init_period_train = int(len(df) * 0.80) #days for training
    # period_val = int(init_period_train * 0.05) # percent of init period 
    # horiz_val = 15
    
    # initial_days =  str(init_period_train)+' '+'days' #make it 80% of the total length
    # period_days = str(period_val)+' '+'days' #
    # horizon_days = str(horiz_val)+' '+'days'
    # for params in tqdm(all_params):
    #     # with suppress_stdout_stderr():
    #     m = Prophet(**params)
    #     m.add_country_holidays(country_name='US')
    #     m.fit(df)  # Fit model with given params
    #     df_cv = cross_validation(m, initial = initial_days, period=period_days, horizon=horizon_days, parallel="processes")
    #     df_p = performance_metrics(df_cv, rolling_window=1)
    #     rmses.append(df_p['mape'].values[0])
    # #plot the performance
    # fig = plot_cross_validation_metric(df_cv, metric='mape') #MAPE is not in %
    # direct = os.getcwd()
    # name = 'tuning_'+ sys.argv[1] + '.png'
    # check_folder = os.path.join(direct,'graphs_yf',sys.argv[1])
    # if os.path.exists(check_folder):
    #     final_dir = os.path.join(check_folder, name)
    # else:
    #     os.mkdir(check_folder)
    #     final_dir = os.path.join(check_folder, name)
    # plt.savefig(final_dir)
    # plt.close()
    # # Find the best parameters
    # tuning_results = pd.DataFrame(all_params)
    # tuning_results['mape'] = rmses
    # min_loc = tuning_results[['mape']].idxmin()
    # # best_params = tuning_results.iloc[min_loc].values
    # change = tuning_results['changepoint_prior_scale'].iloc[min_loc].values
    # season = tuning_results['seasonality_prior_scale'].iloc[min_loc].values
    # # holidays = tuning_results['seasonality_mode'].iloc[min_loc]
    # error = tuning_results['mape'].iloc[min_loc].values
    # tuning_results = tuning_results.sort_values(by=['mape'])
    # file_name = sys.argv[1] +'_tuning_results.csv'
    # final_dir = os.path.join(check_folder,file_name)
    # tuning_results.to_csv(final_dir)
    print('=============================================')
    print(f'Number of days (elements) used for training: {train}')
    print(f'Number of days (elements) used for periods: {test}')
    # print(f'Number of days (elements) used for horizion: {horiz_val}')
    print('=============================================')
    return change, season, error, season_mode, holiday

def read_params(filepath):
    df = read_csv(filepath)
    return df['changepoint_prior_scale'].iloc[0],df['seasonality_prior_scale'].iloc[0],df['error'].iloc[0], df['seasonality_mode'].iloc[0], df['holidays_prior_scale'].iloc[0]

def tuning(df,train,test,params):
    m = Prophet(**params)
    m.add_country_holidays(country_name='US')
    m.fit(df.iloc[0:train])
    forecast_test = m.predict(df.iloc[-test:-1]) #CHECK THIS I THINK ITS ALSO COMPARING THE FUTURE PREDICTIONS
    mape_values = mean((abs(df['y'].iloc[-test:-1].values - forecast_test['yhat'].values)
                        / df['y'].iloc[-test:-1].values) * 100)
    return mape_values

def main():
    #TODO: change percent change to a linear regression?
    start = default_timer()
    names_crypt = set_crypt_names()
    # while True:
    crypt_above_zero = []
    int_change = []
    below_zero_list = []
    macd_sell = []
    for crypt in names_crypt:
        print(crypt)
        while True:
            try:
                http = PoolManager()
                url = 'https://finance.yahoo.com/'
                response = http.request('GET', url)
                break
            except Exception as e:
                    print(f'NO INTERNET: {e}') 
        try:
            data = set_data(crypt)
            df_data = convert_to_panda(data)
            file_name = crypt  + '_tuning_results.csv'
            final_dir = os.path.join(os.getcwd(),'forecast_ML',crypt, file_name)
            if os.path.exists(final_dir):
                print('use parameters from file')
                change, season, error, season_mode, holiday = read_params(final_dir)
            else:
                change, season, error, season_mode, holiday = model_tuning(df_data,crypt)
                change, season, error, season_mode, holiday = read_params(final_dir)
            forecast, cross_point_buy, cross_point_sell, reg_coef = model(df_data, 31, crypt, error, change, season, season_mode, holiday)
            #Regress predictions
            if reg_coef > 0:
                # if cross_point == True:# and below_zero == True:
                crypt_above_zero.append(crypt)
                int_change.append(reg_coef)
                below_zero_list.append(cross_point_buy)
                macd_sell.append(cross_point_sell)
                print(f'{crypt} and coeff: {reg_coef}')
            del forecast, http, data, df_data
        except Exception as e:
                print(f'{e}')
    pos_crypts = DataFrame(list(zip(crypt_above_zero,int_change,below_zero_list,macd_sell)),
                           columns=['crypto','reg_coef','MACD_cross_buy','MACD_cross_sell'])
    pos_crypts = pos_crypts.sort_values(by=['reg_coef'],ascending=False)
    if os.path.exists(os.path.join(os.getcwd(),'save_pos_cryptos.csv')) == True:
        os.remove('save_pos_cryptos.csv')
    pos_crypts.to_csv('save_pos_cryptos.csv')
    print(f'current crypto code took {default_timer() - start} seconds')
    # del pos_crypts, names_crypt, crypt_above_zero, int_change, below_zero_list, http, forecast
if __name__ == "__main__":
    main()
