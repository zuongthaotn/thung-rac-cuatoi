"""Data and utilities for testing."""
import pandas as pd
import numpy as np
from datetime import datetime

def getATR(lookback, high_price, low_price):
    """
    Average True Range
    ATR(100) - It returns the average height of a candle within the last 100 bars.
        1. ATR(100) = ((high1-low1) +(high2-low2) + ... + (high100-low100))/100
        2. ATR(100) = high.rolling(100).mean() - low.rolling(100).mean()
    :param int lookback:
    :param pandas high_price:
    :param pandas low_price:
    :return float:
    """
    atr = high_price.rolling(lookback).mean() - low_price.rolling(lookback).mean()
    return atr.iloc[-1]

def getVolatility(array, n):
    """
    Computing Volatility
    https://blog.quantinsti.com/volatility-and-measures-of-risk-adjusted-return-based-on-volatility/
    :param array:
    :param n:
    :return:
    """
    logRet = np.log(array / array.shift(1))

    # Compute Volatility using the pandas rolling standard deviation function
    return logRet.rolling(window=n).std() * np.sqrt(n)

def getVolatilityV2(lookback, high_price, low_price, close_price):
    """
        Computing Volatility
        :param int lookback:
        :param pandas high_price:
        :param pandas low_price:
        :return float:
        @author: Magnus
    """
    avgClose = (high_price.rolling(lookback).mean() - low_price.rolling(lookback).mean()) / close_price.rolling(lookback).mean()
    return avgClose.iloc[-1]

def getSharpe(returns, rf, days=252):
    """
    Computing Sharpe Ratio
    https://blog.quantinsti.com/volatility-and-measures-of-risk-adjusted-return-based-on-volatility/
    :param returns:
    :param rf:
    :param days:
    :return:
    """
    volatility = returns.std() * np.sqrt(days)
    sharpe_ratio = (returns.mean() - rf) / volatility
    return sharpe_ratio

def getInformationRatio(returns, benchmark_returns, days=252):
    """
    Information ratio (IR)
    https://blog.quantinsti.com/volatility-and-measures-of-risk-adjusted-return-based-on-volatility/
    :param returns:
    :param benchmark_returns:
    :param days:
    :return:
    """
    return_difference = returns - benchmark_returns
    volatility = return_difference.std() * np.sqrt(days)
    information_ratio = return_difference.mean() / volatility
    return information_ratio

def getModiglianiRatio(returns, benchmark_returns, rf, days=252):
    """
    Modigliani Ratio
    https://blog.quantinsti.com/volatility-and-measures-of-risk-adjusted-return-based-on-volatility/
    :param returns:
    :param benchmark_returns:
    :param rf:
    :param days:
    :return:
    """
    volatility = returns.std() * np.sqrt(days)
    sharpe_ratio = (returns.mean() - rf) / volatility
    benchmark_volatility = benchmark_returns.std() * np.sqrt(days)
    m2_ratio = (sharpe_ratio * benchmark_volatility) + rf
    return m2_ratio

def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()


def RSI(array, n):
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)

def MMI(data, period=100):
    '''
    MMM - Market Meanness Index
    :param data:
    :param period: nsarray
    :return:
    '''
    mmi = np.zeros(data.shape)
    for i in range(len(data)):
        if i < period - 1:
            continue

        m = np.median(data[(i - period + 1):i])
        nl = 0
        nh = 0
        for j in range(period - 1):
            if j < 1:
                continue
            if (data[i - j] > m) and (data[i - j] > data[i - j - 1]):
                nl += 1
            if (data[i - j] < m) and (data[i - j] < data[i - j - 1]):
                nh += 1
        mmi[i] = 100.0 * (nl + nh) / (period - 1)

    return mmi


# %% Get VN stocks data
def get_pricing_by_path(filepath, start_date='2000-07-28', end_date=None):
    import os

    usecols = None
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')

    if os.path.isfile(filepath):
        prices = pd.read_csv(
            filepath,
            index_col='Date',
            parse_dates=['Date'],
            date_parser=date_parser,
            usecols=usecols
        )[start_date:end_date]
        prices['Date'] = prices.index
        return prices

    return None


def getListVN30Jan2020():
    hose30 = ["CII", "CTD", "CTG", "DHG", "DPM", "EIB", "FPT", "GAS", "GMD", "HDB",
              "HPG", "MBB", "MSN", "MWG", "NVL", "PNJ", "REE", "ROS", "SAB", "SBT",
              "SSI", "STB", "TCB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]
    return hose30

def getListVN30Jan2021():
    hose30 = ["BID", "BVH", "CTG", "FPT", "GAS", "HDB", "HPG", "KDH", "MBB", "MSN",
              "MWG", "NVL", "PDR", "PLX", "PNJ", "POW", "REE", "SBT", "SSI", "STB",
              "TCB", "TCH", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]
    return hose30

def getListVN30():
    return getListVN30Jan2021()


def getListVN30ProfitableOfStockBreakout():
    hose30 = ["CTG", "GMD", "PNJ", "REE", "SBT", "VCB", "VIC", "VJC", "VPB"]
    return hose30


def getListBlueChips2020():
    blue_chips = ["VNM", "VCB", "VIC", "FPT", "MWG", "VJC", "HPG", "DHG", "SAB", "MBB", "BID", "POW"]
    return blue_chips


def getAllTickers(vnx_file):
    vnx = pd.read_csv(vnx_file, usecols=["ticker"])
    vnx_ticker = np.array(vnx)
    return vnx_ticker.reshape(-1)

def getHOSETickers(vnx_file):
    vnx = pd.read_csv(vnx_file, usecols=["ticker", "exchange"])
    vnx_ticker = np.array(vnx)
    hose_ticker = []
    for ticker in vnx_ticker:
        ticker_id = ticker[0]
        ticker_exchange = ticker[1]
        if ticker_exchange == 'HOSE':
            hose_ticker.append(ticker_id)
    return hose_ticker

# %% Get VN stocks data
## No longer use
def get_pricing(filename, start_date='2000-07-28', end_date=None):
    import os
    from os.path import dirname, join
    filepath = join(dirname(dirname(dirname(__file__))), 'method/cophieu68/' + filename)

    usecols = None
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')

    if os.path.isfile(filepath):
        prices = pd.read_csv(
            filepath,
            index_col='Date',
            parse_dates=['Date'],
            date_parser=date_parser,
            usecols=usecols
        )[start_date:end_date]
        prices['Date'] = prices.index
        return prices

    return None