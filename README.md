# Cryptocurrency Algorithmic Trading and Time Series Forecasting

Technical analysis and machine learning for cryptocurrency

## Installation
```bash
conda env create -f crypto.yaml
```

## Usage

```python
# Time Series Forecasting - cumulative log returns
python ml_with_yfinance.py
# Technical Analysis
python technical_analysis.py BTCUSD or python technical_analysis.py
# Candlestick Patterns
python candlestick.py
```
### Full Market Trend
![alt text](https://github.com/bszek213/cryptoML/blob/dev/full_market_trend.png)
### Sample Output from Time Series Forecasting Matrix
![alt text](https://github.com/bszek213/cryptoML/blob/dev/forecast_ML/BTC/BTC.png)

### Sample Output from the Technical Analysis
![alt text](https://github.com/bszek213/cryptoML/blob/dev/technical_analysis/BTCUSD.png)

## Top 10 performing Cryptos
```bash
   crypto  reg_coef  MACD_cross_buy  MACD_cross_sell
29   ROOK  0.000776           False            False
32    SOL  0.000450           False            False
39    XRP  0.000268           False            False
36   UNFI  0.000255           False            False
3    API3  0.000245           False            False
11   ETHW  0.000240           False            False
27   QTUM  0.000228           False            False
22    MKR  0.000184           False            False
15    GNO  0.000157           False            False
12   FARM  0.000141           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

