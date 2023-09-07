import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime

CUTLOSS_PERCENT = 0.97

def prepareData(htd):
    if 'Time' in htd.columns:
        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
    macd = ta.macd(htd['Close'], 20, 5, 9)
    htd['Date'] = pd.to_datetime(htd['DateStr'])
    htd = htd.assign(MACD=macd['MACD_5_20_9'])
    htd = htd.assign(MACDh=macd['MACDh_5_20_9'])
    htd = htd.assign(MACDs=macd['MACDs_5_20_9'])
    ticker_data = htd.set_index('Date').drop(columns=['Time', 'DateStr'])
    ticker_data['MACD'] = ticker_data['MACD'].replace(np.nan, 0)
    ticker_data['MACDh'] = ticker_data['MACDh'].replace(np.nan, 0)
    ticker_data['MACDs'] = ticker_data['MACDs'].replace(np.nan, 0)
    return ticker_data

def hasBuySignal(macd, signal):
    """

    """
    today_macd = macd[-1]
    today_signal = signal[-1]
    yesterday_macd = macd[-2]
    yesterday_signal = signal[-2]
    if yesterday_macd < yesterday_signal and today_macd > today_signal:
        return True
    return False

def hasSellSignal(macd, signal):
    """

    """
    today_macd = macd[-1]
    today_signal = signal[-1]
    yesterday_macd = macd[-2]
    yesterday_signal = signal[-2]
    if yesterday_macd > yesterday_signal and today_macd < today_signal:
        return True
    return False

def has_force_sell_signal(current_price, buy_price):
    if current_price < buy_price * CUTLOSS_PERCENT:
        return True
    return False