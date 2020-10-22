#
def by4Percentage():
    return 1 - 0.04

def by8Percentage():
    return 1 - 0.08

def byATR():
    return False

def shouldCutLossByPercent(percent, current_price, buy_price):
    if current_price < (1 - percent/100) * buy_price:
        return True
    return False