"""Data and utilities for testing."""
import pandas as pd
import numpy as np
from datetime import datetime

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



def getListVN30():
    hose30 = ["CII", "CTD", "CTG", "DHG", "DPM", "EIB", "FPT", "GAS", "GMD", "HDB",
              "HPG", "MBB", "MSN", "MWG", "NVL", "PNJ", "REE", "ROS", "SAB", "SBT",
              "SSI", "STB", "TCB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"]
    return hose30


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