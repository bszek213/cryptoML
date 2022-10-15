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
python check_positive_trend.py -s 1440 -c BTCUSD
# Candlestick Patterns
python candlestick.py
```
### Full Market Trend
![alt text](https://github.com/bszek213/cryptoML/blob/dev/full_market_trend.png)
### Sample Output from Time Series Forecasting Matrix
![alt text](https://github.com/bszek213/cryptoML/blob/dev/forecast_ML/BTC/BTC.png)

### Sample Output from the Technical Analysis
![alt text](https://github.com/bszek213/cryptoML/blob/dev/technical_analysis/BTCUSD.svg)

## Top 10 performing Cryptos
```bash
   crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
9    COMP  0.114023           False            False
13   DYDX  0.044125           False            False
38    RLC  0.021846           False            False
28   MANA  0.020544           False            False
47    XTZ  0.019627           False            False
16    FIS  0.019457           False            False
37    REP  0.019036           False            False
18   GALA  0.017427           False            False
42   SCRT  0.012712           False            False
17    FTM  0.011951           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.l

