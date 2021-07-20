def convertToJapanCandle(ticker_data):
    ticker_data['Height'] = ticker_data.apply(lambda x: x['High'] - x['Low'], axis=1)
    ticker_data['Body'] = ticker_data.apply(lambda x: abs(x['Close'] - x['Open']), axis=1)
    ticker_data['UpShadow'] = ticker_data.apply(
        lambda x: (x['High'] - x['Close']) if (x['Close'] > x['Open']) else (x['High'] - x['Open']), axis=1)
    ticker_data['LowerShadow'] = ticker_data.apply(
        lambda x: (x['Open'] - x['Low']) if (x['Close'] > x['Open']) else (x['Close'] - x['Low']), axis=1)
    return ticker_data


####------------------------------------------------------------------------------------------------------------#####
SPINNING_BODY_HEIGHT_RATE = 0.3
SPINNING_UP_SHADOW_HEIGHT_RATE = 0.25
SPINNING_LOWER_SHADOW_HEIGHT_RATE = 0.25

SHAVEN_UP_SHADOW_HEIGHT_RATE = 0.05
SHAVEN_LOWER_SHADOW_HEIGHT_RATE = 0.05

DOJI_BODY_HEIGHT_RATE = 0.05
BIG_BODY_HEIGHT_RATE = 0.8

UMBRELLA_BODY_HEIGHT_RATE = 0.3
UMBRELLA_BOTTOM_HEIGHT_RATE = 0.65

SMALL_BODY_RATE = 0.45

def isWhiteCandlestick(open_price, close_price):
    if close_price > open_price:
        return True
    return False


def isBlackCandlestick(open_price, close_price):
    if close_price < open_price:
        return True
    return False


def isSpinningTopCandlestick(body, height, up, bot):
    if body < SPINNING_BODY_HEIGHT_RATE * height:
        if up > SPINNING_UP_SHADOW_HEIGHT_RATE * height:
            if bot > SPINNING_LOWER_SHADOW_HEIGHT_RATE * height:
                return True
    return False


def isShavenHead(height, up):
    """
    Nến cạo đầu
    :param height:
    :param up:
    :return:
    """
    if up < SHAVEN_UP_SHADOW_HEIGHT_RATE * height:
        return True
    return False


def isShavenBottom(height, bot):
    """
    Nến cạo đáy
    :param height:
    :param bot:
    :return:
    """
    if bot < SHAVEN_LOWER_SHADOW_HEIGHT_RATE * height:
        return True
    return False


def isDoji(body, height):
    if body < DOJI_BODY_HEIGHT_RATE * height:
        return True
    return False

def isBigBody(body, height):
    if body > BIG_BODY_HEIGHT_RATE * height:
        return True
    return False

def isUmbrellaCandlestick(body, height, up, bot):
    if up < SHAVEN_UP_SHADOW_HEIGHT_RATE * height:
        if body < UMBRELLA_BODY_HEIGHT_RATE * height:
            if bot > UMBRELLA_BOTTOM_HEIGHT_RATE * height:
                return True
    return False


def isHammer(_open, close, body, height, up, bot):
    if isUmbrellaCandlestick(body, height, up, bot) is True and isWhiteCandlestick(_open, close):
        return True
    return False


def isHangingMan(_open, close, body, height, up, bot):
    if isUmbrellaCandlestick(body, height, up, bot) is True and isBlackCandlestick(_open, close):
        return True
    return False


####------------------------------------------------------------------------------------------------------------#####
def isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = False
    if _close[-2] > _close[-3] and _close[-3] > _close[-4]:
        isUpTrend = True

    if isWhiteCandlestick(_open[-2], _close[-2]) \
            and isWhiteCandlestick(_open[-3], _close[-3]) \
            and isWhiteCandlestick(_open[-4], _close[-4]):
        isUpTrend = True

    k = 0
    for i in [-2, -3, -4, -5, -6, -7]:
        if isWhiteCandlestick(_open[i], _close[i]) is True or isDoji(_body[i], _height[i]) is True:
            k = k + 1

    if k > 3:
        isUpTrend = True

    return isUpTrend

def isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down):
    isDownTrend = False
    if _close[-2] < _close[-3] and _close[-3] < _close[-4]:
        isDownTrend = True
    if isBlackCandlestick(_open[-2], _close[-2]) \
            and isBlackCandlestick(_open[-3], _close[-3]) \
            and isBlackCandlestick(_open[-4], _close[-4]):
        isDownTrend = True

    k = 0
    for i in [-2, -3, -4, -5, -6, -7]:
        if isBlackCandlestick(_open[i], _close[i]) is True or isDoji(_body[i], _height[i]) is True:
            k = k + 1

    if k > 3:
        isDownTrend = True

    return isDownTrend

####------------------------------------------------------------------------------------------------------------#####

def isHammerModel(_open, _close, _high, _low, _body, _height, _up, _down):
    """
    # In a down trend (base on High price)
    # Small body height (base on total height)
    # Small or none upper shadow
    # Body is in upper part of candlestick the below shadow is very long( at least x2 body)

    :param :
    :return bool:
    """
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    _ih = isHammer(_open[-1], _close[-1], _body[-1], _height[-1], _up[-1], _down[-1])
    if isDownTrend is True and _ih is True:
        return True
    else:
        return False


def isHangingManModel(_open, _close, _high, _low, _body, _height, _up, _down):
    """
    # In a up trend (base on High price)
    # Small body height (base on total height)
    # Small or none upper shadow

    :param :
    :return:
    """
    isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    _ih = isHammer(_open[-1], _close[-1], _body[-1], _height[-1], _up[-1], _down[-1])
    if isUpTrend is True and _ih is True:
        return True
    else:
        return False


def isBullishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down):
    """
    :param _open numpy array:
    :param _close:
    :param _body:
    :param _height:
    :param _up:
    :param _down:
    :return:
    """
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    prevDayIsBlackCandlestick = isBlackCandlestick(_open[-2], _close[-2])
    todayIsWhiteCandlestick = isWhiteCandlestick(_open[-1], _close[-1])
    if isDownTrend is True \
            and prevDayIsBlackCandlestick is True \
            and _open[-2] <= _close[-1]  \
            and _close[-2] <= _open[-2] \
            and todayIsWhiteCandlestick is True:
        return True
    return False


def isBearishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    prevDayIsWhiteCandlestick = isWhiteCandlestick(_open[-2], _close[-2])
    todayIsBlackCandlestick = isBlackCandlestick(_open[-1], _close[-1])
    todayHasBigBody = isBigBody(_body[-1], _height[-1])
    if isUpTrend is True \
            and prevDayIsWhiteCandlestick is True \
            and _close[-2] <= _open[-1] \
            and _open[-2] >= _close[-1] \
            and todayIsBlackCandlestick is True\
            and todayHasBigBody is True:
        return True
    return False

def hasBuySignal(_open, _close, _high, _low, _body, _height, _up, _down):
    _ibu = isBullishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down)
    _iha = isHangingManModel(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ibu is True or _iha is True:
        return True


def hasSellSignal(_open, _close, _high, _low, _body, _height, _up, _down):
    _ibe = isBearishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down)
    _iha = isHangingManModel(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ibe is True or _iha is True:
        return True
