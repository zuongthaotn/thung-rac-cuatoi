"""Data and utilities for testing."""
import pandas as pd
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