import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
btc_price = pd.read_csv('ETH_future_lstm.csv')
temp = yf.Ticker("ETH-USD")
data = temp.history(period = 'max', interval="1d")
plt.plot(btc_price.Date.iloc[0:len(data.Close)],data.Close,color='k',label='current_data')
plt.plot(btc_price.Date,btc_price.Actual,color='b',label='old_data') 
plt.plot(btc_price.Date,btc_price.Forecast,color='r',label='predicted_data')
plt.legend()
plt.show()
