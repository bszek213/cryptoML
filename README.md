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
9     BTC  333.636667           False            False
45   WBTC   52.840949           False            False
19    ETH   37.748911           False            False
25    GNO    3.931737           False            False
5    AVAX    0.736194           False            False
31    LPT    0.493533           False            False
33    LTC    0.355463           False            False
15    DOT    0.077802           False            False
46    XMR    0.066955           False            False
21    FTM    0.054434           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ACH bullish bullish engulf pattern
ACH bullish - piercing line pattern
CVX bullish - piercing line pattern
DAI bullish - piercing line pattern
GHST bullish bullish engulf pattern
KINT bullish bullish engulf pattern
LINK bullish bullish engulf pattern
LTC bullish bullish engulf pattern
```

