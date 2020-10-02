# %% Import libraries
import os
import pandas as pd
from datetime import datetime

# %% Get VN stocks data
def get_pricing(symbol, start_date='2018-01-01', end_date=None, frequency='daily', fields=None):
    """Get pricing

    Keyword arguments:
    symbol (str) -- Asset symbol
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to '2018-01-01'.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to None.
    frequency ({'daily', 'minute'}, optional) -- Resolution of the data to be returned
    fields (str or list, optional) -- String or list drawn from {'open', 'high', 'low', 'close', 'volume'}. Default behavior is to return all fields.
    """
    usecols = None
    if fields is not None:
        usecols = ['date']
        if type(fields) is list:
            for field in fields:
                usecols.append(field)
        else:
            usecols.append(fields)

    file = 'Price'
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
    if frequency == 'minute':
        file = 'Prices'
        date_parser = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M')

    for exchange in os.listdir('../data'):
        filepath = '../data/{}/{}/{}.csv'.format(exchange, symbol, file)
        if os.path.isfile(filepath):
            prices = pd.read_csv(
                filepath,
                index_col='date',
                parse_dates=['date'],
                date_parser=date_parser,
                usecols=usecols
            )[start_date:end_date]
            prices.exchange = exchange
            prices.symbol = symbol
            prices['date'] = prices.index
            return prices

    return None


def get_prices(*symbols, start_date='2018-01-01', end_date=None, frequency='daily', field='close'):
    """Get prices

    Keyword arguments:
    symbols (list of str) -- Asset symbols
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to '2018-01-01'.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to None.
    frequency ({'daily', 'minute'}, optional) -- Resolution of the data to be returned
    field (str, optional) -- String or list drawn from {'open', 'high', 'low', 'close', 'volume'}. Default behavior is to return 'close'.
    """
    prices = None
    for symbol in symbols:
        price = get_pricing(symbol, start_date=start_date, end_date=end_date, frequency=frequency, fields=field)
        if price is None:
            continue

        price = price.rename(columns={field: symbol})
        if prices is None:
            prices = price
        else:
            prices = prices.join(price)

    return prices


def get_events(symbol, start_date=None, end_date=None):
    """Get events

    Keyword arguments:
    symbol (str) -- Asset symbol
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date. Defaults to None.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date. Defaults to None.
    """
    for exchange in os.listdir('../data'):
        filepath = '../data/{}/{}/Events.csv'.format(exchange, symbol)
        if os.path.isfile(filepath):
            return pd.read_csv(
                filepath,
                index_col='disclosuredDate',
                parse_dates=['disclosuredDate'],
                date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d')
            )[start_date:end_date]

    return None


def StocksVN():
    """Get list of stocks in VN Market
    """
    return pd.read_csv('../data/VNX.csv', index_col='ticker')


def TradableStocksVN():
    """Get list of tradable stocks in VN Market
    """
    tickers = StocksVN()
    return tickers[tickers.AvgValue20P > 8e8]

def join_price(price, fundamental):
    fund = fundamental
    if not isinstance(fundamental.index, pd.DatetimeIndex):
        fund = fund.reset_index().set_index('date')

    fund = pd.DataFrame(index=price.index).join(fund, how='outer')
    return price.join(fund.fillna(method='ffill'))