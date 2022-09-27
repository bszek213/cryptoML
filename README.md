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
	crypto	reg_coef	MACD_cross_buy	MACD_cross_sell
9	BTC	145.670739123533	False	False
18	ETH	18.4833007706609	False	False
40	QNT	3.70448307323699	False	False
35	MKR	1.95913515510643	False	False
23	GNO	1.01640869490838	False	False
33	LUNA1	1.01434457569243	False	False
15	EGLD	0.62339183047129	False	False
3	ATOM	0.599542982099698	False	False
4	AVAX	0.244793908994724	False	False
31	LTC	0.166726877216872	False	False
30	LPT	0.155144987728211	False	False

```
   crypto    reg_coef  MACD_cross_buy  MACD_cross_sell
7     BTC  220.817672           False            False
17    ETH   22.942737           False            False
22    GNO    1.707989           False            False
31  LUNA1    1.056653           False            False
4    AVAX    0.649316           False            False
28    LPT    0.187799           False            False
29    LTC    0.187244           False            False
19    FTM    0.047525           False            False
10    CRV    0.044252           False            False
15    ENS    0.032315           False            False