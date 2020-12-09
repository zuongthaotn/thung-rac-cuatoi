import numpy as np
import pandas as pd

def isPeak3Days(Data):
    return (Data[-3] < Data[-2]) and (Data[-2] > Data[-1])


def isValley3Days(Data):
    return (Data[-3] > Data[-2]) and (Data[-2] < Data[-1])

#  Done
def isCounterTrendV1(ticker_data):
    """
        Rule:
            1. Bien dong gia 1 thang(22 ngay) gan day <20%
            2. Bien dong gia tuan(5 ngay) gan day < 10%
            3. Dang giam gia
                Price Avg today is the min or smaller min5 * 1.5%
    :param ticker_data: pandas.core.DataFrame
    """
    last22 = ticker_data.tail(22)
    ticker_data22 = last22.copy()
    ticker_data22['avgHL'] = ticker_data22.apply(lambda row: (row.High + row.Low) / 2, axis=1)
    last5 = ticker_data22.tail(5)
    ticker_data5 = last5.copy()
    min22ByAvgHL = ticker_data22[ticker_data22.AvgHL == ticker_data22.AvgHL.min()]
    minAvgHL22 = min22ByAvgHL.AvgHL.values[0]
    max22ByAvgHL = ticker_data22[ticker_data22.AvgHL == ticker_data22.AvgHL.max()]
    maxAvgHL22 = max22ByAvgHL.AvgHL.values[0]
    diffAvgHL22 = (maxAvgHL22 - minAvgHL22) * 100 / maxAvgHL22
    if diffAvgHL22 > 0.21:
        return False
    min5ByAvgHL = ticker_data5[ticker_data5.AvgHL == ticker_data5.AvgHL.min()]
    minAvgHL5 = min5ByAvgHL.AvgHL.values[0]
    max5ByAvgHL = ticker_data5[ticker_data5.AvgHL == ticker_data5.AvgHL.max()]
    maxAvgHL5 = max5ByAvgHL.AvgHL.values[0]
    diffAvgHL5 = (maxAvgHL5 - minAvgHL5) * 100 / maxAvgHL5
    if diffAvgHL5 > 0.11:
        return False
    if ticker_data5.avgHL.values[-1] == minAvgHL5 or ticker_data5.avgHL.values[-1] < minAvgHL5 * 1.015:
        return True
    return False

#  Doing
def isCounterTrendV2(priceArrs):
    """
        Rule:
            1. Bien dong gia 1 thang(22 ngay) gan day <20%
            2. Bien dong gia tuan(5 ngay) gan day < 10%
            3. Dang giam gia
                Price Avg today is the min or smaller min5 * 1.5%
    :param priceArrs: numpy array
    """
    week_price = priceArrs[-5:-1]
    month_price = priceArrs[-22:-1]
    min_week = np.min(week_price)
    max_week = np.max(week_price)
    min_month = np.min(month_price)
    max_month = np.max(month_price)
    diff22 = (max_month - min_month) / max_month
    if diff22 > 0.21:
        return False
    diff5 = (max_week - min_week) / max_week
    if diff5 > 0.11:
        return False
    if week_price[-1] == min_week or week_price[-1] < min_week * 1.015:
        return True
    return False

#  Done
def isStockOut(priceArrs):
    """
        Rule:
            1. Bien dong gia 3 thang(3 * 22 ngay) gan day <20%
            2. Bien dong gia tuan(5 ngay) gan day < 10%
            3. Dang co dau hieu hoi phuc
                Today price is bigger than yesterday & today price is bigger than smallest price in 3 months
            4. Co kha nang sinh loi
                The biggest price in last 3 months is BIGGER than smallest price in last 5 days plus 4%
        """
    week_price = priceArrs[-5:-1]
    month3s_price = priceArrs[-66:-1]
    min_week = np.min(week_price)
    max_week = np.max(week_price)
    min_month3s = np.min(month3s_price)
    max_month3s = np.max(month3s_price)
    last = priceArrs[-1]
    prev_last = priceArrs[-2]
    # Bien dong gia 3 thang gan day <20%
    if max_month3s < min_month3s * 1.21:
        # Bien dong gia tuan gan day < 10%
        if max_week > min_week and max_week < min_week * 1.11:
            # Dang co dau hieu hoi phuc
            if last > prev_last and last > min_month3s:
                # Co kha nang sinh loi
                if max_month3s > min_week * 1.04:
                    return True
    return False


# Doing
def isFollowTrending():
    return True


# Done
def isFollowTrendingV2(prices, volumes, last_open_price, multiplier_number):
    """
    Rule:
        1. Last volume is bigger than 1000000
        2. Close price yesterday is SMALLER than close price today
        3. Close price 2 days ago is SMALLER than close price today
        4. Last volume is max/biggest in last 5 days
        5. Last volume is bigger than multiplier_number * average of last 5 day volumes
        6. Today open price is smaller than today close price.
    :return:
    """
    last_5_volumns = volumes[-5::]
    last_3_prices = prices[-3::]
    max_volumn = max(last_5_volumns)
    last_volumn = last_5_volumns[-1]
    mean_f = np.mean(volumes[-5:-2])
    if last_3_prices[0] < last_3_prices[1] and last_3_prices[0] < last_3_prices[
        2] and last_volumn == max_volumn and last_volumn > multiplier_number * mean_f and last_volumn > 1000000 and last_open_price < \
            last_3_prices[2]:
        return True;
    return False


# Done
def isPriceUpTrendByRSI12D(priceArrs):
    """
    RSI 12 Days
    """
    a12days = priceArrs[-14:-2]
    totalIncrease = 0
    totalDecrease = 0
    lastPrice = priceArrs[-1]
    for data in a12days:
        close_price = data
        if close_price > lastPrice:
            totalIncrease += close_price - lastPrice
        else:
            totalDecrease += lastPrice - close_price
        lastPrice = close_price
    if totalDecrease == 0:
        return False
    RS = totalIncrease / totalDecrease
    RSI = 100 - 100 / (1 + RS)
    if RSI > 55:
        return True
    return False

# Doing
def hasSignalByBollingerBandsV1(prices):
    """
    Đường giá xuống dải Bollinger dưới: tín hiệu mua
    :param prices: numpy array
    :return:
    """
    dataframe = pd.DataFrame(prices)
    ma20 = dataframe.rolling(window=20).mean().iloc[-1].iloc[-1]
    d20STD = dataframe.rolling(window=20).std().iloc[-1].iloc[-1]
    upper = ma20 + (d20STD * 2)
    lower = ma20 - (d20STD * 2)
    if prices[-1] < lower or prices[-1] == lower:
        return 1  # buy signal
    if prices[-1] > upper or prices[-1] == upper:
        return -1  # sell signal
    return 0

