#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
technical analysis - day trading when the whole market is trending
negatively
only use the 5 and 15 min intervals
limit to 5-10 trades a day
@author: brianszekely
"""
from sklearn.linear_model import LinearRegression
import krakenex
from pykrakenapi import KrakenAPI
from numpy import array, zeros, nan, arange, percentile, empty, log
from time import sleep
# import argparse
from os import path, getcwd, listdir, remove, mkdir
from pandas import DataFrame, read_csv, date_range
# from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from os.path import join, exists
import warnings
# import buy_sell_signals
# from datetime import datetime, timedelta
# from scipy.signal import savgol_filter
from tqdm import tqdm
from glob import glob
warnings.filterwarnings("ignore")
SAMPLE_RATE = 5
class technical():
    def __init__(self):
        print('initialize kraken data')
        api = krakenex.API()
        api.load_key('key.txt')
        self.kraken = KrakenAPI(api)
        self.total_trades = 0
    def readin_cryptos(self):
        direct = getcwd()
        location = join(direct, 'crypto_trade_min_kraken.csv')
        self.crypto_list = read_csv(location)
        print(f'number of cryptos monitoring: {len(self.crypto_list)}')
    def get_24_above_zero(self):
        #TODO: change the difference to linear regression
        # total_samples = 24*SAMPLE_RATE
        save_positive = []
        self.readin_cryptos()
        for name in tqdm(self.crypto_list['crypto']):
            try:
                update_name = name + 'USD'
                self.get_ohlc(update_name)
                # prev_24 = self.data.close.iloc[-total_samples]
                # current = self.data.close.iloc[-1]
                self.half_LR()
                # self.volatility()
                if (self.reg_coef > 0): #add coeff variation here
                    save_positive.append(update_name)
                sleep(1) #I have to do this or I get gated
            except:
                print(f'{name} could not be found')
        print(f'All positive cryptos: {save_positive}')
        return save_positive
    def get_ohlc(self,crypt):
        self.data = DataFrame()
        """
        Parameters
        ----------
        kraken : Kraken object
            DESCRIPTION.
        crypt : crypto str name
            DESCRIPTION.
        inter : int variable - sampling window
            time frame interval minutes 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600.
        Returns
        -------
        Pandas df 
            close, high, low prices.
        """
        ohlc = None
        while True:
            try:
                ohlc = self.kraken.get_ohlc_data(crypt, interval = SAMPLE_RATE,
                                                 since = 0,
                                                 ascending = True) #returns two years of data7
            except Exception as e:
                print(f'getohlc() timed out from internet connection: {e}')
            if ohlc is not None:
                break
        # self.ohlc_no_param = ohlc[0]
        self.data = ohlc[0] 
    def half_LR(self):
        data_len = int((24*60)/SAMPLE_RATE) #get samples out of 24 hours
         # = total_samples #last 30 days + the 30 day prediction
        a_list = list(arange(len(self.data)-data_len,len(self.data)))
        X1 = array(a_list)
        X = X1.reshape(-1, 1)
        reg = LinearRegression().fit(X, self.data['close'].iloc[-data_len-1:-1].values)
        self.reg_arr_half = zeros(len(self.data['close']))
        for i in X1:
            self.reg_arr_half[i] = (reg.coef_ * i) + reg.intercept_
        self.reg_arr_half = [nan if x == 0 else x for x in self.reg_arr_half]
        self.reg_coef = reg.coef_
    def macd(self):
        self.data['sma_1'] = self.data['close'].ewm(span=26,
                          min_periods=26-1).mean()
        self.data['sma_2'] = self.data['close'].ewm(span=12,
                         min_periods=12-1).mean()
        self.data['macd_diff'] = self.data['sma_2'] - self.data['sma_1']
        self.data['signal_line'] = self.data['macd_diff'].ewm(span=9,
                                                              min_periods=9-1).mean()
        self.q75_macd, self.q25_macd = percentile(self.data['macd_diff'].dropna().values, 
                                    [75 ,25])
    def RSI(self):
        self.data['change'] = self.data.close.diff()
        # crypto_df['U'] = [x if x > 0 else 0 for x in crypto_df.change]
        # crypto_df['D'] = [abs(x) if x < 0 else 0 for x in crypto_df.change]
        self.data['U']  = self.data['change'].clip(lower=0)
        self.data['D'] = -1*self.data['change'].clip(upper=0)
        self.data['U'] = self.data.U.ewm(span=14,
                   min_periods=13).mean()
        self.data['D'] = self.data.D.ewm(span=14,
                   min_periods=13).mean()
        self.data['RS'] = self.data.U / self.data.D
        self.data['RSI'] = 100 - (100/(1+self.data.RS))
        #calculate the percentile
        self.q75, self.q25 = percentile(self.data['RSI'].dropna().values, [75 ,25])
    def moving_averages(self):
        self.data['ewmshort'] = self.data['close'].ewm(span=25, min_periods=25).mean() #used to be 50
        self.data['ewmmedium'] = self.data['close'].ewm(span=128, min_periods=128).mean()
        self.data['ewmlong'] = self.data['close'].ewm(span=200, min_periods=200).mean()
    def aroon_ind(self,lb=25):
        """
        AROON UP = [ 25 - PERIODS SINCE 25 PERIOD HIGH ] / 25 * [ 100 ]
        AROON DOWN = [ 25 - PERIODS SINCE 25 PERIOD LOW ] / 25 * [ 100 ]
        if up[i] >= 70 and down[i] <= 30: buy
        if up[i] <= 30 and down[i] >= 70: sell
        """
        self.data['aroon_up'] = 100 * ((self.data.high.rolling(lb).apply(lambda x: x.argmax())) / lb)
        self.data['aroon_down'] = 100 * ((self.data.low.rolling(lb).apply(lambda x: x.argmin())) / lb)
    def volatility(self):
        self.data['log_return'] = log(self.data['close']/self.data['close'].shift())
        self.volatility_value = self.data['log_return'].std()*len(self.data)**0.5 #365 days of trading square root
        self.coef_variation = self.data['log_return'].std() / self.data['log_return'].mean()
    def plot(self,name):
        fig, ax = plt.subplots(4,1,figsize=(12, 20)) 
        #plot close price
        str_name = f'{name} : {round(self.coef_variation,4)}% coeff of variation'
        ax[0].set_title(str_name)
        ax[0].plot(self.data.index,self.data['close'],'tab:blue', marker="o",
               markersize=1, linestyle='', label = 'Close Price')
        ax[0].plot(self.data.index,self.reg_arr_half,'tab:orange',label = 'linearRegressor')
        ax[0].plot(self.data.index, self.data['ewmlong'], 'black', label = 'long-200')
        ax[0].plot(self.data.index, self.data['ewmshort'], 'crimson', label = 'short-128')
        ax[0].plot(self.data.index, self.data['ewmmedium'], 'green', label = 'medium-25')
        ax[0].scatter(self.data.index, self.data['buy'], marker='o', s=120, color = 'g', label = 'buy')
        ax[0].legend()
        ax[0].grid(True)
        ax[0].set_xlabel('iterations')
        ax[0].set_ylabel('Close Price')
        #plot macd
        ax[1].plot(self.data.index, self.data['macd_diff'], 'tab:green', marker="o",
                        markersize=1, linestyle='-', label = 'macd diff')
        ax[1].plot(self.data.index, self.data['signal_line'], 'tab:red', marker="o",
                        markersize=1, linestyle='-', label = 'signal line')
        ax[1].fill_between(self.data.index, self.q75_macd, self.q25_macd, color='green',
                          alpha=0.2,label='IQR range MACD')
        ax[1].hlines(y = 0, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[1].legend()
        ax[1].grid(True)
        ax[1].set_xlabel('iterations')
        ax[1].set_ylabel('MACD Values')
        #RSI
        ax[2].plot(self.data.index, self.data['RSI'], 'r', marker="o", markersize=2, 
                   linestyle='-',
                   linewidth= 0.25, label = 'RSI')
        ax[2].hlines(y = self.q25, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[2].hlines(y = self.q75, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[2].legend()
        ax[2].set_xlabel('iterations')
        ax[2].set_ylabel('RSI Values')
        ax[2].grid(True)
        #aroon
        ax[3].plot(self.data.index, self.data['aroon_up'], 'r', marker="o", markersize=2, 
                   linestyle='-',linewidth= 0.25, label = 'aroon_up')
        ax[3].plot(self.data.index, self.data['aroon_down'], 'b', marker="o", markersize=2, 
                   linestyle='-',linewidth= 0.25, label = 'aroon_down')
        ax[3].legend()
        ax[3].set_xlabel('iterations')
        ax[3].set_ylabel('aroon')
        ax[3].grid(True)
        save_name = name + '.svg'
        direct = getcwd()
        final_dir = join(direct, 'technical_analysis', save_name)
        plt.tight_layout()
        plt.savefig(final_dir,dpi=350)
        plt.close()
    def buy(self):
        self.data['buy'] = empty(len(self.data))
        self.data['buy'].iloc[:] = nan
        for o in range(len(self.data)): 
            if (#(self.data['macd_diff'].iloc[o-1] < self.data['signal_line'].iloc[o-1]) and
                #(self.data['macd_diff'].iloc[o] > self.data['signal_line'].iloc[o]) and
                #(self.data['macd_diff'].iloc[o] < self.q25_macd) and
                # (self.data['macd_diff'].iloc[o] < 0) and
                # (self.data['aroon_down'].iloc[o-1] > self.data['aroon_down'].iloc[o])
                # (self.data['macd_diff'].iloc[o-1] < self.data['macd_diff'].iloc[o]) and
                # (self.data['aroon_up'].iloc[o-1] < self.data['aroon_up'].iloc[o])
                (self.data['ewmshort'].iloc[o-1] < self.data['ewmlong'].iloc[o-1]) and
                (self.data['ewmshort'].iloc[o] > self.data['ewmlong'].iloc[o]) and
                (self.data['RSI'].iloc[o-1] < self.data['RSI'].iloc[o]) and 
                (self.data['RSI'].iloc[o] < self.q75)
                ):
                # if ((self.data['ewmshort'].iloc[o]) <= (self.data['close'].iloc[o]) or
                #     (self.data['ewmlong'].iloc[o]) <= (self.data['close'].iloc[o]) or
                #     (self.data['ewmmedium'].iloc[o]) <= (self.data['close'].iloc[o])):
                    self.data['buy'].iloc[o] = self.data['close'].iloc[o]
                
    def sell(self):
        pass
    def run_analysis_pos_crypt(self):
        pos_crypt = self.get_24_above_zero()
        files = glob(join(getcwd(),'technical_analysis','*'))
        for f in files:
            remove(f)
        save_hist = []
        for name in tqdm(pos_crypt):
            self.get_ohlc(name)
            self.macd()
            self.RSI()
            self.aroon_ind()
            self.moving_averages()
            self.half_LR()
            self.volatility()
            self.buy()
            self.plot(name)
            save_hist.append(self.coef_variation)
            sleep(1)
        plt.figure()
        plt.hist(save_hist,bins=60)
        plt.show()
def main():
    technical().run_analysis_pos_crypt()
if __name__ == "__main__":
    main()
