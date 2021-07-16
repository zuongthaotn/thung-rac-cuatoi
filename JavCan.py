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

UMBRELLA_BODY_HEIGHT_RATE = 0.3
UMBRELLA_BOTTOM_HEIGHT_RATE = 0.65


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

def isUmbrellaCandlestick(body, height, up, bot):
    if up < SHAVEN_UP_SHADOW_HEIGHT_RATE * height:
        if body < UMBRELLA_BODY_HEIGHT_RATE * height:
            if bot > UMBRELLA_BOTTOM_HEIGHT_RATE * height:
                return True
    return False


####------------------------------------------------------------------------------------------------------------#####

def isHammer(_4daysData):
    """
    # In a down trend (base on High price)
    # Small body height (base on total height)
    # Small or none upper shadow
    # Body is in upper part of candlestick the below shadow is very long( at least x2 body)

    :param _4daysData: pandas.core.DataFrame:
    :return bool:
    """
    h_prices = _4daysData.High
    body = _4daysData.Body
    height = _4daysData.Height
    u = _4daysData.UpShadow
    l = _4daysData.LowerShadow
    isDownTrend = isSmallBody = isSmallUpperShadow = hasLongTail = False
    if h_prices[-1] < h_prices[-2]:
        if h_prices[-2] < h_prices[-3]:
            if h_prices[-3] < h_prices[-4]:
                isDownTrend = True
    if body[-1] < 0.45 * height[-1]:
        isSmallBody = True
    if u[-1] == 0 or u[-1] < 0.1 * height[-1]:
        isSmallUpperShadow = True
    if l[-1] > 2 * body:
        hasLongTail = True

    if isDownTrend is True and isSmallBody is True and isSmallUpperShadow is True and hasLongTail is True:
        return True
    else:
        return False


def isHangingMan(_4daysData):
    """
    # In a up trend (base on High price)
    # Small body height (base on total height)
    # Small or none upper shadow

    :param _4daysData: pandas.core.DataFrame:
    :return:
    """
    h_prices = _4daysData.High
    body = _4daysData.Body
    height = _4daysData.Height
    uShadow = _4daysData.UpShadow
    lShadow = _4daysData.LowerShadow
    isUpTrend = isSmallBody = isSmallUpperShadow = False
    if h_prices[-1] > h_prices[-2]:
        if h_prices[-2] > h_prices[-3]:
            if h_prices[-3] > h_prices[-4]:
                isUpTrend = True
    if float(body[-1]) < 0.45 * float(height[-1]):
        isSmallBody = True
    if uShadow[-1] == 0 or (
            float(uShadow[-1]) < 0.1 * float(height[-1]) and float(body[-1]) < 0.3 * float(lShadow[-1])):
        isSmallUpperShadow = True

    if isUpTrend is True and isSmallBody is True and isSmallUpperShadow is True:
        return True
    else:
        return False
