# Cryptocurrency Algorithmic Trading and Time Series Forecasting

Technical analysis and machine learning for cryptocurrency

## Installation
```bash
conda env create -f crypto.yaml
```

## Usage

```python
# Time Series Forecasting - cumulative log returns
python ml_with_yfinance.py
# Technical Analysis
python technical_analysis.py BTCUSD or python technical_analysis.py all
# Candlestick Patterns
python candlestick.py
```
### Full Market Trend
![alt text](https://github.com/bszek213/cryptoML/blob/dev/full_market_trend.png)
### Sample Output from Time Series Forecasting Matrix
![alt text](https://github.com/bszek213/cryptoML/blob/dev/forecast_ML/BTC/BTC.png)

### Sample Output from the Technical Analysis
![alt text](https://github.com/bszek213/cryptoML/blob/dev/technical_analysis/BTCUSD_174.png)

## Top 10 performing Cryptos
```bash
   crypto  yhat_sum  MACD_cross_buy  MACD_cross_sell
17  FORTH  0.144993           False            False
28   RARE  0.140888           False            False
37    WOO  0.125425           False            False
32    SOL  0.121373           False            False
5    ATOM  0.095684           False            False
24   MSOL  0.088325           False            False
34   TOKE  0.083227           False            False
29    REQ  0.074029           False            False
38    XMR  0.067982           False            False
35  TRIBE  0.067520           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
   crypto  yhat_sum  MACD_cross_buy  MACD_cross_sell
17  FORTH  0.144993           False            False
28   RARE  0.140888           False            False
37    WOO  0.125425           False            False
32    SOL  0.121373           False            False
5    ATOM  0.095684           False            False
24   MSOL  0.088325           False            False
34   TOKE  0.083227           False            False
29    REQ  0.074029           False            False
38    XMR  0.067982           False            False
35  TRIBE  0.067520           False            FalseEmpty DataFrame
Columns: [crypto, yhat_sum, MACD_cross_buy, MACD_cross_sell]
Index: []   crypto  yhat_sum  MACD_cross_buy  MACD_cross_sell
17  FORTH  0.144993           False            False
28   RARE  0.140888           False            False
37    WOO  0.125425           False            False
32    SOL  0.121373           False            False
5    ATOM  0.095684           False            False
24   MSOL  0.088325           False            False
34   TOKE  0.083227           False            False
29    REQ  0.074029           False            False
38    XMR  0.067982           False            False
35  TRIBE  0.067520           False            False