#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Candlestick analysis yFinance
@author: bszekely
"""
import yfinance as yf
from os import getcwd, path, mkdir, remove
from pandas import read_csv
from timeit import default_timer
import plotly.graph_objects as go
import krakenex
from pykrakenapi import KrakenAPI
from technical_analysis import stoch_RSI
# def kraken_info():
#     print('initialize kraken data')
#     api = krakenex.API()
#     api.load_key('key.txt')
#     kraken = KrakenAPI(api)
#     return kraken
def get_ohlc(crypt,sample_rate=1440):
    """
    Parameters
    ----------
    kraken : Kraken object
        DESCRIPTION.
    crypt : crypto str name
        DESCRIPTION.
    inter : int variable - sampling window
        time frame interval minutes 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600.
        ((((((((((((((((((sampling time in UTC time zone))))))))))))))))))
    Returns
    -------
    Pandas df 
        close, high, low prices.
    """
    if crypt == "APE3":
        crypt = "APE"
    if crypt == "LUNA1":
        crypt = "LUNA"
    crypt = crypt + 'USD'
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
def set_data(crypt):
    # crypt_name = sys.argv[1] + '-USD'
    crypt_name = crypt + '-USD'
    temp = yf.Ticker(crypt_name)
    history = temp.history(period = 'max', interval="1d")
    return history
def set_crypt_names():
    location = getcwd()
    df = read_csv(path.join(location,'crypto_trade_min.csv'))
    df.sort_values(by=['crypto'],inplace=True)
    return df['crypto']
def create_candlestick(crypt,ohlc):
    # data.loc[ohlc.iloc[-1].name] = [ohlc['open'].iloc[-1],
    #                                 ohlc['high'].iloc[-1],
    #                                 ohlc['low'].iloc[-1],
    #                                 ohlc['close'].iloc[-1],
    #                                 ohlc['volume'].iloc[-1],
    #                                 0,0]
    direct = getcwd()
    check_folder = path.join(direct,'candlestick_figures')
    name = crypt + '_candlestick.png'
    if path.exists(check_folder):
        final_dir = path.join(check_folder, name)
    else:
        mkdir(check_folder)
        final_dir = path.join(check_folder, name)
    # fig = go.FigureWidget(go.Candlestick(x=data.index,
    #                                      open=data['Open'],
    #                                      high=data['High'],
    #                                      low=data['Low'],
    #                                      close=data['Close']))
    
    if len(ohlc.index) > 30:
        dates_index = ohlc.index[-30::]
        open_data = ohlc['open'].iloc[-30::]
        high_data = ohlc['high'].iloc[-30::]
        low_data = ohlc['low'].iloc[-30::]
        close_data = ohlc['close'].iloc[-30::]
        start = min(ohlc['low'].iloc[-30::])
        end = max(ohlc['high'].iloc[-30::])
    else:
        dates_index = ohlc.index[-10::]
        open_data = ohlc['open'].iloc[-10::]
        high_data = ohlc['high'].iloc[-10::]
        low_data = ohlc['low'].iloc[-10::]
        close_data = ohlc['close'].iloc[-10::]
        start = min(ohlc['low'].iloc[-10::])
        end = max(ohlc['high'].iloc[-10::])

    fig = go.FigureWidget(go.Candlestick(x=dates_index,
                                      open=open_data,
                                      high=high_data,
                                      low=low_data,
                                      close=close_data))
    fig.update_yaxes(range=[start, end])
    fig.update_layout(title=crypt,
                      margin=dict(l=50,r=50,b=100,t=100,pad=4),
                      xaxis_rangeslider_visible=False,
                      yaxis_title='Price USD')
    fig.write_image(final_dir,scale=2)
    # except:
    #     print(f'{crypt} candlestick cannot be created')
    
def analysis_candlestick(ohlc,crypt):
    text_file = open('candlestick_output.txt','a')
    engulf_out = bullish_engulf(ohlc)
    inv_hammer_out = inverted_hammer_bullish(ohlc)
    morning_star_out = morning_star(ohlc)
    pierce_line_out = piercing_line(ohlc)
    three_soldiers_out = three_white_soldiers(ohlc)
    if engulf_out == True:
        with open("candlestick_output.txt", "a") as text_file:
            string_out = f'{crypt} bullish bullish engulf pattern'
            # text_file.write("bullish engulf pattern: %c" % (crypt))
            text_file.write(string_out)
            text_file.write("\n")
        # string_out = f'{crypt} bullish as denoted by bullish engulf pattern'
        # text_file.write(string_out)
        print(f'{crypt} bullish - engulf pattern')
    if inv_hammer_out == True:
        with open("candlestick_output.txt", "a") as text_file:
            string_out = f'{crypt} bullish - inverted hammer  pattern'
            text_file.write(string_out)
            text_file.write("\n")
        # string_out = f'{crypt} bullish as denoted by bullish inverted hammer bullish pattern'
        # text_file.write(string_out)
        print(f'{crypt} bullish - inverted hammer bullish pattern')
    if morning_star_out == True:
        with open("candlestick_output.txt", "a") as text_file:
            string_out = f'{crypt} bullish - morning star pattern'
            text_file.write(string_out)
            text_file.write("\n")
            print(string_out)
    if pierce_line_out == True:
        with open("candlestick_output.txt", "a") as text_file:
            string_out = f'{crypt} bullish - piercing line pattern'
            text_file.write(string_out)
            text_file.write("\n")
            print(string_out)
    if three_soldiers_out == True:
        with open("candlestick_output.txt", "a") as text_file:
            string_out = f'{crypt} bullish - three white soldiers pattern'
            text_file.write(string_out)
            text_file.write("\n")
            print(string_out)
    # text_file.close()
    
def bullish_engulf(crypto_df):
    if ((crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-2]) and
        (crypto_df['open'].iloc[-1] < crypto_df['close'].iloc[-2])
        and (crypto_df['high'].iloc[-1] > crypto_df['high'].iloc[-2]) and 
        (crypto_df['low'].iloc[-1] < crypto_df['low'].iloc[-2])):
        return True
    else:
        return False
def inverted_hammer_bullish(crypto_df):
    if ((crypto_df['close'].iloc[-3] < crypto_df['open'].iloc[-3]) and
        (crypto_df['close'].iloc[-2] < crypto_df['open'].iloc[-2]) and
        (crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-1]) and
        (crypto_df['high'].iloc[-1] > crypto_df['high'].iloc[-2]) and
        (crypto_df['low'].iloc[-1] == crypto_df['open'].iloc[-1]) and
        (crypto_df['low'].iloc[-1] > crypto_df['low'].iloc[-2]) #This conditional part I might change to be low=open
        ):
        return True
    else:
        return False
def morning_star(crypto_df):
    # if ((crypto_df['close'].iloc[-2] > crypto_df['open'].iloc[-2]) and
    #     (crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-1]) and
    #     (crypto_df['low'].iloc[-2] < crypto_df['low'].iloc[-1]) and
    #     (crypto_df['high'].iloc[-2] > crypto_df['low'].iloc[-1]) and
    #     (crypto_df['close'].iloc[-2] > crypto_df['low'].iloc[-1]) and
    #     (crypto_df['close'].iloc[-1] > crypto_df['high'].iloc[-2])
    #     ):
    if ((crypto_df['close'].iloc[-4] < crypto_df['open'].iloc[-4]) and
        (crypto_df['close'].iloc[-3] < crypto_df['open'].iloc[-3]) and
        (crypto_df['close'].iloc[-2] < crypto_df['open'].iloc[-2]) and
        (crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-1]) and
        (crypto_df['low'].iloc[-3] < crypto_df['open'].iloc[-2]) and
        (crypto_df['low'].iloc[-1] > crypto_df['open'].iloc[-1])
            ):
        return True
    else:
        return False
def piercing_line(crypto_df):
    mid_line = (crypto_df['close'].iloc[-2] + crypto_df['open'].iloc[-2]) / 2
    if ((crypto_df['close'].iloc[-2] < crypto_df['open'].iloc[-2]) and
        (crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-1]) and
        mid_line > crypto_df['open'].iloc[-1] and
        mid_line < crypto_df['close'].iloc[-1] and 
        (crypto_df['low'].iloc[-2] > crypto_df['low'].iloc[-1])
        ):
        return True
    else:
        return False
def three_white_soldiers(crypto_df):
    try:
        out, _, _ = stoch_RSI(crypto_df)
        stoch_rsi = out['Stoch_RSI'].iloc[-1]
    except:
        stoch_rsi = 100
    if ((crypto_df['close'].iloc[-3] > crypto_df['open'].iloc[-3]) and
        (crypto_df['close'].iloc[-2] > crypto_df['open'].iloc[-2]) and
        (crypto_df['close'].iloc[-1] > crypto_df['open'].iloc[-1]) and
        (crypto_df['open'].iloc[-2] > crypto_df['open'].iloc[-3]) and 
        (crypto_df['open'].iloc[-1] > crypto_df['open'].iloc[-2]) and
        (crypto_df['close'].iloc[-2] > crypto_df['close'].iloc[-3]) and
        (crypto_df['close'].iloc[-1] > crypto_df['close'].iloc[-2]) and
        (stoch_rsi < 70)
            ):
        return True
    else:
        return False
def main():
    start = default_timer()
    if path.exists(path.join(getcwd(),'candlestick_output.txt')):
        remove(path.join(getcwd(),'candlestick_output.txt'))
    names_crypt = set_crypt_names()
    for crypt in names_crypt:
        print(crypt)
        # data = set_data(crypt)
        ohlc = get_ohlc(crypt)
        create_candlestick(crypt,ohlc)
        analysis_candlestick(ohlc, crypt)
    print(f'{default_timer() - start} time to complete')
if __name__ == "__main__":
    main()