import pandas as pd
import numpy as np


def prepareData(htd):
    if 'Time' in htd.columns:
        from datetime import datetime

        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
    htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
    htd['SMA_20'] = htd['Close'].rolling(window=20).mean()
    htd['SMA_H'] = htd.apply(
        lambda x: (x['SMA_20'] - x['SMA_5']), axis=1)
    htd['Date'] = pd.to_datetime(htd['DateStr'])
    ticker_data = htd.set_index('Date')
    ticker_data.drop(['Time'], axis=1)
    ticker_data.drop(['DateStr'], axis=1)
    ticker_data['Date'] = pd.to_datetime(ticker_data.index)
    ticker_data['SMA_5'] = ticker_data['SMA_5'].replace(np.nan, 0)
    ticker_data['SMA_20'] = ticker_data['SMA_20'].replace(np.nan, 0)
    ticker_data['SMA_H'] = ticker_data['SMA_H'].replace(np.nan, 0)
    return ticker_data

def prepareDataVersionOffline(htd):
    htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
    htd['SMA_20'] = htd['Close'].rolling(window=20).mean()
    htd['SMA_H'] = htd.apply(
        lambda x: (x['SMA_20'] - x['SMA_5']), axis=1)
    return htd

def RSI(array, n):
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)


def hasBuySignal(sma_h, open=None, close=None, sma5=None, sma20=None):
    """
    2 days ago sma20 was above sma5
    yesterday sma20 was above sma5
    today sma20 is above sma5
    sma_height_2_days_ago > 2.5 * sma_height_today
    """
    p1_sma_h = sma_h[-1]
    p2_sma_h = sma_h[-2]
    p3_sma_h = sma_h[-3]
    if p1_sma_h > 0 and p2_sma_h > p1_sma_h and p1_sma_h < 0.02 * close[-1]:
        return True
    if close[-1] > sma5[-1] and open[-1] > sma5[-1]:
        return False
    if p1_sma_h > 0 and p2_sma_h > p1_sma_h and p3_sma_h > p2_sma_h and (p3_sma_h / p1_sma_h) > 2.5:
        return True
    return False


def hasSellSignal(open, close, sma_h, sma5, sma20=None, cutoff_percent=.99):
    p1_sma_h = sma_h[-1]
    close_price = close[-1]
    open_price = open[-1]
    """
        Yesterday, sma20 is below sma5 but
        Today, sma20 is above sma5
    """
    if sma20[-2] < sma5[-2] and sma20[-1] > sma5[-1]:
        return True
    """
        Yesterday, sma20 is below sma5 but
        Today, sma20 is above close
    """
    if (sma20[-1] < sma5[-1] and sma20[-1] > close[-1]):
        return True
    """
        if sma_h is very small (<1% close price)
    """
    if p1_sma_h > close_price * 0.001:
        return False

    """
        Today sma20 is above sma5
        or current_price < sma5 and open_price > current_price
        or current_price < 99% today_sma5
    """
    # if p1_sma_h > 0 or (close_price < sma5[-1] and open_price > close_price) or close_price < cutoff_percent * sma5[-1]:
    # if p1_sma_h > 0 or (close_price <= sma20[-1] or close_price < cutoff_percent * sma5[-1]):
    if ((close_price < cutoff_percent * sma5[-1]) and sma20[-1] < sma5[-1]):
        return True
    return False