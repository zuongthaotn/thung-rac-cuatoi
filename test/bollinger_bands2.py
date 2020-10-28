import requests
import pandas as pd
import matplotlib.pyplot as plt


def bollingerbands(stock):
    stockprices = pd.read_csv('/home/zuongthao/GIT/zuongthaotn/quant-trading-by-py/cophieu68/AAA.csv')
    stockprices = stockprices.set_index('Date')
    stockprices['MA20'] = stockprices['Close'].rolling(window=20).mean()
    stockprices['20dSTD'] = stockprices['Close'].rolling(window=20).std()

    stockprices['Upper'] = stockprices['MA20'] + (stockprices['20dSTD'] * 2)
    stockprices['Lower'] = stockprices['MA20'] - (stockprices['20dSTD'] * 2)

    stockprices[['Close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
    plt.grid(True)
    plt.title(stock + ' Bollinger Bands')
    plt.axis('tight')
    plt.ylabel('Price')
    plt.savefig('apple.png', bbox_inches='tight')


bollingerbands('aapl')