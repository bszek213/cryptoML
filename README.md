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
6     BTC  292.527841           False            False
29   WBTC   37.746647           False            False
13    ETH   35.793396           False            False
17    GNO    3.088090           False            False
4    AVAX    0.417297           False            False
19    LPT    0.355017           False            False
21    LTC    0.286711           False            False
9     DOT    0.062374           False            False
14    FTM    0.054599           False            False
11    ENS    0.036449           False            False
```
## Candlestick Results
```bash
ANKR bullish bullish engulf pattern
GST bullish - inverted hammer  pattern
NYM bullish - piercing line pattern
OCEAN bullish bullish engulf pattern
UMA bullish bullish engulf pattern
XRP bullish - three white soldiers pattern
```
