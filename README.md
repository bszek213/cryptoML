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
8     GALA  0.000776           False            False
31    UNFI  0.000453           False            False
34     XRP  0.000253           False            False
29     SOL  0.000250           False            False
7      FIS  0.000212           False            False
24    QTUM  0.000187           False            False
18     MKR  0.000167           False            False
23  PSTAKE  0.000159           False            False
32     WOO  0.000149           False            False
5     ETHW  0.000140           False            False
```
## Candlestick Results
run candlestick analysis before 5pm PDT, as the sample rates are on UTC time. The
new "day" will start then.
```bash
ETC bullish - inverted hammer  pattern
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
   crypto  reg_coef  MACD_cross_buy  MACD_cross_sell
31    SOL  0.000447           False            False
34   UNFI  0.000348           False            False
37    XRP  0.000273           False            False
28   ROOK  0.000247           False            False
1    API3  0.000245           False            False
10   ETHW  0.000240           False            False
26   QTUM  0.000228           False            False
21    MKR  0.000188           False            False
14    GNO  0.000144           False            False
36    XMR  0.000142           False            False