import method.algofuncs as _af

####------------------------------------------------------------------------------------------------------------#####
def convertToJapanCandle(ticker_data):
    ticker_data['Height'] = ticker_data.apply(lambda x: x['High'] - x['Low'], axis=1)
    ticker_data['Body'] = ticker_data.apply(lambda x: abs(x['Close'] - x['Open']), axis=1)
    ticker_data['UpShadow'] = ticker_data.apply(
        lambda x: (x['High'] - x['Close']) if (x['Close'] > x['Open']) else (x['High'] - x['Open']), axis=1)
    ticker_data['LowerShadow'] = ticker_data.apply(
        lambda x: (x['Open'] - x['Low']) if (x['Close'] > x['Open']) else (x['Close'] - x['Low']), axis=1)
    return ticker_data


####------------------------------------------------------------------------------------------------------------#####

BIG_BODY_PRICE_RATE = 0.04  # 4%
SMALL_BODY_PRICE_RATE = 0.01

UP_SHADOW_HEIGHT_RATE_65 = 0.65
UP_SHADOW_HEIGHT_RATE_30 = 0.30
UP_SHADOW_HEIGHT_RATE_25 = 0.25
UP_SHADOW_HEIGHT_RATE_05 = 0.05

BODY_HEIGHT_RATE_85 = 0.85  # for compare 4/5
BODY_HEIGHT_RATE_60 = 0.60  # for compare 1/2
BODY_HEIGHT_RATE_45 = 0.45  # for compare 1/2
BODY_HEIGHT_RATE_35 = 0.35  # for compare 1/3
BODY_HEIGHT_RATE_30 = 0.3  # for compare 1/3
BODY_HEIGHT_RATE_20 = 0.2  # for compare 1/4
BODY_HEIGHT_RATE_05 = 0.05  # for compare 1/20

LOWER_SHADOW_HEIGHT_RATE_65 = 0.65
LOWER_SHADOW_HEIGHT_RATE_30 = 0.30
LOWER_SHADOW_HEIGHT_RATE_25 = 0.25
LOWER_SHADOW_HEIGHT_RATE_05 = 0.05


##### --------------------------------------------------------------------------------- #####
def isBodyOver85(body, height):
    return True if body > BODY_HEIGHT_RATE_85 * height else False


def isBodyOver60(body, height):
    return True if body > BODY_HEIGHT_RATE_60 * height else False


def isBodyOver45(body, height):
    return True if body > BODY_HEIGHT_RATE_45 * height else False


def isBigBody(body, height, _open, _close):
    maxPrice = _open if _open > _close else _close
    if isBodyOver45(body, height) and body > BIG_BODY_PRICE_RATE * maxPrice:
        return True
    return False


def isSmallBody(body, height, _open, _close):
    maxPrice = _open if _open > _close else _close
    if isBodyLess35(body, height) and body < SMALL_BODY_PRICE_RATE * maxPrice:
        return True
    return False


def isBodyLess45(body, height):
    return True if body < BODY_HEIGHT_RATE_45 * height else False


def isBodyLess35(body, height):
    return True if body < BODY_HEIGHT_RATE_35 * height else False


def isBodyLess20(body, height):
    return True if body < BODY_HEIGHT_RATE_20 * height else False


def isDoji(body, height):
    if body < BODY_HEIGHT_RATE_05 * height:
        return True
    return False


##### --------------------------------------------------------------------------------- #####

def isWhiteCandlestick(open_price, close_price):
    if close_price > open_price:
        return True
    return False


def isBlackCandlestick(open_price, close_price):
    if close_price < open_price:
        return True
    return False


def isSpinningTopCandlestick(body, height, up, bot):
    if body < BODY_HEIGHT_RATE_35 * height:
        if up > UP_SHADOW_HEIGHT_RATE_30 * height:
            if bot > LOWER_SHADOW_HEIGHT_RATE_30 * height:
                return True
    return False


def isHammer(body, height, up, bot):
    if up < UP_SHADOW_HEIGHT_RATE_05 * height:
        if body < BODY_HEIGHT_RATE_30 * height:
            if bot > LOWER_SHADOW_HEIGHT_RATE_65 * height:
                return True
    return False


def isInvertedHammer(body, height, up, bot):
    if up > UP_SHADOW_HEIGHT_RATE_65 * height:
        if body < BODY_HEIGHT_RATE_30 * height:
            if bot < LOWER_SHADOW_HEIGHT_RATE_05 * height:
                return True
    return False


def isShavenHead(height, up):
    """
    Nến cạo đầu
    :param height:
    :param up:
    :return:
    """
    if up < UP_SHADOW_HEIGHT_RATE_05 * height:
        return True
    return False


def isShavenBottom(height, bot):
    """
    Nến cạo đáy
    :param height:
    :param bot:
    :return:
    """
    if bot < LOWER_SHADOW_HEIGHT_RATE_05 * height:
        return True
    return False


def isUmbrellaCandlestick(body, height, up, bot):
    return isHammer(body, height, up, bot)


####------------------------------------------------------------------------------------------------------------#####
def isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = False
    if _close[-2] > _close[-3] > _close[-4]:
        isUpTrend = True

    if _high[-2] > _high[-3] > _high[-4]:
        isUpTrend = True

    if isWhiteCandlestick(_open[-2], _close[-2]) \
            and isWhiteCandlestick(_open[-3], _close[-3]) \
            and isWhiteCandlestick(_open[-4], _close[-4]):
        isUpTrend = True

    k = 0
    for i in [-2, -3, -4, -5, -6, -7]:
        if isWhiteCandlestick(_open[i], _close[i]) is True:
            k = k + 1

    if k > 3:
        isUpTrend = True

    return isUpTrend


def isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down):
    if isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down):
        return False
    isDownTrend = False
    if _close[-2] < _close[-3] < _close[-4]:
        isDownTrend = True
    if _low[-2] < _low[-3] < _low[-4]:
        isDownTrend = True
    if isBlackCandlestick(_open[-2], _close[-2]) \
            and isBlackCandlestick(_open[-3], _close[-3]) \
            and isBlackCandlestick(_open[-4], _close[-4]):
        isDownTrend = True

    k = 0
    for i in [-2, -3, -4, -5, -6, -7]:
        if isBlackCandlestick(_open[i], _close[i]) is True:
            k = k + 1

    if k > 3:
        isDownTrend = True

    return isDownTrend


####------------------------------------------------------------------------------------------------------------#####
def isUpTrendV2ByRSI(_close):
    return True if _af.RSIV2(_close, 5) > 55 else False

def isDownTrendV2ByRSI(_close):
    # return True if _af.RSIV2(_close, 5) < 45 else False
    rsi = _af.RSI(_close, 5).tail(1).item()
    return True if rsi < 45 else False
####------------------------------------------------------------------------------------------------------------#####

def isHammerModel(_open, _close, _high, _low, _body, _height, _up, _down):
    """
    # In a down trend
    # today is a hammer candlestick
    :param :
    :return bool:
    """
    isDownTrend = isDownTrendV2ByRSI(_close[:-2])
    _iuc = isHammer(_body[-1], _height[-1], _up[-1], _down[-1])
    # _iwc = isWhiteCandlestick(_open[-1], _close[-1])
    if isDownTrend is True and _iuc is True:
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
    # isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    isUpTrend = isUpTrendV2ByRSI(_close[:-2])
    _iuc = isUmbrellaCandlestick(_body[-1], _height[-1], _up[-1], _down[-1])
    if isUpTrend is True and _iuc is True:
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
    todayHasBigBody = isBigBody(_body[-1], _height[-1], _open[-1], _close[-1])
    if todayHasBigBody is False:
        return False
    prevDayIsSpinningCandlestick = isSpinningTopCandlestick(_body[-2], _height[-2], _up[-2], _down[-2])
    if prevDayIsSpinningCandlestick is True and _body[-1] < 2 * _body[-2]:
        return False

    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    prevDayIsBlackCandlestick = isBlackCandlestick(_open[-2], _close[-2])
    prevDayMaxOpenClose = _open[-2] if _open[-2] > _close[-2] else _close[-2]
    prevDayMinOpenClose = _open[-2] if _open[-2] < _close[-2] else _close[-2]
    prevDayIsDoJi = isDoji(_body[-2], _height[-2])
    todayIsWhiteCandlestick = isWhiteCandlestick(_open[-1], _close[-1])
    todayMaxOpenClose = _open[-1] if _open[-1] > _close[-1] else _close[-1]
    todayMinOpenClose = _open[-1] if _open[-1] < _close[-1] else _close[-1]

    if isDownTrend is True \
            and (prevDayIsBlackCandlestick is True or prevDayIsDoJi is True) \
            and prevDayMaxOpenClose <= 0.96 * todayMaxOpenClose \
            and prevDayMinOpenClose >= todayMinOpenClose \
            and todayIsWhiteCandlestick is True:
        return True
    return False


def isBearishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    todayIsBlackCandlestick = isBlackCandlestick(_open[-1], _close[-1])
    prevDayMaxOpenClose = _open[-2] if _open[-2] > _close[-2] else _close[-2]
    prevDayMinOpenClose = _open[-2] if _open[-2] < _close[-2] else _close[-2]
    todayMaxOpenClose = _open[-1] if _open[-1] > _close[-1] else _close[-1]
    todayMinOpenClose = _open[-1] if _open[-1] < _close[-1] else _close[-1]

    if isUpTrend is True \
            and prevDayMaxOpenClose <= todayMaxOpenClose \
            and prevDayMinOpenClose >= todayMinOpenClose \
            and todayIsBlackCandlestick is True:
        return True
    return False


def isPiercingPattern(_open, _close, _high, _low, _body, _height, _up, _down):
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    the1stDayIsBlackCandlestick = isBlackCandlestick(_open[-2], _close[-2])
    the1stDayHasBigBody = isBodyOver45(_body[-2], _height[-2])
    the2ndDayIsWhiteCandlestick = isWhiteCandlestick(_open[-1], _close[-1])
    the2ndDayHasBigBody = isBodyOver45(_body[-1], _height[-1])
    the2ndDayFallInThe1stDay = True if _open[-1] < _close[-2] < _close[-1] < _open[-2] else False
    if isDownTrend is True and the1stDayIsBlackCandlestick is True and the1stDayHasBigBody is True \
            and the2ndDayIsWhiteCandlestick is True and the2ndDayHasBigBody is True \
            and the2ndDayFallInThe1stDay is True :
        return True
    return False


def isDarkCloudCoverPattern(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    prevDayIsWhiteCandlestick = isWhiteCandlestick(_open[-2], _close[-2])
    prevDayHasBigBody = isBodyOver45(_body[-2], _height[-2])
    todayIsBlackCandlestick = isBlackCandlestick(_open[-1], _close[-1])
    todayHasBigBody = isBodyOver45(_body[-1], _height[-1])
    todayFallInYesterday = True if _open[-2] < _close[-1] < _close[-2] < _open[-1] else False
    if isUpTrend is True and prevDayIsWhiteCandlestick is True and prevDayHasBigBody is True \
            and todayIsBlackCandlestick is True and todayHasBigBody is True \
            and todayFallInYesterday is True:
        return True
    return False


def isMorningStarsPattern(_open, _close, _high, _low, _body, _height, _up, _down):
    the1stDayIsBlackCandlestick = isBlackCandlestick(_open[-3], _close[-3])
    the1stDayHasBigBody = isBodyOver45(_body[-3], _height[-3])
    the2ndDayIsSmallBody = isBodyLess35(_body[-2], _height[-2])
    the2ndMaxOpenClosePrice = _open[-2] if _open[-2] > _close[-2] else _close[-2]
    the2ndDayHasGap = True if the2ndMaxOpenClosePrice < _close[-3] else False
    todayIsWhiteCandlestick = isWhiteCandlestick(_open[-1], _close[-1])
    todayFallInThe1stDay = True if _open[-3] > _close[-1] > _close[-3] and _body[-1] > 2 * _body[-2] else False
    if the1stDayIsBlackCandlestick is True and the1stDayHasBigBody is True \
            and the2ndDayIsSmallBody is True and the2ndDayHasGap is True \
            and todayIsWhiteCandlestick is True and todayFallInThe1stDay is True:
        return True
    return False


def isEveningStarsPattern(_open, _close, _high, _low, _body, _height, _up, _down):
    the1stDayIsWhiteCandlestick = isWhiteCandlestick(_open[-3], _close[-3])
    the1stDayHasBigBody = isBodyOver45(_body[-3], _height[-3])
    the2ndDayIsSmallBody = isBodyLess35(_body[-2], _height[-2])
    the2ndMinOpenClosePrice = _open[-2] if _open[-2] < _close[-2] else _close[-2]
    the2ndDayHasGap = True if the2ndMinOpenClosePrice > _close[-3] else False
    todayIsBlackCandlestick = isBlackCandlestick(_open[-1], _close[-1])
    todayFallInThe1stDay = True if _open[-3] < _close[-1] < _close[-3] and _body[-1] > 2 * _body[-2] else False
    if the1stDayIsWhiteCandlestick is True and the1stDayHasBigBody is True \
            and the2ndDayIsSmallBody is True and the2ndDayHasGap is True \
            and todayIsBlackCandlestick is True and todayFallInThe1stDay is True:
        return True
    return False


def isThreeBlackCrowsPattern(_open, _close, _high, _low, _body, _height, _up, _down):
    the1stDayIsBlackCandlestick = isBlackCandlestick(_open[-3], _close[-3])
    the2ndDayIsBlackCandlestick = isBlackCandlestick(_open[-2], _close[-2])
    todayIsBlackCandlestick = isBlackCandlestick(_open[-1], _close[-1])
    if the1stDayIsBlackCandlestick is True and the2ndDayIsBlackCandlestick is True and todayIsBlackCandlestick is True:
        return True
    return False


def isBullishHarami(_open, _close, _high, _low, _body, _height, _up, _down):
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    yesterdayIsBlackCandlestick = isBlackCandlestick(_open[-2], _close[-2])
    yesterdayIsBigBody = isBodyOver45(_body[-2], _height[-2])
    toDayHasSmallBody = isSmallBody(_body[-1], _height[-1], _open[-1], _close[-1])
    todayIsDeepInYesterday = True if (_open[-2] + _close[-2]) / 2 > _open[-1] > _close[-2] else False
    if isDownTrend is True and yesterdayIsBlackCandlestick is True and yesterdayIsBigBody is True \
            and toDayHasSmallBody is True and todayIsDeepInYesterday is True:
        return True
    return False


def isBearishHarami(_open, _close, _high, _low, _body, _height, _up, _down):
    isUpTrend = isUpTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    yesterdayIsWhiteCandlestick = isWhiteCandlestick(_open[-2], _close[-2])
    yesterdayIsBigBody = isBodyOver45(_body[-2], _height[-2])
    toDayHasSmallBody = isSmallBody(_body[-1], _height[-1], _open[-1], _close[-1])
    todayIsDeepInYesterday = True if _open[-2] < _close[-1] < (_open[-2] + _close[-2]) / 2 else False
    if isUpTrend is True and yesterdayIsWhiteCandlestick is True and yesterdayIsBigBody is True \
            and toDayHasSmallBody is True and todayIsDeepInYesterday is True:
        return True
    return False


####------------------------------------------------------------------------------------------------------------#####
def customBuySignal01(_open, _close, _high, _low, _body, _height, _up, _down):
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    _ibc = isSpinningTopCandlestick(_body[-2], _height[-2], _up[-2], _down[-2])
    _iwc = isWhiteCandlestick(_open[-1], _close[-1])
    _ibb = isBigBody(_body[-1], _height[-1], _open[-1], _close[-1])
    if isDownTrend is True and _ibc is True \
            and _iwc is True and _ibb is True \
            and _close[-1] > _close[-2]:
        return "hasBuySignal-01"
    return False

def customBuySignal02(_open, _close, _high, _low, _body, _height, _up, _down):
    isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    the2ndDayIsDoji = isDoji(_body[-2], _height[-2])
    todayIsShavenHead = isShavenHead(_height[-1], _up[-1])
    todayIsWhite = isWhiteCandlestick(_open[-1], _close[-1])
    if isDownTrend is True and the2ndDayIsDoji is True and todayIsShavenHead is True and todayIsWhite is True:
        return "hasBuySignal-02"
    return False

def customBuySignal03(_open, _close, _high, _low, _body, _height, _up, _down):
    # isDownTrend = isDownTrendV1(_open, _close, _high, _low, _body, _height, _up, _down)
    prevDayIsShavenBottom = isShavenBottom(_height[-2], _down[-2])
    todayIsShavenHead = isShavenHead(_height[-1], _up[-1])
    todayIsWhite = isWhiteCandlestick(_open[-1], _close[-1])

    if prevDayIsShavenBottom is True and todayIsShavenHead is True and todayIsWhite is True:
        return "hasBuySignal-03"
    return False

def customBuySignal04(_open, _close, _high, _low, _body, _height, _up, _down):
    """ Optimize the Hammer pattern"""
    isDownTrend = isDownTrendV2ByRSI(_close[:-2])
    todayIsHammer = isHammer(_body[-1], _height[-1], _up[-1], _down[-1])
    todayIsWhite = isWhiteCandlestick(_open[-1], _close[-1])
    if isDownTrend is True and todayIsHammer is True and todayIsWhite is True:
        return "hasBuySignal-04"
    return False

def customSellSignal01(_open, _close, _high, _low, _body, _height, _up, _down):
    todayIsDoJi = isDoji(_body[-1], _height[-1])
    prevDayIsDoJi = isDoji(_body[-2], _height[-2])
    if todayIsDoJi is True and prevDayIsDoJi is True:
        return True

def customSellSignal02(_open, _close, _high, _low, _body, _height, _up, _down):
    yesterdayIsBlack = isBlackCandlestick(_open[-1], _close[-1])
    todayIsWhite = isWhiteCandlestick(_open[-1], _close[-1])
    bodyTodayX2Yesterday = True if _body[-1] > 1.5*_body[-2] else False
    if yesterdayIsBlack is True and todayIsWhite is True and bodyTodayX2Yesterday is True:
        return True

####------------------------------------------------------------------------------------------------------------#####

def hasBuySignal(_open, _close, _high, _low, _body, _height, _up, _down, _volume=0, _date=''):

    # Hammer Pattern not working fine with back test, bad result
    # _iHm = isHammerModel(_open, _close, _high, _low, _body, _height, _up, _down)
    # if _iHm is True:
    #     return 'isHammerModel'

    _ibu = isBullishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ibu is True:
        return 'isBullishEngulfing'

    _ipp = isPiercingPattern(_open, _close, _high, _low, _body, _height, _up, _down)
    isVolumeUp = True if _volume[-1] > 1.4 * _volume[-2] else False
    if _ipp is True and isVolumeUp is True:
        return 'isPiercingPattern'

    _ims = isMorningStarsPattern(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ims is True:
        return 'isMorningStarsPattern'

    _cBS01 = customBuySignal01(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cBS01 is True:
        return 'customBuySignal01'

    _cBS02 = customBuySignal02(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cBS02 is True:
        return 'customBuySignal02'

    _cBS03 = customBuySignal03(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cBS03 is True:
        return 'customBuySignal03'

    _cBS04 = customBuySignal04(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cBS04 is not False:
        return _cBS04

    return False


def hasSellSignal(_open, _close, _high, _low, _body, _height, _up, _down, _volume=0, _date=''):
    _ibe = isBearishEngulfing(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ibe is True:
        return 'isBearishEngulfing'

    _idc = isDarkCloudCoverPattern(_open, _close, _high, _low, _body, _height, _up, _down)
    if _idc is True:
        return 'isDarkCloudCoverPattern'

    _ies = isEveningStarsPattern(_open, _close, _high, _low, _body, _height, _up, _down)
    if _ies is True:
        return 'isEveningStarsPattern'

    _itb = isThreeBlackCrowsPattern(_open, _close, _high, _low, _body, _height, _up, _down)
    if _itb is True:
        return 'isThreeBlackCrowsPattern'

    _iha = isHangingManModel(_open, _close, _high, _low, _body, _height, _up, _down)
    if _iha is True:
        return 'isHangingManModel'

    _cSS01 = customSellSignal01(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cSS01 is True:
        return 'customSellSignal01'

    _cSS02 = customSellSignal02(_open, _close, _high, _low, _body, _height, _up, _down)
    if _cSS02 is True:
        return 'customSellSignal02'

    return False


def hasCustomBuySignal(_open, _close, _high, _low, _body, _height, _up, _down, version=0):
    if version == 1 or version == 0:
        _cBS01 = customBuySignal01(_open, _close, _high, _low, _body, _height, _up, _down)
        if _cBS01 is True:
            return 'customBuySignal01'

    if version == 2 or version == 0:
        _cBS02 = customBuySignal02(_open, _close, _high, _low, _body, _height, _up, _down)
        if _cBS02 is True:
            return 'customBuySignal02'

    if version == 3 or version == 0:
        _cBS03 = customBuySignal03(_open, _close, _high, _low, _body, _height, _up, _down)
        if _cBS03 is True:
            return 'customBuySignal03'

    return False


def hasCustomSellSignal(_open, _close, _high, _low, _body, _height, _up, _down, version=0):
    todayIsDoJi = isDoji(_body[-1], _height[-1])
    prevDayIsDoJi = isDoji(_body[-2], _height[-2])
    if todayIsDoJi is True and prevDayIsDoJi is True:
        return True
