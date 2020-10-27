import numpy as np;

#  Done
def isStockOut(priceArrs):
    """
        Rule:
            1. Bien dong gia 3 thang(22 ngay) gan day <20%
            2. Bien dong gia tuan(5 ngay) gan day < 10%
            3. Dang co dau hieu hoi phuc
                Today price is bigger than yesterday & today price is bigger than smallest price in 3 months
            4. Co kha nang sinh loi
                The biggest price in last 3 months is BIGGER than smallest price in last 5 days plus 40%
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

def getAllTickers():
    import os
    import platform
    import pandas as pd
    path = os.getcwd()
    if platform.system() == 'Windows':
        vnx_file = path + '\\VNX.csv'
    if platform.system() != 'Windows':
        vnx_file = path + '/VNX.csv'

    vnx = pd.read_csv(vnx_file, usecols=["ticker", "exchange"])
    vnx_ticker = np.array(vnx)
    return vnx_ticker