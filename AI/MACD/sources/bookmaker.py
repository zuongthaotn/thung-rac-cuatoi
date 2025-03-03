import math


class Bookmaker:

    def __init__(self, start_capital):
        self.capital = start_capital
        self.equity_peak = start_capital
        self.number_of_stocks = 0
        self.buy_price = 0
        self.sell_price = 0
        self.expenses = 0
        self.incomes = 0
        self.history = []

    # buy all stocks that bookmaker can afford
    def buy_all_stocks(self, stock_price, date=''):
        how_many_stocks = math.floor(self.capital / stock_price)
        if self.canBuyMore(stock_price):
            self.buy_price = stock_price
            self.sell_price = 0
            self.expenses = stock_price * how_many_stocks
            self.capital -= self.expenses
            self.number_of_stocks = how_many_stocks
            if date:
                self.history.append('Buy with price {} in {}'.format(stock_price, date))

    def sell_all_stocks(self, stock_price, date=''):
        if self.number_of_stocks > 0:
            if date:
                self.history.append('Sell with price {} in {}'.format(stock_price, date))
            self.sell_price = stock_price
            self.buy_price = 0
            self.incomes = stock_price * self.number_of_stocks
            self.capital += self.incomes
            if self.equity_peak < self.capital:
                self.equity_peak = self.capital
            self.number_of_stocks = 0

    def canBuyMore(self, stock_price):
        if stock_price == 0:
            return False
        how_many_stocks = math.floor(self.capital / stock_price)
        if how_many_stocks > 0:
            return True
        else:
            return False

    def canSellStock(self):
        if self.number_of_stocks > 0:
            return True
        else:
            return False
