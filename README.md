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
4     BTC  297.877662           False            False
11    ETH   32.861956           False            False
28   WBTC   30.506243           False            False
15    GNO    2.949444           False            False
2    AVAX    0.464088           False            False
18    LPT    0.331747           False            False
20    LTC    0.267853           False            False
29    XMR    0.071820           False            False
12    FTM    0.054332           False            False
7     DOT    0.040178           False            False
```
## Candlestick Results
```bash
LUNA2 bullish - piercing line pattern
OXT bullish - piercing line pattern
RARE bullish - inverted hammer pattern
RARE bullish - piercing line pattern
SBR bullish - piercing line pattern
```
