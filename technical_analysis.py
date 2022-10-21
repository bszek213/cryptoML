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
from numpy import array, zeros, nan, arange, percentile, empty, log, mean, isnan,logical_not
from time import sleep
# import argparse
from os import getcwd, remove
from pandas import DataFrame, read_csv
# from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from os.path import join
import warnings
from buy_sell_signals import buy_signal_hft,basic_sell
# from datetime import datetime, timedelta
# from scipy.signal import savgol_filter
from tqdm import tqdm
from glob import glob
from psutil import virtual_memory
import logging
warnings.filterwarnings("ignore")
"""
TODO: 
-convert UTC to PST time
-change the sell condition to be the crossover points of the MACD or zero crossing of the Awe ind
"""
SAMPLE_RATE = 5
logging.basicConfig(filename=join(getcwd(),'errors.log'), level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
class technical():
    def __init__(self):
        print('initialize kraken data')
        api = krakenex.API()
        api.load_key('key.txt')
        self.kraken = KrakenAPI(api)
        self.total_trades = 0
        self.cumlative_gained = float(0.0)
    def readin_cryptos(self):
        direct = getcwd()
        location = join(direct, 'crypto_trade_min_kraken.csv')
        self.crypto_list = read_csv(location)
        print(f'number of cryptos monitoring: {len(self.crypto_list)}')
    def get_24_above_zero(self):
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
        #calculate MAPE
        temp_arr = [x for x in self.reg_arr_half if ~isnan(x)]
        APE = (self.data['close'].iloc[-data_len-1:-1].values - temp_arr) / self.data['close'].iloc[-data_len-1:-1].values
        self.MAPE = abs(mean(APE))*100
    def awesome_indicator(self):
        self.data['median_price'] = (self.data['high'] + self.data['low']) / 2
        self.data['long_ao'] = self.data['median_price'].rolling(34,
                         min_periods=34-1).mean()
        self.data['short_ao'] = self.data['median_price'].rolling(5,
                         min_periods=5-1).mean()
        self.data['ao'] = self.data['short_ao'] - self.data['long_ao']
        self.q75_ao, self.q25_ao = percentile(self.data['ao'].dropna().values, 
                                    [75 ,25])
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
        self.data['RSI'] = self.data['RSI'].rolling(5).mean()
        #calculate the percentile
        try:
            self.q75, self.q25 = percentile(self.data['RSI'].dropna().values, [75 ,25])
            #calculate an upper bound: Q3 + .2 *IQR
            self.RSI_upper_bound = self.q75 + (.1*(self.q75-self.q25))
        except:
            print('IndexError: cannot do a non-empty take from an empty axes. default to 0')
            self.q75, self.q25, self.RSI_upper_bound = 0,0,0
    def stoch_RSI(self):
        min_val  = self.data['RSI'].rolling(window=14, center=False).min()
        max_val = self.data['RSI'].rolling(window=14, center=False).max()
        self.data['Stoch_RSI'] = ((self.data['RSI'] - min_val) / (max_val - min_val)) * 100
        self.data['Stoch_RSI'] = self.data['Stoch_RSI'].rolling(9).mean()
        try:
            self.q75_Stoch_RSI, self.q25_Stoch_RSI = percentile(self.data['Stoch_RSI'].dropna().values, 
                                                                [75 ,25])
        except:
            print('IndexError: cannot do a non-empty take from an empty axes. default to 0')
            self.q75_Stoch_RSI, self.q25_Stoch_RSI = 0,0
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
        # xlim_val = [self.data.index[int((24*60)/SAMPLE_RATE)],self.data.index[-1]]
        x_low_lim = self.data.index[-int((24*60)/SAMPLE_RATE)]
        fig, ax = plt.subplots(4,1,figsize=(12, 20)) 
        buy_df = self.data[~self.data['buy'].isnull()]
        sell_df = self.data[~self.data['sell'].isnull()]
        #plot close price
        str_name = f'{name} : {round(self.coef_variation,4)} coeff of variation : fit error: {self.MAPE}%'
        ax[0].set_title(str_name)
        ax[0].plot(self.data.index,self.data['close'],'tab:blue', marker="o",
               markersize=1, linestyle='', label = 'Close Price')
        ax[0].plot(self.data.index,self.reg_arr_half,'tab:orange',label = 'linearRegressor')
        ax[0].plot(self.data.index, self.data['ewmlong'], 'black', label = 'long-200')
        ax[0].plot(self.data.index, self.data['ewmshort'], 'crimson', label = 'short-128')
        ax[0].plot(self.data.index, self.data['ewmmedium'], 'green', label = 'medium-25')
        ax[0].scatter(self.data.index, self.data['buy'], marker='o', s=120, color = 'g', label = 'buy')
        ax[0].scatter(self.data.index, self.data['buy_no_condition'], marker='o', s=60, color = 'black', label = 'buy_no_open_trade')
        ax[0].scatter(self.data.index, self.data['sell'], marker='o', s=120, color = 'r', label = 'sell')
        # ax[0].vlines(x=self.data.index[indx],
        #              ymin=min(self.data['close'].values),
        #              ymax= max(self.data['close'].values),color='g',label='buy')
        # ax[0].vlines(x=self.data.index[indx_sell],
        #              ymin=min(self.data['close'].values),
        #              ymax= max(self.data['close'].values),color='r',label='sell')
        ax[0].legend()
        ax[0].grid(True)
        ax[0].set_xlim(left=x_low_lim)
        ax[0].set_xlabel('iterations')
        ax[0].set_ylabel('Close Price')
        #plot macd
        ax[1].plot(self.data.index, self.data['macd_diff'], 'tab:blue', marker="o",
                        markersize=1, linestyle='-', label = 'macd diff')
        ax[1].plot(self.data.index, self.data['signal_line'], 'tab:red', marker="o",
                        markersize=1, linestyle='-', label = 'signal line')
        ax[1].fill_between(self.data.index, self.q75_macd, self.q25_macd, color='green',
                          alpha=0.2,label='IQR range MACD')
        ax[1].scatter(buy_df.index, buy_df['macd_diff'], marker='o', s=120, color = 'g', label = 'buy')
        ax[1].scatter(sell_df.index, sell_df['macd_diff'], marker='o', s=120, color = 'r', label = 'sell')
        # ax[1].vlines(x=self.data.index[indx],
        #              ymin=min(self.data['macd_diff'].values),
        #              ymax= max(self.data['macd_diff'].values),color='g')
        ax[1].hlines(y = 0, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[1].legend()
        ax[1].grid(True)
        ax[1].set_xlim(x_low_lim)
        ax[1].set_xlabel('iterations')
        ax[1].set_ylabel('MACD Values')
        #RSI
        ax[2].plot(self.data.index, self.data['RSI'], 'r', marker="o", markersize=2, 
                   linestyle='-',
                   linewidth= 0.25, label = 'RSI')
        ax[2].hlines(y = self.q25, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[2].hlines(y = self.q75, xmin=self.data.index[0], xmax=self.data.index[-1]) 
        # ax[2].hlines(y = self.RSI_upper_bound, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[2].scatter(buy_df.index, buy_df['RSI'], marker='o', s=120, color = 'g', label = 'buy')
        ax[2].scatter(sell_df.index, sell_df['RSI'], marker='o', s=120, color = 'r', label = 'sell')
        ax[2].legend()
        ax[2].set_xlim(x_low_lim)
        ax[2].set_xlabel('iterations')
        ax[2].set_ylabel('stochRSI Values')
        ax[2].grid(True)
        #ao indicator
        ax[3].plot(self.data.index, self.data['ao'], 'r', marker="o", markersize=2, 
                   linestyle='-',linewidth= 0.25, label = 'awesome_indicator')
        ax[3].scatter(buy_df.index, buy_df['ao'], marker='o', s=120, color = 'g', label = 'buy')
        ax[3].scatter(sell_df.index, sell_df['ao'], marker='o', s=120, color = 'r', label = 'sell')
        ax[3].hlines(y = 0, xmin=self.data.index[0], xmax=self.data.index[-1])
        ax[3].fill_between(self.data.index, self.q75_ao, self.q25_ao, color='green',
                          alpha=0.2,label='IQR range AO')
        ax[3].legend()
        ax[3].set_xlim(x_low_lim)
        ax[3].set_xlabel('iterations')
        ax[3].set_ylabel('Awesome Indicator')
        ax[3].grid(True)
        save_name = name + '.png'
        direct = getcwd()
        final_dir = join(direct, 'technical_analysis', save_name)
        plt.tight_layout()
        plt.savefig(final_dir,dpi=350)
        plt.close()
    def trade(self):
        self.data['buy'] = empty(len(self.data))
        self.data['buy'].iloc[:] = nan
        self.data['buy_no_condition'] = empty(len(self.data))
        self.data['buy_no_condition'].iloc[:] = nan
        self.data['sell'] = empty(len(self.data))
        self.data['sell'].iloc[:] = nan
        open_trade = True
        buy_price = 0
        self.buy_for_trading = 0
        thresh_buy = 0
        thresh_sell = 0
        count_hold_iter = 0
        self.save_time_hold = []
        for o in range(len(self.data)): 
            if (
                #This works but at 60%
                # (self.data['ewmshort'].iloc[o-1] < self.data['ewmlong'].iloc[o-1]) and
                # (self.data['ewmshort'].iloc[o] > self.data['ewmlong'].iloc[o]) and
                # (self.data['RSI'].iloc[o-1] < self.data['RSI'].iloc[o]) and
                # (self.data['ao'].iloc[o] < 0) and
                # (self.data['macd_diff'].iloc[o] < self.q75_macd) and
                # (self.coef_variation > self.lb_coef_deter) and 
                # (self.coef_variation < self.ub_coef_deter)
                (self.data['macd_diff'].iloc[o-1] < self.data['signal_line'].iloc[o-1]) and
                (self.data['macd_diff'].iloc[o] > self.data['signal_line'].iloc[o]) and
                (self.data['RSI'].iloc[o] < self.q25) and
                (self.data['ao'].iloc[o] < 0) and
                (self.data['macd_diff'].iloc[o] < 0) and
                (self.data['macd_diff'].iloc[o] < self.q25_macd) and
                (self.coef_variation > self.lb_coef_deter) and 
                (self.coef_variation < self.ub_coef_deter)
                ):
                    self.buy_for_trading = o
                    self.data['buy_no_condition'].iloc[o] = self.data['close'].iloc[o]
                    if open_trade == True:
                        self.data['buy'].iloc[o] = self.data['close'].iloc[o]
                        buy_price = self.data['close'].iloc[o]
                        thresh_buy = buy_price + (buy_price * 0.0085)
                        thresh_sell = buy_price - (buy_price * (1.5*0.0085))
                        count_hold_iter = 0
                        open_trade = False
            if (open_trade == False):
                count_hold_iter +=1
            #TODO change the sell condition to zero crossing of the Awe ind
            if ((open_trade == False) and
                (self.data['macd_diff'].iloc[o-1] > self.data['signal_line'].iloc[o-1]) and
                (self.data['macd_diff'].iloc[o] < self.data['signal_line'].iloc[o]) and
                (self.data['macd_diff'].iloc[o] > 0)
                ):
                self.data['sell'].iloc[o] = self.data['close'].iloc[o]
                self.cumlative_gained += ((self.data['close'].iloc[o] - buy_price) / buy_price)*100
                self.save_time_hold.append(count_hold_iter)
                open_trade = True
            # if (self.data['ao'].iloc[o] > 0):
            # if ((open_trade == False) and (thresh_buy < self.data['close'].iloc[o])):         
            # if ((open_trade == False) and (thresh_sell > self.data['close'].iloc[o])):
            #     self.data['sell'].iloc[o] = self.data['close'].iloc[o]
            #     self.cumlative_gained += ((self.data['close'].iloc[o] - buy_price) / buy_price)*100
            #     open_trade = True
    def live_trading(self,name):
        trade_now = len(self.data) - self.buy_for_trading
        print(' ') #tqdm things
        print(f'closet trade was {trade_now} iterations ago')
        if trade_now <= 2:
            try:
                print(f'buy {name}')
                #put a buy function here : ad save the thresh and time? 
                old_name = name.replace('USD','')
                ind_cryp_t = self.crypto_list[self.crypto_list['crypto'] == old_name]
                volume_inst = ind_cryp_t['Order'].values
                balance = self.kraken.get_account_balance()
                money_min = float((self.kraken.get_ticker_information(name))['a'][0][0]) * volume_inst
                if money_min < balance.vol['ZUSD']:
                    _, ask_price , _ = buy_signal_hft(name, self.kraken, volume_inst, balance.vol['ZUSD'])
                    threshold = ask_price + (ask_price * 0.0085)
                    thresh_sell = ask_price - (ask_price * (1.5*0.0085))
                    count_iter_hold = 0
                    sold_not_sold = 'not sold'
                    while True:
                        self.get_ohlc(name)
                        self.macd()
                        self.RSI()
                        # self.stoch_RSI()
                        self.aroon_ind()
                        self.moving_averages()
                        self.awesome_indicator()
                        self.half_LR()
                        self.volatility()
                        self.trade()
                        self.plot(name)
                        sold_not_sold = self.check_sell(name, volume_inst, ask_price, threshold, count_iter_hold,thresh_sell)
                        count_iter_hold+=1
                        if sold_not_sold == 'sold':
                            break
                        sleep(SAMPLE_RATE*60)
                else:
                    print(f'cannot buy {old_name}, not enough money in trading acoount')
            except Exception as e:
                logger.error(e)
    def check_sell(self,name,volume_inst,ask_price,threshold,count_iter_hold,thresh_sell):
        curr_ask = float((self.kraken.get_ticker_information(name))['a'][0][0])
        print(f'current ask: {curr_ask} : {threshold} threshold')
        if  (threshold < curr_ask):
            balance = self.kraken.get_account_balance()
            basic_sell(name, self.kraken, volume_inst, balance)
            return 'sold'
        if (thresh_sell > curr_ask):
        # if count_iter_hold > self.average_pos_hold:
            balance = self.kraken.get_account_balance()
            basic_sell(name, self.kraken, volume_inst, balance)
            return 'sold'
        return 'not sold'
    def run_analysis_pos_crypt(self):
        self.average_pos_hold = 76
        self.lb_coef_deter = 18.75
        self.ub_coef_deter = 60.35
        while True:
            pos_crypt = self.get_24_above_zero()
            files = glob(join(getcwd(),'technical_analysis','*'))
            for f in files:
                remove(f)
            save_hist = []
            save_hold_time_temp = []
            for name in tqdm(pos_crypt):
                self.get_ohlc(name)
                self.macd()
                self.RSI()
                # self.stoch_RSI()
                self.aroon_ind()
                self.moving_averages()
                self.awesome_indicator()
                self.half_LR()
                self.volatility()
                self.trade()
                # if self.coef_variation != 'nan':
                save_hist.append(self.coef_variation)
                if ((self.lb_coef_deter < self.coef_variation) and 
                   (self.ub_coef_deter > self.coef_variation)):
                    self.plot(name)
                self.live_trading(name)
                save_hold_time_temp.append(self.save_time_hold)
                print(f'cumulative gain {round(self.cumlative_gained,4)}% after running {name}')
                sleep(1)
            # plt.figure()
            # plt.hist(save_hist,bins=100)
            # plt.show()
            # print(save_hold_time_temp)
            save_hist_no_nan = [x for x in save_hist if str(x) != 'nan']
            coeff_var_75, coeff_var_25 = percentile(save_hist_no_nan, 
                                        [75 ,25])
                
            self.lb_coef_deter = coeff_var_25
            self.ub_coef_deter = coeff_var_75
            print(f'LB coef determination {self.lb_coef_deter} : UP coef determination {self.ub_coef_deter}')
            iter_hold_pos = [item for sublist in save_hold_time_temp for item in sublist]
            try:
                iter_hold_pos_75,iter_hold_pos_25 = percentile(iter_hold_pos,[75 ,25])
                print(f'LB_iterations_held {iter_hold_pos_25} : UB_iterations_held {iter_hold_pos_75}')
            except:
                iter_hold_pos_75 = 76
                print(f'Use default hold time of {iter_hold_pos_75}, as percentile of the hold times could not be calculated')
            self.average_pos_hold = iter_hold_pos_75
            #print(f'3rd quartile iterations held {self.average_pos_hold}')
            print(iter_hold_pos_75 * SAMPLE_RATE, 'minutes held')
            self.cumlative_gained = float(0.0)
            print(f'% RAM USED: {virtual_memory()[2]}')
            if virtual_memory()[2] > 95:
                break
            sleep(SAMPLE_RATE*60)
def main():
    technical().run_analysis_pos_crypt()
if __name__ == "__main__":
    main()