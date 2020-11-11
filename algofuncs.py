"""Data and utilities for testing."""
import pandas as pd
import numpy as np
from datetime import datetime


def isPeak3Days(Data):
    return (Data[-3] < Data[-2]) and (Data[-2] > Data[-1])


def isValley3Days(Data):
    return (Data[-3] > Data[-2]) and (Data[-2] < Data[-1])

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