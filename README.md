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
python technical_analysis.py BTCUSD or python technical_analysis.py
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
9    COMP  0.114029           False            False
23   MANA  0.031019           False            False
36   SAND  0.028251           False            False
32    RLC  0.019631           False            False
14    FIS  0.018038           False            False
29  POLIS  0.017638           False            False
31    REP  0.016150           False            False
42    XTZ  0.013699           False            False
10    CRV  0.012676           False            False
3    ANKR  0.011565           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
