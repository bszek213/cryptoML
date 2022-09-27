#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Candlestick analysis yFinance
@author: bszekely
"""
import yfinance as yf
from os import getcwd, path, mkdir
from pandas import read_csv
from timeit import default_timer
import plotly.graph_objects as go
#TODO: ADD kraken input to the last day, as yfinance day interval will only get the previous days price, not the current day.
def set_data(crypt):
    # crypt_name = sys.argv[1] + '-USD'
    crypt_name = crypt + '-USD'
    temp = yf.Ticker(crypt_name)
    history = temp.history(period = 'max', interval="1d")
    # data = yf.download(tickers=crypt_name, period = 'max', interval = '1d') #columns = Index(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    return history
def set_crypt_names():
    location = getcwd()
    df = read_csv(path.join(location,'crypto_trade_min.csv'))
    df.sort_values(by=['crypto'],inplace=True)
    return df['crypto']
def create_candlestick(data,crypt):
    direct = getcwd()
    check_folder = path.join(direct,'candlestick_figures')
    name = crypt + '_candlestick.png'
    if path.exists(check_folder):
        final_dir = path.join(check_folder, name)
    else:
        mkdir(check_folder)
        final_dir = path.join(check_folder, name)
    fig = go.FigureWidget(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close']))
    try:
        if len(data.index) > 30:
            start = data.index[-30]
            end = data.index[-1]
            fig.update_xaxes(range=[start, end])
            start = min(data['Low'].iloc[-30:-1])
            end = max(data['High'].iloc[-30:-1])
        else:
            start = data.index[-15]
            end = data.index[-1]
            fig.update_xaxes(range=[start, end])
            start = min(data['Low'].iloc[-15:-1])
            end = max(data['High'].iloc[-15:-1])
        fig.update_yaxes(range=[start, end])
        fig.update_layout(title=crypt,xaxis_rangeslider_visible=False)
        fig.write_image(final_dir)
    except:
        print(f'{crypt} candlestick cannot be created')
    
def analysis_candlestick(data):
    pass
def main():
    start = default_timer()
    names_crypt = set_crypt_names()
    for crypt in names_crypt:
        print(crypt)
        data = set_data(crypt)
        create_candlestick(data,crypt)
if __name__ == "__main__":
    main()
