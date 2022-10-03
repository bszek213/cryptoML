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
4     BTC  291.087474           False            False
11    ETH   32.391578           False            False
27   WBTC   26.477027           False            False
15    GNO    2.723575           False            False
2    AVAX    0.436584           False            False
17    LPT    0.303859           False            False
19    LTC    0.255842           False            False
5     CRV    0.053200           False            False
12    FTM    0.052249           False            False
28    XMR    0.034384           False            False

```
