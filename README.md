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
5     BTC  262.622806           False            False
29   WBTC   35.046764           False            False
12    ETH   28.888579           False            False
16    GNO    2.311337           False            False
2    AVAX    0.784491           False            False
19    LPT    0.251691           False            False
21    LTC    0.221613           False            False
13    FTM    0.052247           False            False
6     CRV    0.051400           False            False
8     DOT    0.025124           False            False

```

