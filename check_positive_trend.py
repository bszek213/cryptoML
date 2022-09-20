#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 16:00:51 2022

@author: bszekely
Crypto is garbae and if you run the code with a sample rate of anything less
than 240 minutes you will lose money. Crypto is too volatile and you 
need to look at long term regressions to see what is increasing and has the best
fit.
"""
from sklearn.linear_model import LinearRegression
import krakenex
from pykrakenapi import KrakenAPI
from numpy import array, zeros, nan, arange, percentile, empty
from time import sleep
import argparse
from os import path, getcwd, listdir, remove
from pandas import DataFrame, read_csv, date_range
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from os.path import join
import warnings
import buy_sell_signals
from datetime import datetime, timedelta
from scipy.signal import savgol_filter
warnings.filterwarnings("ignore")
def input_arg():
    global sample_rate
    global input_crypt
    global filter_val
    global filter_val_rsi
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--crypto", help = "crypto ID")
    parser.add_argument("-s", "--sample", help = "time frame interval minutes 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600")
    args = parser.parse_args()
    sample_rate = int(args.sample)
    input_crypt = args.crypto
    filter_val = 13
    filter_val_rsi = 31
    return args
def kraken_info():
    print('initialize kraken data')
    api = krakenex.API()
    api.load_key('key.txt')
    kraken = KrakenAPI(api)
    return kraken

def readin_cryptos():
    direct = getcwd()
    location = join(direct, 'crypto_trade_min.csv')
    df_crypto = read_csv(location)
    print(f' number of cryptos monitoring: {len(df_crypto)}')
    return df_crypto

def get_ohlc(crypt):
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
    api = krakenex.API()
    api.load_key('key.txt')
    kraken = KrakenAPI(api)
    ohlc = None
    while True:
        try:
            ohlc = kraken.get_ohlc_data(crypt, interval = sample_rate, since = 0,
                                        ascending = True) #returns two years of data7
        except Exception as e:
            print(f'getohlc() timed out from internet connection: {e}')
        if ohlc is not None:
            break
    # self.ohlc_no_param = ohlc[0]
    return ohlc[0]

def RSI(crypto_df):
    crypto_df['change'] = crypto_df.close.diff()
    # crypto_df['U'] = [x if x > 0 else 0 for x in crypto_df.change]
    # crypto_df['D'] = [abs(x) if x < 0 else 0 for x in crypto_df.change]
    crypto_df['U']  = crypto_df['change'].clip(lower=0)
    crypto_df['D'] = -1*crypto_df['change'].clip(upper=0)
    crypto_df['U'] = crypto_df.U.ewm(span=14,
               min_periods=13).mean()
    crypto_df['D'] = crypto_df.D.ewm(span=14,
               min_periods=13).mean()
    crypto_df['RS'] = crypto_df.U / crypto_df.D
    crypto_df['RSI'] = 100 - (100/(1+crypto_df.RS))
    # crypto_df['RSI'] = crypto_df['RSI'].ewm(span=25,min_periods=25-1).mean()
    return crypto_df

def volume_osc(crypto_df):
    """
    Volume Oscillator = [(Shorter Period SMA of Volume – Longer Period SMA of Volume)
                         / Longer Period SMA of Volume ] * 100
    """
    short = crypto_df['volume'].ewm(span=14,min_periods=13).mean() 
    long = crypto_df['volume'].ewm(span=28,min_periods=27).mean() 
    crypto_df['volume_os'] = ((short - long) / long) * 100
    #Filter
    sav_data =  savgol_filter(crypto_df['volume_os'].dropna().values, filter_val, 2)
    an_array = empty(len(crypto_df['volume_os']))
    an_array[:] = nan
    an_array[len(crypto_df['volume_os']) - len(sav_data):len(crypto_df['volume_os'])] = sav_data
    crypto_df['volume_os'] = an_array
    return crypto_df

def bollinger_band(crypto_df):
    crypto_df['typical_price'] = (crypto_df['close'] + crypto_df['high'] + crypto_df['low']) / 3
    crypto_df['TP_ewm'] = crypto_df['typical_price'].ewm(span=20,
                      min_periods=19).mean()
    crypto_df['std'] = crypto_df['TP_ewm'].ewm(span=20,
                      min_periods=19).std()
    crypto_df['upper_bound'] = crypto_df['TP_ewm']  + (2 * crypto_df['std'])
    crypto_df['lower_bound'] = crypto_df['TP_ewm']  - (2 * crypto_df['std'])
    return crypto_df
    
def awesome_indicator(inst_data):
    inst_data['median_price'] = (inst_data['high'] + inst_data['low']) / 2
    inst_data['long_ao'] = inst_data['median_price'].rolling(34,
                     min_periods=34-1).mean()
    inst_data['short_ao'] = inst_data['median_price'].rolling(5,
                     min_periods=5-1).mean()
    inst_data['ao'] = inst_data['short_ao'] - inst_data['long_ao']
    # per_change = zeros(len(inst_data['ao']))
    # for i in range(1,len(inst_data['ao'])):
    #     per_change[i] = (inst_data['ao'].iloc[i] - inst_data['ao'].iloc[i-1]) / inst_data['ao'].iloc[i-1]
    # inst_data['ao_velocity'] = per_change
    # inst_data['ao_velocity'] = inst_data['ao_velocity'].rolling(10).mean()
    return inst_data

def VWMA(crypto_df):
    crypto_df['typical_price'] = (crypto_df['high'] + crypto_df['low'] + crypto_df['close']) / 3
    crypto_df['price_volume'] = crypto_df['typical_price'] * crypto_df['volume']
    crypto_df['price_volume_sum'] = crypto_df['price_volume'].cumsum()
    crypto_df['volume_sum'] = crypto_df['volume'].cumsum()
    crypto_df['VMWA'] =  crypto_df['price_volume_sum'] / crypto_df['volume_sum']
    crypto_df['VMWA_28'] =  crypto_df['price_volume_sum'].rolling(28).mean() / crypto_df['volume_sum'].rolling(28).mean()
    crypto_df['VMWA_14'] =  crypto_df['price_volume_sum'].rolling(14).mean() / crypto_df['volume_sum'].rolling(14).mean()
    return crypto_df

def stoch_RSI(crypto_df):
    crypto_df = RSI(crypto_df)
    min_val  = crypto_df['RSI'].rolling(window=14, center=False).min()
    max_val = crypto_df['RSI'].rolling(window=14, center=False).max()
    crypto_df['Stoch_RSI'] = ((crypto_df['RSI'] - min_val) / (max_val - min_val)) * 100
    
    #FILTERING STEP
    try:
        sav_data =  savgol_filter(crypto_df['Stoch_RSI'].dropna().values, filter_val_rsi, 2)
        an_array = empty(len(crypto_df['Stoch_RSI']))
        an_array[:] = nan
        an_array[len(crypto_df['Stoch_RSI']) - len(sav_data):len(crypto_df['Stoch_RSI'])] = sav_data
        crypto_df['Stoch_RSI'] = an_array
    # crypto_df['Stoch_RSI'] = crypto_df['Stoch_RSI'].ewm(span=20,min_periods=20-1).mean() #I THINK I WILL NEED TO PLAY WITH THIS WINDOW MORE
    except:
        print('no filter was applied to Stoch_RSI')
    #get std of data
    q75, q25 = percentile(crypto_df['Stoch_RSI'].dropna().values, [75 ,25])
    iqr = q75 - q25
    lower_bound_buy = q25
    upper_bound_buy = q75
    # std_data = crypto_df['Stoch_RSI'].std()
    # lower_bound_buy = crypto_df['Stoch_RSI'].median() - (1.5 * std_data)
    # upper_bound_buy = crypto_df['Stoch_RSI'].median() + (1.5 * std_data)
    return crypto_df,lower_bound_buy,upper_bound_buy

def OBV(crypto_df_final,name='None'):
    """
    If the closing price of the asset is higher than the previous day?s closing price: 
    OBV = Previous OBV + Current Day Volume
    
    If the closing price of the asset is the same as the previous day?s closing price:
    OBV = Previous OBV (+ 0)

    If the closing price of the asset is lower than the previous day?s closing price:
    OBV = Previous OBV - Current Day's Volume
    """
    #TODO: add a linear regression lineover like 10-20 data points and use that 
    # as a buy signal if it is positive
    if crypto_df_final.empty == True:
        crypto_df_final = get_ohlc(name)
    crypto_df_final['OBV'] = zeros(len(crypto_df_final))
    # crypto_df_final['OBV'].iloc[0] = crypto_df_final['volume'].iloc[0]
    OBV_iter = crypto_df_final['volume'].iloc[0]
    crypto_df_final['OBV'].iloc[0] = OBV_iter
    for i in range(1,len(crypto_df_final['OBV'])):
        if (crypto_df_final['close'].iloc[i-1] < crypto_df_final['close'].iloc[i]):
            OBV_iter += crypto_df_final['volume'].iloc[i]
        if (crypto_df_final['close'].iloc[i-1] > crypto_df_final['close'].iloc[i]):
            OBV_iter -= crypto_df_final['volume'].iloc[i]
        if (crypto_df_final['close'].iloc[i-1] == crypto_df_final['close'].iloc[i]):
            OBV_iter += 0
        crypto_df_final['OBV'].iloc[i] = OBV_iter

    #linear regression
    data_len = int(len(crypto_df_final) / 4) #quarter of the data
    a_list = list(arange(len(crypto_df_final)-data_len,len(crypto_df_final)))
    X1 = array(a_list)
    X = X1.reshape(-1, 1)
    reg = LinearRegression().fit(X, crypto_df_final['OBV'].iloc[-data_len-1:-1].values)

    #create an array  of linear regression - short 
    X1_half = arange(len(crypto_df_final)-data_len,len(crypto_df_final))
    reg_arr_half = zeros(len(crypto_df_final))
    for i in X1_half:
        reg_arr_half[i] = (reg.coef_ * i) + reg.intercept_
    rval_reg =  reg_arr_half[reg_arr_half != 0]
    reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
    rval, pval = pearsonr(rval_reg, crypto_df_final['close'].iloc[-data_len-1:-1].values)
    
    #calc OBV bounds 
    q75, q25 = percentile(crypto_df_final['OBV'].dropna().values, [75 ,25])
    lower_bound_buy = q25
    upper_bound_buy = q75
    if name != 'None':
        return rval, reg.coef_
    else:
        return crypto_df_final,reg.coef_,reg_arr_half, lower_bound_buy, upper_bound_buy, rval

def macd(crypto_df_final):
    crypto_df_final['sma_1'] = crypto_df_final['close'].ewm(span=26,
                      min_periods=26-1).mean()
    crypto_df_final['sma_2'] = crypto_df_final['close'].ewm(span=12,
                     min_periods=12-1).mean()
    crypto_df_final['macd_diff'] = crypto_df_final['sma_2'] - crypto_df_final['sma_1']
    #filter the MACD diff line
    sav_data =  savgol_filter(crypto_df_final['macd_diff'].dropna().values, filter_val, 2)
    an_array = empty(len(crypto_df_final['macd_diff']))
    an_array[:] = nan
    an_array[len(crypto_df_final['macd_diff']) - len(sav_data):len(crypto_df_final['macd_diff'])] = sav_data
    crypto_df_final['macd_diff'] = an_array
    crypto_df_final['signal_line'] = crypto_df_final['macd_diff'].ewm(span=9,
                     min_periods=9-1).mean()
    return crypto_df_final

def sell_percentage(name,bought,crypto_list):
    api = krakenex.API()
    api.load_key('key.txt')
    kraken = KrakenAPI(api)
    bid_price = float(kraken.get_ticker_information(name)['b'][0][0])
    threshold = bought + (bought * 0.007)
    print(f'bid: {bid_price} | threshod: {threshold}')
    if bid_price >= threshold:
        old_name = name.replace('USD','')
        ind_cryp_t = crypto_list[crypto_list['crypto'] == old_name]
        volume_inst = ind_cryp_t['Order'].values
        kraken = kraken_info()
        balance = kraken.get_account_balance()
        open_pos, i = buy_sell_signals.basic_sell(name, 
                                                  kraken, 
                                                  volume_inst[0], 
                                                  balance)
        bought = False 
        open_pos = True
    else:
        bought = True 
        open_pos = False
    return bought, open_pos
def buy_find(inst_data,name):
    font = {'family' : 'DejaVu Sans',
        'weight' : 'bold',
        'size'   : 10}
    plt.rc('font', **font)
    print('==================')
    # print(name)
    #all data
    a_list = list(range(0, len(inst_data.close))) 
    X1 = array(a_list)
    X = X1.reshape(-1, 1)
    reg = LinearRegression().fit(X, inst_data.close.values)
    reg_arr = zeros(len(inst_data.close))
    for i in range(len(inst_data.close)):
        reg_arr[i] = (reg.coef_ * i) + reg.intercept_
    rval, pval = pearsonr(reg_arr, inst_data.close.values)
    if sample_rate <=60:
        #half data 
        half_data = int(len(inst_data.close.values) / 2)
        X1_half = X1[-half_data:-1]
        X_half = X1_half.reshape(-1,1)
        half_close = inst_data.iloc[-half_data:-1].close.values
        reg_half = LinearRegression().fit(X_half, half_close)
        reg_arr_half = zeros(len(reg_arr))
        for i in X1_half:
            reg_arr_half[i+1] = (reg_half.coef_ * i) + reg_half.intercept_
        reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
    else:
        #quarter data 
        half_data = int(len(inst_data.close.values) / 4)
        X1_half = X1[-half_data:-1]
        X_half = X1_half.reshape(-1,1)
        half_close = inst_data.iloc[-half_data:-1].close.values
        reg_half = LinearRegression().fit(X_half, half_close)
        reg_arr_half = zeros(len(reg_arr))
        for i in X1_half:
            reg_arr_half[i+1] = (reg_half.coef_ * i) + reg_half.intercept_
        reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
    inst_data['ewmshort'] = inst_data['close'].ewm(span=50, min_periods=50).mean()
    inst_data['ewmmedium'] = inst_data['close'].ewm(span=128, min_periods=128).mean()
    inst_data['ewmlong'] = inst_data['close'].ewm(span=200, min_periods=200).mean()
    inst_data,lower_bound_buy,upper_bound_buy = stoch_RSI(inst_data)
    inst_data = macd(inst_data)
    inst_data = awesome_indicator(inst_data)
    inst_data = VWMA(inst_data)
    inst_data = volume_osc(inst_data)
    inst_data = bollinger_band(inst_data)
    inst_data, coeff_OBV, reg_array, OBV_lower, OBV_upper, OBV_rval = OBV(inst_data)
    # inst_data['ewm20'] = inst_data['close'].ewm(span=20, min_periods=20).mean()
    inst_data['LR'] = reg_arr
    inst_data['LR_half'] = reg_arr_half
    inst_data['buy'] = zeros(len(inst_data['close']))
    inst_data['sell'] = zeros(len(inst_data['close']))
    open_pos = False
    percent_gain = 0
    buy_price= 0
    for o in range(len(inst_data)):
        #TODO maybe add another condition where the closing price has to be above the LR line
        if ((inst_data['macd_diff'].iloc[o-1] < inst_data['signal_line'].iloc[o-1]) and
            (inst_data['macd_diff'].iloc[o] > inst_data['signal_line'].iloc[o]) and
            (inst_data['Stoch_RSI'].iloc[o] > inst_data['Stoch_RSI'].iloc[o-2]) and
            (inst_data['macd_diff'].iloc[o] < 0)
            # (inst_data['Stoch_RSI'].iloc[o] < upper_bound_buy)
            # (inst_data['VMWA_14'].iloc[o] > inst_data['VMWA_28'].iloc[o]) and
            # (inst_data['volume_os'].iloc[o] > 0) and
            # (inst_data['volume_os'].iloc[o] > inst_data['volume_os'].iloc[o-1]) and
            # (inst_data['macd_diff'].iloc[o-1] < inst_data['macd_diff'].iloc[o]) and
            # (inst_data['ewm75'].iloc[o] < inst_data['LR_half'].iloc[o]) and 
            # (inst_data['ewm150'].iloc[o] < inst_data['LR_half'].iloc[o]) and
            # (inst_data['close'].iloc[o] < inst_data['LR_half'].iloc[o]) and
            # (inst_data['Stoch_RSI'].iloc[o] < lower_bound_buy) and 
            # open_pos == False
            ):
            if ((inst_data['ewmshort'].iloc[o]) <= (inst_data['close'].iloc[o]) or
            (inst_data['ewmlong'].iloc[o]) <= (inst_data['close'].iloc[o]) or
            (inst_data['ewmmedium'].iloc[o]) <= (inst_data['close'].iloc[o])):
                inst_data['buy'].iloc[o] = inst_data['close'].iloc[o]
                # cross_buy= False
                # for i in range(o-10,o):
                #     if (inst_data['Stoch_RSI'].iloc[o] < lower_bound_buy):
                #         cross_buy= True
                # if cross_buy == True:
                #     inst_data['buy'].iloc[o] = inst_data['close'].iloc[o]
                #     buy_price = inst_data['close'].iloc[o]
                #     cross_buy= False
                # else:
                #     inst_data['buy'].iloc[o] = nan
            else:
                inst_data['buy'].iloc[o] = nan
        else:
            inst_data['buy'].iloc[o] = nan
        if ((inst_data['macd_diff'].iloc[o-1] > inst_data['signal_line'].iloc[o-1]) and
            (inst_data['macd_diff'].iloc[o] < inst_data['signal_line'].iloc[o]) and
            (inst_data['VMWA_14'].iloc[o] > inst_data['VMWA_28'].iloc[o]) and 
            # (inst_data['Stoch_RSI'].iloc[o] > upper_bound_buy) and
            (inst_data['macd_diff'].iloc[o] > 0)):
            cross_sell = False
            for i in range(o-4,o):
                if (inst_data['Stoch_RSI'].iloc[i] > upper_bound_buy):
                    cross_sell = True
            if cross_sell == True:
                inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
            # inst_data['sell'].iloc[o] = nan
            # open_pos = False
                temp_price = ((inst_data['sell'].iloc[o] - buy_price) / buy_price) * 100
                percent_gain += (temp_price)
                cross_sell = False
            else:
                inst_data['sell'].iloc[o] = nan
        else:
            inst_data['sell'].iloc[o] = nan
    inst_data.index = arange(0,len(inst_data.index))
    find_closet_buy = inst_data[inst_data['buy'].notnull()]
    find_closet_sell = inst_data[inst_data['sell'].notnull()]
    
    #calculate time for index
    periods = ((sample_rate * len(inst_data['close'])) / 60)
    start_date = datetime.now() - timedelta(hours=int(periods))
    date_range_arr = date_range(start=start_date, end=datetime.now(),periods=len(inst_data['close']))
    inst_data.index = date_range_arr
    
    # fig, ax = plt.subplots(1,1,figsize=(10, 5), dpi=150) 
    fig, ax = plt.subplots(5,1,figsize=(12, 15), dpi=250) 
    title_name = name + ' LR R-val: ' + str(rval) + ' LR_half: ' + str(reg_half.coef_)
    # LR and closing price plot
    ax[0].set_title(title_name)
    ax[0].plot(inst_data.index,inst_data['close'],'tab:blue', marker="o",
               markersize=1, linestyle='', label = 'Close Price')
    ax[0].plot(inst_data.index, inst_data['ewmlong'], 'black', label = 'long')
    ax[0].plot(inst_data.index, inst_data['ewmshort'], 'crimson', label = 'short')
    ax[0].plot(inst_data.index, inst_data['ewmmedium'], 'green', label = 'medium')
    ax[0].plot(inst_data.index, inst_data['LR'], 'blue', label = 'LR_full')
    ax[0].plot(inst_data.index, inst_data['LR_half'], 'lime', label = 'LR_half')
    ax[0].scatter(inst_data.index, inst_data['buy'], marker='o', s=120, color = 'g', label = 'buy')
    ax[0].scatter(inst_data.index, inst_data['sell'], marker='o',s=120, color = 'k', label = 'sell')
    ax[0].fill_between(inst_data.index, inst_data.upper_bound, inst_data.lower_bound, color='grey',
                      alpha=0.4)
    ax[0].legend()
    ax[0].grid(True)
    #MACD PLOT
    ax[1].plot(inst_data.index, inst_data['macd_diff'], 'tab:green', marker="o",
                        markersize=2, linestyle='-', label = 'macd diff')
    ax[1].plot(inst_data.index, inst_data['signal_line'], 'tab:red', marker="o",
                        markersize=2, linestyle='-', label = 'signal line')
    ax[1].hlines(y = 0, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    ax[1].legend()
    ax[1].grid(True)
    ax[1].set_xlabel('iterations')
    ax[1].set_ylabel('MACD Values')
    #STOCH RSI
    ax[2].plot(inst_data.index, inst_data['Stoch_RSI'], 'r', marker="o", markersize=2, linestyle='-',
                linewidth= 0.25, label = 'Stoch_RSI')
    # ax[2].plot(inst_data.index, inst_data['Stoch_RSI_D'], 'tab:blue', marker="o", markersize=2, linestyle='-',
    #             linewidth= 0.25, label = 'Stoch_RSI_D')
    ax[2].hlines(y = lower_bound_buy, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    ax[2].hlines(y = upper_bound_buy, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    # ax[2].fill_between(inst_data.index, 80, 50, color='grey',
    #                   alpha=0.3)
    ax[2].legend()
    ax[2].set_xlabel('iterations')
    ax[2].set_ylabel('RSI Values')
    ax[2].grid(True)
    #VWMA INDICATOR
    # ax[3].plot(inst_data.index, inst_data['VMWA_28'], 'b', marker="o", markersize=2, linestyle='-',
    #             linewidth= 0.25, label = 'VMWA_28')
    # ax[3].plot(inst_data.index, inst_data['VMWA_14'], 'r', marker="o", markersize=2, linestyle='-',
    #             linewidth= 0.25, label = 'VMWA_14')
    # # ax[3].hlines(y = 0, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    # ax[3].legend()
    # # ax[3].set_xlabel('iterations')
    # ax[3].set_ylabel('VWMA Values')
    # ax[3].grid(True)
    #OBV INDICATOR
    ax[3].plot(inst_data.index, inst_data['OBV'], 'b', marker="o", markersize=2, linestyle='-',
                linewidth= 0.25, label = 'OBV')
    ax[3].plot(inst_data.index, reg_array, 'r',marker="o", markersize=2, linestyle='-',
                linewidth= 0.25, label = 'OBV Reg Array')
    ax[3].hlines(y = 0, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    ax[3].hlines(y = OBV_lower, xmin=inst_data.index[0], xmax=inst_data.index[-1],colors='red')
    ax[3].hlines(y = OBV_upper, xmin=inst_data.index[0], xmax=inst_data.index[-1],colors='red')
    ax[3].legend()
    title_name = f'OBV Coeff: {coeff_OBV} | OBV r: {OBV_rval}'
    ax[3].set_title(title_name)
    ax[3].set_xlabel('iterations')
    ax[3].set_ylabel('OBV Values')
    ax[3].grid(True)
    # VOLUME OSCILLATOR
    ax[4].plot(inst_data.index, inst_data['volume_os'], 'r' ,marker="o", markersize=2, linestyle='-',
                linewidth= 0.25, label = 'VOLUME OSCILLATOR')
    ax[4].hlines(y = 0, xmin=inst_data.index[0], xmax=inst_data.index[-1])
    ax[4].legend()
    ax[4].set_xlabel('iterations')
    ax[4].set_ylabel('volume_os Values')
    ax[4].grid(True)
    save_name = name + '.svg'
    direct = getcwd()
    final_dir = join(direct, 'lin_regress_plots', save_name)
    plt.tight_layout()
    plt.savefig(final_dir,dpi=300)
    plt.close()
    try: 
        nearest_buy = find_closet_buy.index[-1]
        diff_buy = len(inst_data) - nearest_buy
        buy_price_val = find_closet_buy['buy'].iloc[-1]
    except:
        nearest_buy = 0
        buy_price_val = 0
        diff_buy = 301
    try:
        nearest_sell = find_closet_sell.index[-1]
    except:
        nearest_sell = 0
        
    if diff_buy <= 2:
        return nearest_sell, name, nearest_buy, 'buy', buy_price_val
    else:
        return nearest_sell, name, nearest_buy, 'do not buy', buy_price_val

def track_sell(name):#,buy_init
    inst_data = get_ohlc(name)
    print(f' track_sell is currently monitoring: {name}')
    a_list = list(range(0, len(inst_data.close))) 
    #all data
    X1 = array(a_list)
    X = X1.reshape(-1, 1)
    reg = LinearRegression().fit(X, inst_data.close.values)
    reg_arr = zeros(len(inst_data.close))
    for i in range(len(inst_data.close)):
        reg_arr[i] = (reg.coef_ * i)+ reg.intercept_
    if sample_rate <=60:
        #half data 
        half_data = int(len(inst_data.close.values) / 2)
        X1_half = X1[-half_data:-1]
        X_half = X1_half.reshape(-1,1)
        half_close = inst_data.iloc[-half_data:-1].close.values
        reg_half = LinearRegression().fit(X_half, half_close)
        reg_arr_half = zeros(len(reg_arr))
        for i in X1_half:
            reg_arr_half[i+1] = (reg_half.coef_ * i) + reg_half.intercept_
        reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
    else:
        #quarter data 
        half_data = int(len(inst_data.close.values) / 4)
        X1_half = X1[-half_data:-1]
        X_half = X1_half.reshape(-1,1)
        half_close = inst_data.iloc[-half_data:-1].close.values
        reg_half = LinearRegression().fit(X_half, half_close)
        reg_arr_half = zeros(len(reg_arr))
        for i in X1_half:
            reg_arr_half[i+1] = (reg_half.coef_ * i) + reg_half.intercept_
        reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
    inst_data['ewm150'] = inst_data['close'].ewm(span=26, min_periods=26).mean()
    inst_data['ewm75'] = inst_data['close'].ewm(span=12, min_periods=12).mean()
    inst_data,lower_bound_buy,upper_bound_buy = stoch_RSI(inst_data)
    inst_data = macd(inst_data)
    inst_data = awesome_indicator(inst_data)
    inst_data = VWMA(inst_data)
    inst_data['LR'] = reg_arr
    inst_data['LR_half'] = reg_arr_half
    inst_data['buy'] = zeros(len(inst_data['close']))
    inst_data['sell'] = zeros(len(inst_data['close']))
    open_pos = False
    percent_gain = 0
    buy_price= 0
    # sell_price_ = buy_init + (buy_init * 1.05)

    for o in range(len(inst_data)):
        if ((inst_data['macd_diff'].iloc[o-1] < inst_data['signal_line'].iloc[o-1]) and
            (inst_data['macd_diff'].iloc[o] > inst_data['signal_line'].iloc[o]) and
            (inst_data['VMWA_14'].iloc[o] > inst_data['VMWA_28'].iloc[o]) and
            (inst_data['macd_diff'].iloc[o] < 0) 
            ):
            # inst_data['buy'].iloc[o] = inst_data['close'].iloc[o]
            inst_data['buy'].iloc[o] = nan
            # open_pos = True
            buy_price = inst_data['close'].iloc[o]
        else:
            inst_data['buy'].iloc[o] = nan
        if ((inst_data['macd_diff'].iloc[o-1] > inst_data['signal_line'].iloc[o-1]) and
            (inst_data['macd_diff'].iloc[o] < inst_data['signal_line'].iloc[o]) and
            (inst_data['VMWA_14'].iloc[o] > inst_data['VMWA_28'].iloc[o]) and 
            # (inst_data['Stoch_RSI'].iloc[o] > upper_bound_buy) and
            (inst_data['macd_diff'].iloc[o] > 0)):
            cross_sell = False
            for i in range(o-4,o):
                if (inst_data['Stoch_RSI'].iloc[i] > upper_bound_buy):
                    cross_sell = True
            if cross_sell == True:
                inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
            # inst_data['sell'].iloc[o] = nan
            # open_pos = False
                temp_price = ((inst_data['sell'].iloc[o] - buy_price) / buy_price) * 100
                percent_gain += (temp_price)
                cross_sell = False
            else:
                inst_data['sell'].iloc[o] = nan
        else:
            inst_data['sell'].iloc[o] = nan
        # elif (reg.coef_ < 0): 
        #     inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
        #     # open_pos = False
        #     temp_price = ((inst_data['sell'].iloc[o] - buy_price) / buy_price) * 100
        #     percent_gain += (temp_price)
        # elif (reg_half.coef_ < 0): 
        #     inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
        #     # open_pos = False
        #     temp_price = ((inst_data['sell'].iloc[o] - buy_price) / buy_price) * 100
        #     percent_gain += (temp_price)
        # elif inst_data['close'].iloc[o] > sell_price_:
        #     inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
        #     temp_price = ((inst_data['sell'].iloc[o] - buy_price) / buy_price) * 100
        #     percent_gain += (temp_price)
        # elif ((inst_data['ewm75'].iloc[o-1] > inst_data['ewm150'].iloc[o-1]) and
        #     (inst_data['ewm75'].iloc[o] < inst_data['ewm150'].iloc[o]) and
        #     (inst_data['ewm75'].iloc[o] < inst_data['LR'].iloc[o]) and 
        #     (inst_data['ewm150'].iloc[o] < inst_data['LR'].iloc[o])):
        #     inst_data['sell'].iloc[o] = inst_data['close'].iloc[o]
    inst_data.index = arange(0,len(inst_data.index))
    find_closet_buy = inst_data[inst_data['buy'].notnull()]
    find_closet_sell = inst_data[inst_data['sell'].notnull()]
    # print('threshold sell price: ',sell_price_)
    print('Current price: ',inst_data['close'].iloc[-1])
    try:
        nearest_sell = find_closet_sell.index[-1]
        diff_sell = len(inst_data) - nearest_sell
        if diff_sell <= 2:
            return 'sell'
    except:
        nearest_sell = 10
        return 'do not sell'

def main():
    args =  input_arg()
    while True:
        positive_cryptos = []
        crypto_beta = []
        r_val = []
        p_val = []
        positive_cryptos_half = []
        crypto_beta_half = []
        r_val_half = []
        p_val_half = []
        if input_crypt:
            df_empty = DataFrame({'A' : []})
            rval_obv, reg_obv = OBV(df_empty,input_crypt)
            sell_not, name, find_closet, buy_not, buy_price = buy_find(get_ohlc(input_crypt),input_crypt)
            print(f'name: {name} | buy condition: {buy_not} | nearest_buy: {find_closet} | buy_price: {buy_price}| OBV_reg: {reg_obv}')
            print(f'checking {input_crypt} individually')
            break
        crypto_list = readin_cryptos()
        for name in crypto_list['crypto']:
            name = name +'USD'
            # print(f'current crypto: {name}')
            crypto_df = get_ohlc(name)
            a_list = list(range(0, len(crypto_df.close))) 
            X1 = array(a_list)
            X = X1.reshape(-1, 1)
            reg = LinearRegression().fit(X, crypto_df.close.values)
            reg_arr = zeros(len(crypto_df.close))
            for i in range(len(crypto_df.close)):
                reg_arr[i] = (reg.coef_ * i) + reg.intercept_
            rval, pval = pearsonr(reg_arr, crypto_df.close.values)
            #across all the data
            if  rval > 0.70 and reg.coef_ > 0:
                positive_cryptos.append(name)
                crypto_beta.append(reg.coef_[0])
                r_val.append(rval)
                p_val.append(pval)
            #IF USING LONGER INTERVALS LOOK AT TRENDS ACROSS SHORTER WINDOWS
            if sample_rate <= 60:
                #ACROSS HALF THE DATA
                half_data = int(len(crypto_df.close.values) / 2)
                X1_half = X1[-half_data:-1]
                X_half = X1_half.reshape(-1,1)
                half_close = crypto_df.iloc[-half_data:-1].close.values
                reg_half = LinearRegression().fit(X_half, half_close)
                reg_arr_half = zeros(len(X1_half))
                m = 0
                for i in X1_half:
                    reg_arr_half[m] = (reg_half.coef_ * i) + reg_half.intercept_
                    m+=1
                # reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
                rval_half, pval_half= pearsonr(reg_arr_half, half_close)
            else:
                #ACROSS QUARTER THE DATA
                half_data = int(len(crypto_df.close.values) / 4)
                X1_half = X1[-half_data:-1]
                X_half = X1_half.reshape(-1,1)
                half_close = crypto_df.iloc[-half_data:-1].close.values
                reg_half = LinearRegression().fit(X_half, half_close)
                reg_arr_half = zeros(len(X1_half))
                m = 0
                for i in X1_half:
                    reg_arr_half[m] = (reg_half.coef_ * i) + reg_half.intercept_
                    m+=1
                # reg_arr_half = [nan if x == 0 else x for x in reg_arr_half]
                rval_half, pval_half= pearsonr(reg_arr_half, half_close)
            if  rval_half > 0.70 and reg_half.coef_ > 0: #reg.coef_
                positive_cryptos_half.append(name)
                crypto_beta_half.append(reg_half.coef_[0])
                r_val_half.append(rval_half)
                p_val_half.append(pval_half)

        crypto_df = DataFrame(zip(positive_cryptos, crypto_beta, r_val, p_val),
                              columns=['crypto','beta', 'R', 'p_value'])
        crypto_df = crypto_df.sort_values(by=['R','beta'], ascending=True)
        
        crypto_df_half = DataFrame(zip(positive_cryptos_half, crypto_beta_half, r_val_half, p_val_half),
                              columns=['crypto','beta', 'R', 'p_value'])
        crypto_df_half = crypto_df_half.sort_values(by=['R','beta'], ascending=True)
        print('=================================================')
        print('ALL CRYPTO WITH R > 0.70 ACROSS ALL SAMPLING POINTS')
        print(f'{crypto_df}')
        print('=================================================')
        if sample_rate <= 60:
            print('ALL CRYPTO WITH R > 0.70 ACROSS HALF SAMPLING POINTS')
            crypto_df_half = crypto_df_half[crypto_df_half['R'] > 0.70] #strong correlation
            print(f'{crypto_df_half}')
        else:
            print('ALL CRYPTO WITH R > 0.70 ACROSS QUARTER SAMPLING POINTS')
            crypto_df_half = crypto_df_half[crypto_df_half['R'] > 0.70] #strong correlation
            print(f'{crypto_df_half}')
        print('=================================================')
        #delete old plots
        direct = getcwd()
        final_dir = join(direct, 'lin_regress_plots')
        for f in listdir(final_dir):
            remove(join(final_dir, f))
        #plot function#
        file_loc = path.join(getcwd(), "lin_regress_plots", "positive_trend.csv")
        crypto_df.to_csv(file_loc)
        bought = False
        buy_crypt = 'place_holder'
        #Buy sell crypto
        for name in crypto_df_half['crypto']:
            #only use the OBV regression for time intervals less than 60 minutes
            # if sample_rate <= 60:
            df_empty = DataFrame({'A' : []})
            rval_obv, reg_obv = OBV(df_empty,name)
            if reg_obv > 0 and rval_obv > 0.5:
                sell_not, name, find_closet, buy_not, buy_price = buy_find(get_ohlc(name),name)
                print(f'name: {name} | buy condition: {buy_not} | nearest_buy: {find_closet} | buy_price: {buy_price}')
                print(f'OBV rval: {rval_obv} | OBV_reg: {reg_obv}')
                print('==================')
                if buy_not == "buy":
                    buy_crypt = name
            # else:
            #     sell_not, name, find_closet, buy_not, buy_price = buy_find(get_ohlc(name),name)
            #     print(f'name: {name} | buy condition: {buy_not} | nearest_buy: {find_closet} | buy_price: {buy_price}')
            #     print('==================')
            #     if buy_not == "buy":
            #         buy_crypt = name
        if buy_crypt == 'place_holder':
            print('no crypto is in the buy condition')
            print(f'bought condition: {bought}')
        if buy_crypt != 'place_holder' and bought == False:
            print('buy condition met, buy: ', buy_crypt)
            old_name = buy_crypt.replace('USD','')
            ind_cryp_t = crypto_list[crypto_list['crypto'] == old_name]
            volume_inst = ind_cryp_t['Order'].values
            kraken = kraken_info()
            balance = kraken.get_account_balance()
            open_pos, MATI_ask, traded = buy_sell_signals.buy_signal_hft(buy_crypt, 
                                                                 kraken, 
                                                                 volume_inst[0], 
                                                                 balance.vol['ZUSD'])
            if traded == False:
                bought = False
                open_pos == True
                buy_not = 'do not buy'
            else:
                buy_price_init = float(kraken.get_ticker_information(buy_crypt)['a'][0][0])
                bought = True
                open_pos == False
        while bought == True and open_pos == False:
            direct = getcwd()
            final_dir = join(direct, 'lin_regress_plots')
            for f in listdir(final_dir):
                remove(join(final_dir, f))
            sell_or_not = track_sell(buy_crypt)
            print(f'sell condition: {sell_or_not}')
            # Only use the percentage sell on short term time intervals
            if sample_rate <=60:
                bought, open_pos = sell_percentage(buy_crypt,buy_price_init,crypto_list)
            buy_find(get_ohlc(buy_crypt),buy_crypt)
            if sell_or_not == 'sell':
                print('sell condition met ')
                kraken = kraken_info()
                balance = kraken.get_account_balance()
                open_pos, i = buy_sell_signals.basic_sell(buy_crypt, 
                                                          kraken, 
                                                          volume_inst[0], 
                                                          balance)
                bought = False
                break
            elif sell_or_not == 'do not sell':
                bought = True
                open_pos = False
                print('sell condition not met')
                print(f'bought condition: {bought}')
            # visualize(buy_crypt)
            print(f'Pause for {sample_rate} minutes')
            time_secs = sample_rate*60
            while time_secs:
                mins, secs = divmod(time_secs,60)
                timeformat = '{:02d}:{:02d}'.format(mins,secs)
                print(timeformat, end='\r')
                sleep(1)
                time_secs -= 1
            
            
        #buy sell individual crypto
        # if input_crypt:
        #     direct = getcwd()
        #     final_dir = join(direct, 'lin_regress_plots')
        #     for f in listdir(final_dir):
        #         remove(join(final_dir, f))
        #     sell_not, name, find_closet, buy_not, buy_price = buy_find(get_ohlc(input_crypt),input_crypt)
        #     sell_or_not = track_sell(input_crypt,10000000000) #10000000000 is a placeholder value until I figure out what I want to do here
        #     sell_percentage(input_crypt,buy_price,crypto_list)
        #     if sell_or_not == 'sell':
        #         print(f'sell {input_crypt}')
        #         old_name = input_crypt.replace('USD','')
        #         ind_cryp_t = crypto_list[crypto_list['crypto'] == old_name]
        #         volume_inst = ind_cryp_t['Order'].values
        #         kraken = kraken_info()
        #         balance = kraken.get_account_balance()
        #         open_pos, i = buy_sell_signals.basic_sell(input_crypt, 
        #                                                   kraken, 
        #                                                   volume_inst[0], 
        #                                                   balance)
        #     else:
        #         print(f'do not sell {input_crypt}')
        #find what crypto to buy
        # else:
        print('no crypto is in the buy condition, sanity check')  
        time_secs = sample_rate*60
        while time_secs:
            mins, secs = divmod(time_secs,60)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            print(timeformat, end='\r')
            sleep(1)
            time_secs -= 1

if __name__ == "__main__":
    main()
