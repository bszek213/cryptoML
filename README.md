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
7     BTC  240.264303           False            False
17    ETH   26.526868           False            False
22    GNO    1.964114           False            False
31  LUNA1    1.081725           False            False
4    AVAX    0.591182           False            False
28    LPT    0.216415           False            False
29    LTC    0.203888           False            False
19    FTM    0.050840           False            False
10    CRV    0.046167           False            False
15    ENS    0.031658           False            False

```

