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
9     BTC  342.933466           False            False
43   WBTC   50.523715           False            False
19    ETH   37.009757           False            False
25    GNO    3.713055           False            False
30    LPT    0.486213           False            False
5    AVAX    0.365264           False            False
32    LTC    0.350030           False            False
44    XMR    0.122482           False            False
15    DOT    0.079124           False            False
12    CRV    0.057860           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
CQT bullish - inverted hammer  pattern
CVC bullish - inverted hammer  pattern
FARM bullish - inverted hammer  pattern
FET bullish - inverted hammer  pattern
FLOW bullish - inverted hammer  pattern
JUNO bullish - piercing line pattern
KEEP bullish - inverted hammer  pattern
KSM bullish - inverted hammer  pattern
PERP bullish - inverted hammer  pattern
SRM bullish - inverted hammer  pattern
TBTC bullish - piercing line pattern
TOKE bullish bullish engulf pattern
UNFI bullish - inverted hammer  pattern
```
