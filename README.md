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
5     BTC  229.287834           False            False
14    ETH   27.169836           False            False
19    GNO    1.900921           False            False
28  LUNA1    1.077960           False            False
3    AVAX    0.563080           False            False
25    LPT    0.209725           False            False
26    LTC    0.199216           False            False
16    FTM    0.049966           False            False
8     CRV    0.042195           False            False
12    ENS    0.027165           False            False

```
