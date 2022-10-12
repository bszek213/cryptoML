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
6    COMP  0.100889           False            False
13    FTM  0.046808           False            False
19    LPT  0.040716           False            False
22  MATIC  0.025588           False            False
12    FIS  0.019431           False            False
5     BTC  0.018828           False            False
9     ENJ  0.013895           False            False
27  SUSHI  0.013310           False            False
20    LRC  0.012063           False            False
3    AVAX  0.011485           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
RUNE bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
