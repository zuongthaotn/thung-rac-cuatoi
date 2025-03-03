import time

import neat
import os
import pickle
from datetime import datetime
from datetime import date

import vn_realtime_stock_data.stockHistory as stockHistory
import method.EMA.v1 as ema_v1
import AI.EMA.sources.constants as constants
from AI.EMA.sources.broker import Broker
import matplotlib.pyplot as plt

def run():
    # getting data for this generation
    timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    htd = stockHistory.getStockHistoryData("MBB", 1, timestamp_to)
    prepared_data = ema_v1.prepareData(htd)
    plt.title("EMA_R Histogram")
    plt.hist(prepared_data['EMA_R'].to_numpy(), bins=100)
    plt.show()
run()