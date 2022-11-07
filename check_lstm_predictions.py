import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import sys
csv_name = f'{sys.argv[1]}_future_lstm.csv'
btc_price = pd.read_csv(csv_name)
crypt = f'{sys.argv[1]}-USD'
temp = yf.Ticker(crypt)
data = temp.history(period = 'max', interval="1d")
# plt.plot(btc_price.Date.iloc[0:len(data.Close)],data.Close,color='k',label='current_data')
# plt.plot(btc_price.Date,btc_price.Actual,color='b',label='old_data') 
plt.plot(btc_price.Date.iloc[0:len(data.Close)],data.Close.values,color='k',label='current price')
plt.plot(btc_price.Date,btc_price.Forecast.values,color='r',label='predicted_data')
plt.legend()
plt.title(sys.argv[1])
plt.show()
