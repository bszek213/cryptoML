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
30    WOO  0.257789           False            False
2     AKT  0.159403           False            False
32    XMR  0.121267           False            False
3    ALGO  0.116804           False            False
10    CRV  0.106895           False            False
5    ATOM  0.099164           False            False
19  MATIC  0.095757           False            False
15    GNO  0.092551           False            False
24    REQ  0.083756           False            False
26    SNX  0.077708           False            False
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
41    WOO  0.270392           False            False
2    ALGO  0.203717           False            False
37    SOL  0.187695           False            False
33   RARE  0.153312           False            False
18  FORTH  0.105568           False            False
19    ICP  0.098867           False            False
5    ATOM  0.097012           False            False
0     ACH  0.095352           False            False
42    XMR  0.088953           False            False
34    REQ  0.081795           False            False