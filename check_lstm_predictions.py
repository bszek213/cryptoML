import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import sys
import os
csv_name = f'{sys.argv[1]}_future_lstm.csv'
final_dir = os.path.join(os.getcwd(), 'lstm_data', csv_name)
btc_price = pd.read_csv(final_dir)
crypt = f'{sys.argv[1]}-USD'
temp = yf.Ticker(crypt)
data = temp.history(period = 'max', interval="1d")
# plt.plot(btc_price.Date.iloc[0:len(data.Close)],data.Close,color='k',label='current_data')
# plt.plot(btc_price.Date,btc_price.Actual,color='b',label='old_data') 
plt.plot(btc_price.Date.iloc[0:len(data.Close)],data.Close.values,color='k',label='current price')
save_predicted_price = []
fore_pct_change = btc_price.Forecast.dropna().values
temp_df = btc_price[['Date','Forecast']].dropna()
temp_actual = btc_price[['Date','Actual']].dropna()
for i in range(len(fore_pct_change)):
    if i == 0:
        temp = data.Close.loc[temp_actual.Date.iloc[-1]]
        save_predicted_price.append(temp + (temp * fore_pct_change[i]))
    else:
        save_predicted_price.append(save_predicted_price[i-1] + (save_predicted_price[i-1] * fore_pct_change[i]))
plt.plot(temp_df.Date,save_predicted_price,color='r',label='predicted_data')
plt.legend()
plt.title(sys.argv[1])
plt.show()
