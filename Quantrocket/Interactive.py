import datetime
import pandas as pd
import Ticker
import platform
import os

# vnx = pd.read_csv('data/VNX.csv', usecols=["ticker", "exchange"])
# vnx_ticker = np.array(vnx)
vnx_ticker = Ticker.getListVN30ProfitableOfStockBreakout()
total_buy = 0
total_sell = 0
os.chdir('../')
path = os.getcwd()
for ticker in vnx_ticker:
    # ticker_id = ticker[0]
    ticker_id = ticker
    # ticker_exchange = ticker[1]
    # if ticker_exchange == 'HOSE':
    if platform.system() == 'Windows':
        file = path + '\\cophieu68\\' + ticker_id + '.csv'
    if platform.system() != 'Windows':
        file = path + '/cophieu68/' + ticker_id + '.csv'
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
    # ticker_data = pd.read_csv(file,
    #                           index_col='Date',
    #                           parse_dates=['Date'],
    #                           date_parser=date_parser,
    #                           usecols=["Close", "Volume"])
    ticker_data = pd.read_csv(file, index_col='Date', usecols=["Date", "Close", "Volume"])
    closes = ticker_data["Close"]
    volumes = ticker_data["Volume"]
    # calculate 90 day average dollar volume
    avg_dollar_volumes = (closes * volumes).rolling(90).mean()

    # rank biggest to smallest; pct=True gives percentile ranks between 0-1
    dollar_volume_ranks = avg_dollar_volumes.rank(axis=0, ascending=False, pct=True)
    have_adequate_dollar_volumes = dollar_volume_ranks <= (0.60)
    # print(have_adequate_dollar_volumes.tail())

    # Step 2: Apply momentum screen
    # Next, we identify the 10% of stocks with the strongest 12-month momentum, excluding the most recent month. First calculate the returns:
    TRADING_DAYS_PER_YEAR = 252
    TRADING_DAYS_PER_MONTH = 22
    year_ago_closes = closes.shift(TRADING_DAYS_PER_YEAR)
    month_ago_closes = closes.shift(TRADING_DAYS_PER_MONTH)
    returns = (month_ago_closes - year_ago_closes) / year_ago_closes.where(
        year_ago_closes != 0)  # avoid DivisionByZero errors
    # We identify momentum stocks by ranking on returns, but we only apply the rankings to stocks with adequate dollar volume
    returns_ranks = returns.where(have_adequate_dollar_volumes).rank(axis=0, ascending=False, pct=True)
    have_momentum = returns_ranks <= 0.10

    are_positive_days = closes.pct_change() > 0
    positive_days_last_twelve_months = are_positive_days.astype(int).rolling(TRADING_DAYS_PER_YEAR).sum()

    positive_days_last_twelve_months_ranks = positive_days_last_twelve_months.where(have_momentum).rank(axis=0,
                                                                                                        ascending=False,
                                                                                                        pct=True)
    have_smooth_momentum = positive_days_last_twelve_months_ranks <= 0.50

    long_signals = have_smooth_momentum.astype(int)

    daily_signal_counts = long_signals.abs().sum(axis=0)

    weights = long_signals.div(daily_signal_counts, axis=0).fillna(0)
    print(weights.where(weights!=0).stack().tail())
    exit()