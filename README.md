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
### Full Market Trend
![alt text](https://github.com/bszek213/cryptoML/blob/dev/full_market_trend.png)
### Sample Output from Time Series Forecasting Matrix
![alt text](https://github.com/bszek213/cryptoML/blob/dev/forecast_ML/BTC/BTC.png)

### Sample Output from the Technical Analysis
![alt text](https://github.com/bszek213/cryptoML/blob/dev/technical_analysis/BTCUSD.svg)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Top 10 performing Cryptos
```bash
   crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
30   WBTC  52.196006           False            False
14    ETH  41.577373           False            False
4    AVAX   0.338812           False            False
11    DOT   0.095071           False            False
31    XMR   0.090924           False            False
10    CRV   0.058907           False            False
26   SAND   0.049405           False            False
12    ENS   0.037481           False            False
0    ALGO   0.020772           False            False
13    ETC   0.017785           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
AUDIO bullish - piercing line pattern
DENT bullish - piercing line pattern
DYDX bullish bullish engulf pattern
INJ bullish - piercing line pattern
```

