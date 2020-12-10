
def takeProfitByPercent(percent, current_price, buy_price):
    if current_price > (1 + percent/100) * buy_price:
        return True
    return False

def shouldCutLossByPercent(percent, current_price, buy_price):
    if current_price < (1 - percent/100) * buy_price:
        return True
    return False

def shouldSellByATR():
    return False