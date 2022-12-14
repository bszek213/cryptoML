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
37    SOL  0.281478           False            False
42    WOO  0.264608           False            False
30   RARE  0.172207           False            False
36    SNX  0.129528           False            False
8    BICO  0.129436           False            False
33    REQ  0.098533           False            False
25   MSOL  0.098461           False            False
0     ACH  0.096372           False            False
44    XMR  0.083277           False            False
16    ENS  0.073642           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
