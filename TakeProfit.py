#
def byPercentage(percent):
    return 1 + percent/100

def by4Percentage():
    return 1 + 0.04

def by8Percentage():
    return 1 + 0.08

def by15Percentage():
    return 1 + 0.15

def takeProfit(percent, current_price, buy_price):
    if current_price > percent/100 * buy_price:
        return True
    return False