from datetime import datetime
import json
import pickle
from pathlib import Path

#
LONG_TYPE = 'long'
SHORT_TYPE = 'short'
#
QTY_ORDER = 1
STOP_LOSS_STEP = 3
RR = 5
#
GOOD_POSITION = 1
BAD_POSITION = -1
#
NO_SIGNAL = ''
BUY_SIGNAL = 'long'
CLOSE_BUY_SIGNAL = 'close_long'
SWITCH_TO_BUY_SIGNAL = 'switch_long'
SELL_SIGNAL = 'short'
CLOSE_SELL_SIGNAL = 'close_short'
SWITCH_TO_SELL_SIGNAL = 'switch_short'
#
DECISION_HOLD = 'hold'
DECISION_LONG = 'long'
DECISION_SHORT = 'short'
DECISION_CLOSE_LONG = 'close_long'
DECISION_CLOSE_SHORT = 'close_short'
DECISION_NONE = ''
MIN_SR_RANGE = 3
#
WORKER_FILE = 'worker.pkl'


# Decision is made and based on signal & technical indicators
class Worker:
    def __init__(self):
        # data
        self.broker = None
        self.last_data = None
        self.current_time = None
        self.mode = 'live'
        self.algo_version = 'custom_v19'
        self.changed = False
        # price
        self.current_price = 0
        self.min_oc = 0
        self.max_oc = 0
        self.breakout = 0
        self.resistance = 0
        self.support = 0
        # signal
        self.signal = NO_SIGNAL
        self.decision = DECISION_NONE
        self.position = BAD_POSITION
        # deal
        self.expected_price = 0
        self.risk = 0
        self.reward = 0
        self.stoploss = 0
        self.take_profit = 0
        self.force_stoploss = 0
        self.reason = ''
        #
        self.worker_data = None

    def set_data(self, **kwargs):
        self.broker = kwargs['broker']
        self.mode = kwargs['mode']
        self.last_data = kwargs['last_data']

    def _log(self, message):
        if self.mode == 'live':
            print(message)

    def do_action(self):
        last_data = self.last_data
        if self.mode == 'dev':
            self.current_time = last_data['current']
        else:
            self.current_time = datetime.now()
        self.current_price = last_data['Close']
        broker = self.broker
        broker.do_date = self.current_time
        #
        self.cal_support_resistance_prices(last_data)
        #
        if self.current_time.hour == 14 and self.current_time.minute >= 25:
            broker.close_all_orders()
            if broker.has_opened_deal() and self.current_time.minute >= 27:
                broker.close_all_open_deal(last_data['Close'])
            if self.mode == 'dev':
                broker.number_of_deal = 0
                broker.reset_pending_deal()

    def cal_support_resistance_prices(self, last_data):
        self.handle_worker_data('read')
        self.breakout = 0
        if not self.support and not self.resistance:
            if self.min_oc == 0 or self.min_oc > min(last_data['Open'], last_data['Close']):
                self.min_oc = min(last_data['Open'], last_data['Close'])
                self.changed = True
            if self.max_oc == 0 or self.max_oc < max(last_data['Open'], last_data['Close']):
                self.max_oc = max(last_data['Open'], last_data['Close'])
                self.changed = True
            if self.max_oc - self.min_oc > MIN_SR_RANGE:
                self.breakout = 1
                if last_data['Open'] > last_data['Close']:
                    # Black/Red => keep R and change support
                    self.resistance = self.max_oc
                    self.support = self.resistance - MIN_SR_RANGE
                else:
                    # White/Green => keep S and change R
                    self.support = self.min_oc
                    self.resistance = self.support + MIN_SR_RANGE
                self.changed = True

    def handle_worker_data(self, action='read'):
        current_time = self.current_time
        if 100 * current_time.hour + current_time.minute < 906:
            self.worker_data.reset()
        if action == 'read':
            data = self.worker_data.read()
            self.stoploss = data.stoploss
            self.take_profit = data.take_profit
            self.force_stoploss = data.force_stoploss
        elif action == 'update':
            self.worker_data.update(stoploss=self.stoploss, take_profit=self.take_profit,
                                    force_stoploss=self.force_stoploss)

    def set_worker_data(self, data):
        self.worker_data = data

    def make_decision(self, opening_deal=False):
        decision = DECISION_NONE
        if not opening_deal:
            if self.signal == BUY_SIGNAL and self.position == GOOD_POSITION:
                decision = DECISION_LONG
            elif self.signal == SELL_SIGNAL and self.position == GOOD_POSITION:
                decision = DECISION_SHORT
        else:
            decision = DECISION_HOLD
            if self.signal == CLOSE_SELL_SIGNAL:
                decision = DECISION_CLOSE_SHORT
            elif self.signal == CLOSE_BUY_SIGNAL:
                decision = DECISION_CLOSE_LONG
        self.decision = decision
        return self.decision

    def _validated_time(self):
        current_time = self.current_time
        if 100 * current_time.hour + current_time.minute < 900 or 100 * current_time.hour + current_time.minute > 1431:
            return False
        return True

    def get_reports(self):
        return {'signal': self.signal, 'decision': self.decision,
                'expected_price': self.expected_price, 'stoploss': self.stoploss, 'take_profit': self.take_profit,
                'force_stoploss': self.force_stoploss, 'version': self.algo_version}


class WorkerData:
    def __init__(self, mode='dev'):
        self.mode = mode
        self.stoploss = 0
        self.take_profit = 0
        self.force_stoploss = 0

    def read(self):
        if self.mode == 'live':
            current_dir = Path(__file__).parent
            file = str(current_dir) + '/' + WORKER_FILE
            with open(file, 'rb') as fp:
                return pickle.load(fp)
        return self

    def reset(self):
        self.stoploss = 0
        self.take_profit = 0
        self.force_stoploss = 0
        if self.mode == 'live':
            current_dir = Path(__file__).parent
            file = str(current_dir) + '/' + WORKER_FILE
            with open(file, 'wb') as fp:
                pickle.dump(self, fp)

    def update(self, **kwargs):
        if 'stoploss' not in kwargs or 'take_profit' not in kwargs or 'force_stoploss' not in kwargs:
            print('Some required worker data attributes are missing.')
            exit()
        self.stoploss = kwargs['stoploss']
        self.take_profit = kwargs['take_profit']
        self.force_stoploss = kwargs['force_stoploss']
        if self.mode == 'live':
            current_dir = Path(__file__).parent
            file = str(current_dir) + '/' + WORKER_FILE
            with open(file, 'wb') as fp:
                pickle.dump(self, fp)
