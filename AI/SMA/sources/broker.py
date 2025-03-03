import math


class Broker:

    def __init__(self, start_capital):
        self.capital = start_capital
        self.capital_peak = start_capital
        self.equity_peak = 0
        self.equity_peak_period = 0
        self.number_of_stocks = 0
        self.expenses = 0
        self.incomes = 0
        self.is_alive = True
        self.history = []

    def do_action(self, decision, price, date=''):
        if decision[0] > 0.5:
            if not self.number_of_stocks:
                # If not buy => buy
                self.buy_all_stocks(price, date)
                self.equity_peak_period = self.number_of_stocks * price
            else:
                # if bought = > hold
                equity = self.number_of_stocks * price
                if self.equity_peak < equity:
                    self.equity_peak = equity
                if self.equity_peak_period < equity:
                    self.equity_peak_period = equity
                if (equity < self.equity_peak * 0.6 or equity < self.capital_peak * 0.8
                        or equity < self.equity_peak_period * 0.90
                        or equity < self.capital * 0.90):
                    self.is_alive = False
        elif decision[0] <= 0.5:
            # If bought => sell, if not buy => do nothing
            if self.number_of_stocks:
                self.sell_all_stocks(price, date)

    # buy all stocks that broker can afford
    def buy_all_stocks(self, stock_price, date=''):
        how_many_stocks = math.floor(self.capital / stock_price)
        self.expenses = stock_price * how_many_stocks
        self.capital -= self.expenses
        self.number_of_stocks = how_many_stocks
        if date:
            self.history.append('Buy with price {} in {}'.format(stock_price, date))

    def sell_all_stocks(self, stock_price, date=''):
        if self.number_of_stocks > 0:
            if date:
                self.history.append('Sell with price {} in {}'.format(stock_price, date))
            self.incomes = stock_price * self.number_of_stocks
            self.capital += self.incomes
            if self.capital_peak < self.capital:
                self.capital_peak = self.capital
            self.number_of_stocks = 0
