def convertToJapanCandle(ticker_data):
    ticker_data['Height'] = ticker_data.apply(lambda x: x['High'] - x['Low'], axis=1)
    ticker_data['Body'] = ticker_data.apply(lambda x: abs(x['Close'] - x['Open']), axis=1)
    ticker_data['UpShadow'] = ticker_data.apply(
        lambda x: (x['High'] - x['Close']) if (x['Close'] > x['Open']) else (x['High'] - x['Open']), axis=1)
    ticker_data['LowerShadow'] = ticker_data.apply(
        lambda x: (x['Open'] - x['Low']) if (x['Close'] > x['Open']) else (x['Close'] - x['Low']), axis=1)
    return ticker_data


def isHammer(_4daysData):
    """
    # In a down trend (base on High price)
    # Small body height (base on total height)
    # Small or none upper shadow

    :param _4daysData: pandas.core.DataFrame:
    :return:
    """
    h_prices = _4daysData.High
    body = _4daysData.Body
    height = _4daysData.Height
    u = _4daysData.UpShadow
    isDownTrend = isSmallBody = isSmallUpperShadow = False
    if h_prices[-1] < h_prices[-2]:
        if h_prices[-2] < h_prices[-3]:
            if h_prices[-3] < h_prices[-4]:
                # print("Down Trend")
                isDownTrend = True
    if body[-1] < 0.45 * height[-1]:
        # print("Small body")
        isSmallBody = True
    if u[-1] == 0 or u[-1] < 0.1 * height[-1]:
        # print("Small upper shadow")
        isSmallUpperShadow = True

    if isDownTrend is True and isSmallBody is True and isSmallUpperShadow is True:
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
    if uShadow[-1] == 0 or (float(uShadow[-1]) < 0.1 * float(height[-1]) and float(body[-1]) < 0.3 * float(lShadow[-1])):
        isSmallUpperShadow = True

    if isUpTrend is True and isSmallBody is True and isSmallUpperShadow is True:
        print(_4daysData.tail(1))
        print(height[-1])
        print(body[-1])
        print(lShadow[-1])
        print(0.3 * float(lShadow[-1]))
        return True
    else:
        return False