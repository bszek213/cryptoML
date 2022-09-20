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
  crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
0    BTC  132.869644           False            False
1    ETH   17.858826           False            False
2    QNT    3.716742           False            False
3    MKR    1.716291           False            False
4  LUNA1    1.006432           False            False
5    GNO    0.827734           False            False
6   EGLD    0.643910           False            False
7   ATOM    0.611704           False            False
8   AVAX    0.284228           False            False
9    LTC    0.166953           False            False