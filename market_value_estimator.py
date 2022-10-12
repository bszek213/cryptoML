#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estimate market value across n days by calculating the cumulative percent change 
for every crypto
@author: brianszekely
"""
import matplotlib.pyplot as plt
import os
from pandas import DataFrame, read_csv
import yfinance as yf
from timeit import default_timer
from numpy import nanmedian, nanmean, zeros, log
from tqdm import tqdm
SET_PERIOD = 90
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
def percent_change(main_df,history,crypto,crypt_count):
    if len(history) >= SET_PERIOD:
        # temp = log(inst_data['Close']/inst_data['Close'].shift(1))
        # inst_data['log_return_sum'] = temp.cumsum()
        # temp_per_change = history[-SET_PERIOD:].pct_change()
        temp = log(history['Close']/history['Close'].shift(1))
        colum_title = f'{crypto}'
        main_df[colum_title] = temp[-SET_PERIOD:].cumsum()
        crypt_count+=1
        return main_df,crypt_count
    else:
        return main_df,crypt_count
def plot_all(main_df,crypt_count):
    rolling_mean = zeros(len(main_df))
    for i in range(len(main_df)):
        rolling_mean[i] = nanmedian(main_df.iloc[i])
    plt.figure(figsize=(12, 10), dpi=350)
    for crypt in main_df.columns:
        plt.plot(main_df[crypt],'tab:gray')
        plt.annotate(xy=(main_df[crypt].index[-1],main_df[crypt].iloc[-1]),
                    xytext=(5,0),
                    textcoords='offset points', 
                    text=crypt, va='center',fontsize=8)
    plt.plot(main_df.index,rolling_mean,linewidth=3,color='blue',label='2-week rolling median')
    lower = nanmean(rolling_mean) - (nanmean(rolling_mean) * 11)
    upper = abs(nanmean(rolling_mean) + (nanmean(rolling_mean) * 11))
    plt.ylim([lower,upper])
    set_title = f'Cumulative log returns across {SET_PERIOD} days on {crypt_count} cryptos'
    plt.title(set_title,fontweight='bold')
    plt.xlabel('TIME')
    plt.ylabel('Cumulative Log Returns')
    plt.legend()
    direct = os.getcwd()
    name = 'full_market_trend.png'
    direct = os.getcwd()
    check_folder = os.path.join(direct)
    if os.path.exists(check_folder):
        final_dir = os.path.join(check_folder, name)
    else:
        os.mkdir(check_folder)
        final_dir = os.path.join(check_folder, name)
    plt.tight_layout()
    plt.savefig(final_dir,dpi=350)
    plt.close()
def main():
    start = default_timer()
    main_df = DataFrame()
    names_crypt = set_crypt_names()
    crypt_count = 0
    for crypt in tqdm(names_crypt):
        print(crypt)
        data = set_data(crypt)
        main_df,crypt_count = percent_change(main_df,data,crypt,crypt_count)
    plot_all(main_df,crypt_count)
if __name__ == "__main__":
    main()