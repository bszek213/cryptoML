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
37    WOO  0.330807           False            False
20    ICP  0.159149           False            False
33    SOL  0.129524           False            False
28   RARE  0.127118           False            False
3    ALGO  0.124974           False            False
6    ATOM  0.114917           False            False
30    REQ  0.108873           False            False
35      T  0.094538           False            False
0     ACH  0.092719           False            False
32    SNX  0.091575           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
