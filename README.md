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
6     BTC  251.756272            True            False
16    ETH   27.653922           False            False
21    GNO    2.145629           False            False
31  LUNA1    1.093027           False            False
3    AVAX    0.539347           False            False
28    LPT    0.235083           False            False
29    LTC    0.215558           False            False
18    FTM    0.051624           False            False
9     CRV    0.050486           False            False
14    ENS    0.030906           False            False

```
   crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
5     BTC  251.756272           False            False
13    ETH   27.653922           False            False
17    GNO    2.145629           False            False
23  LUNA1    1.093027           False            False
3    AVAX    0.539347           False            False
20    LPT    0.235083           False            False
21    LTC    0.215558           False            False
14    FTM    0.051624           False            False
7     CRV    0.050486           False            False
11    ENS    0.030906           False            False