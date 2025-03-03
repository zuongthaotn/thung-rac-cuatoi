import math
import AI.EMA.sources.constants as constants

class Broker:

    def __init__(self, start_capital):
        self.capital = start_capital
        self.capital_peak = start_capital
        self.equity_peak = 0
        self.equity_peak_period = 0
        self.number_of_stocks = 0
        self.days_in_house = 0
        self.expenses = 0
        self.incomes = 0
        self.profit = 0
        self.is_alive = True
        self.num_transaction = 0
        self.win_trades = 0
        self.history = []
    # capital : tong tien sau khi ban cp
    # capital_peak : so tien LON NHAT dc tinh lai sau moi lan ban cp
    # equity : tong tien tinh theo gia tri cp dang nam giu

    def do_action(self, decision, price, date=''):
        self.profit = 0
        if self.number_of_stocks:
            """ Already has stocks """
            today_equity = self.number_of_stocks * price
            if self.equity_peak < today_equity:
                self.equity_peak = today_equity
            if self.equity_peak_period < today_equity:
                self.equity_peak_period = today_equity
            self.days_in_house += 1
            if decision[0] <= constants.SELL_SIGNAL_LINE:
                if self.days_in_house > 2:
                    self.sell_all_stocks(price, date)
                else:
                    """ Mua chua dc 2 ngay da ban, kill luon """
                    self.is_alive = False
            else:
                """
                    if bought = > hold
                    die:
                     - Lo 10% capital
                     - Mat 15% equity (equity tinh tu luc mua)
                     - Mat 50% equity peak (equity cao nhat duoc tich luy)
                     - Mat 30% capital peak (capital cao nhat duoc tich luy))
                """
                if (today_equity < self.capital * 0.90
                        or today_equity < self.equity_peak_period * 0.85
                        or today_equity < self.equity_peak * 0.5
                        or today_equity < self.capital_peak * 0.7):
                    self.is_alive = False
        else:
            """ 
                Stock is empty, ready to buy more.
                If bought => sell, if not buy => do nothing
            """
            if decision[0] >= constants.BUY_SIGNAL_LINE:
                self.buy_all_stocks(price, date)
                self.equity_peak_period = self.number_of_stocks * price
                self.days_in_house = 0

    # buy all stocks that broker can afford
    def buy_all_stocks(self, stock_price, date=''):
        how_many_stocks = math.floor(self.capital / stock_price)
        self.expenses = stock_price * how_many_stocks
        self.capital -= self.expenses
        self.number_of_stocks = how_many_stocks
        if date:
            self.history.append('Buy with price {} in {}'.format(stock_price, date))

    def sell_all_stocks(self, stock_price, date=''):
        if date:
            self.history.append('Sell with price {} in {}'.format(stock_price, date))
        self.incomes = stock_price * self.number_of_stocks
        self.profit = self.incomes - self.expenses
        if self.profit > 0:
            self.win_trades += 1
        self.capital += self.incomes
        if self.capital_peak < self.capital:
            self.capital_peak = self.capital
        self.number_of_stocks = 0
        self.num_transaction += 1
        self.days_in_house = 0
        self.expenses = 0
        self.incomes = 0
