# Cryptocurrency Algorithmic Trading and Time Series Forecasting

Technical analysis and machine learning for cryptocurrency

## Installation
```bash
conda env create -f crypto.yaml
```

## Usage

```python
# Time Series Forecasting
python ml_with_yfinance.py
# Technical Analysis
python check_positive_trend.py -s 1440 -c BTCUSD
# Candlestick Patterns
python candlestick.py
```
### Sample Output from Time Series Forecasting Matrix
![alt text](https://github.com/bszek213/cryptoML/blob/main/forecast_ML/BTC/BTC.png)

### Sample Output from the Technical Analysis
![alt text](https://github.com/bszek213/cryptoML/blob/main/technical_analysis/BTCUSD.svg)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Top 10 performing Cryptos
```bash
   crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
9     BTC  322.827111           False            False
45   WBTC   42.804918           False            False
19    ETH   35.400248           False            False
25    GNO    3.404684           False            False
5    AVAX    0.718336           False            False
32    LPT    0.412729           False            False
34    LTC    0.314041           False            False
46    XMR    0.072940           False            False
15    DOT    0.063428           False            False
12    CRV    0.058793           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
APE3 bullish - piercing line pattern
DYDX bullish - piercing line pattern
EGLD bullish bullish engulf pattern
KAR bullish - piercing line pattern
NYM bullish - piercing line pattern
OCEAN bullish - piercing line pattern
POWR bullish bullish engulf pattern
RAY bullish bullish engulf pattern
STORJ bullish - piercing line pattern
XRP bullish bullish engulf pattern
```
