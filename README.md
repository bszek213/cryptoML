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
4     BTC  271.841126           False            False
11    ETH   29.814209           False            False
27   WBTC   19.313308           False            False
15    GNO    2.469442           False            False
2    AVAX    0.506106           False            False
18    LPT    0.267511           False            False
20    LTC    0.238648           False            False
12    FTM    0.053155           False            False
5     CRV    0.048230           False            False
9     ENS    0.038461           False            False

```
