import numpy as np;

#  Done
def isStockOut(priceArrs):
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
        # Bien dong gia tuan gan day 10%
        if max_week > min_week and max_week < min_week * 1.11:
            # Dang co dau hieu hoi phuc
            if last > prev_last and last > min_month3s:
                # Co kha nang sinh loi
                if max_month3s > min_week * 1.04:
                    return True
    return False


# Doing
def isFollowTrending():
    """
    Rule:

    :return:
    """
    return True;


# Doing
def isPriceUpTrendByRSI(priceArrs):
    a12days = priceArrs[-14:-2]
    totalIncrease = 0
    totalDecrease = 0
    lastPrice = priceArrs[-15]
    for data in a12days:
        close_price = data
        if close_price > lastPrice:
            totalIncrease += close_price - lastPrice
        else:
            totalDecrease += lastPrice - close_price
        lastPrice = close_price
    RS = totalIncrease / totalDecrease
    RSI = 100 - 100 / (1 + RS)
    return


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
