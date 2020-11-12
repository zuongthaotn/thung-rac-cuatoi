
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

def getATR(lookback, high_price, low_price):
    """
    ATR(100) - It returns the average height of a candle within the last 100 bars.
        1. ATR(100) = ((high1-low1) +(high2-low2) + ... + (high100-low100))/100
        2. ATR(100) = high.rolling(100).mean() - low.rolling(100).mean()
    :param int lookback:
    :param pandas high_price:
    :param pandas low_price:
    :return float:
    """
    atr = high_price.rolling(lookback).mean() - low_price.rolling(lookback).mean()
    return atr[-1]