from worker import *


class Exporter(Worker):
    def __init__(self):
        super().__init__()
        self.reason = ''

    def do_action(self):
        super().do_action()
        if not self._validated_time():
            return
        self.handle_json_data('read')

        broker = self.broker
        """ Handle opening deal"""
        self.handle_opening_deal(broker)
        if self.changed:
            self.handle_json_data('update')

    def handle_opening_deal(self, broker):
        today_data = self.today_data
        last_data = today_data.iloc[-1]
        current_price = last_data['Close']
        if self.mode == 'dev':
            if not self.force_stoploss or not self.take_profit:
                raise Exception("Sorry, The stop loss & take profit price must to be set!")
            self.signal = self._handle_force_stoploss(broker, last_data, self.force_stoploss)
            self.signal = self._handle_take_profit(broker, last_data, self.take_profit)

        if broker.has_opened_deal:
            self.update_stoploss(last_data)
            """ Still has deal. No force stoploss or take profit. """
            entry_data = today_data[(today_data.index > broker.entry_time)]
            min_price = entry_data['Low'].min()
            max_price = entry_data['High'].max()
            if broker.is_long_open:
                if last_data['Low'] < self.stoploss:
                    self.signal = CLOSE_BUY_SIGNAL
                # if self.signal == NO_SIGNAL:
                    # if last_data['prev_Close'] - last_data['prev_Open'] > 2.5 and \
                    #         last_data['Open'] > last_data['Close']:
                    #     self.signal = CLOSE_BUY_SIGNAL
                    #     self.reason = 'close - open > 2.5'
                if self.signal == NO_SIGNAL and current_price < max_price - 4:
                    self.signal = CLOSE_BUY_SIGNAL
                    self.reason = 'current_price < max_price - 4'
                if self.signal == NO_SIGNAL:
                    body = abs(last_data['Close'] - last_data['Open'])
                    upper_shadow = last_data['High'] - max(last_data['Close'], last_data['Open'])
                    is_long_upper_shadow = True if upper_shadow > 2 else False
                    if body > 0.3 and is_long_upper_shadow and upper_shadow > 3 * body:
                        self.signal = CLOSE_BUY_SIGNAL
                        self.reason = 'long upper shadow'
            elif broker.is_short_open:
                if last_data['High'] > self.stoploss:
                    self.signal = CLOSE_SELL_SIGNAL
                # if self.signal == NO_SIGNAL:
                #     if last_data['prev_Open'] - last_data['prev_Close'] > 2.5 and \
                #             last_data['Open'] < last_data['Close']:
                #         self.signal = CLOSE_SELL_SIGNAL
                if self.signal == NO_SIGNAL and current_price > min_price + 4:
                    self.signal = CLOSE_BUY_SIGNAL
                    self.reason = 'current_price > min_price + 4'
                if self.signal == NO_SIGNAL:
                    body = abs(last_data['Close'] - last_data['Open'])
                    lower_shadow = min(last_data['Close'], last_data['Open']) - last_data['Low']
                    is_long_lower_shadow = True if lower_shadow > 2 else False
                    if body > 0.3 and is_long_lower_shadow and lower_shadow > 3 * body:
                        self.signal = CLOSE_SELL_SIGNAL
                        self.reason = 'long lower shadow'

            self.make_decision(True)
            if self.decision == DECISION_CLOSE_SHORT or self.decision == DECISION_CLOSE_LONG:
                broker.close_all_open_deal(last_data['Close'])

    def update_stoploss(self, last_data):
        broker = self.broker
        if broker.is_long_open:
            if last_data['Close'] > last_data['Open'] and last_data['Close'] - last_data['Open'] > 2.1:
                self.stoploss = last_data['Open'] - 0.1
                self.changed = True
        else:
            if last_data['Close'] < last_data['Open'] and last_data['Open'] - last_data['Close'] > 2.1:
                self.stoploss = last_data['Close'] + 0.1
                self.changed = True

    @classmethod
    def _handle_force_stoploss(cls, broker, signal_data, stoploss):
        signal = NO_SIGNAL
        if broker.is_long_open:
            low_price = signal_data['Low']
            if low_price < stoploss:
                broker.close_all_open_deal(stoploss)
                signal = CLOSE_BUY_SIGNAL
        elif broker.is_short_open:
            high_price = signal_data['High']
            if high_price > stoploss:
                broker.close_all_open_deal(stoploss)
                signal = CLOSE_SELL_SIGNAL
        return signal

    def _handle_take_profit(self, broker, signal_data, take_profit):
        signal = NO_SIGNAL
        if broker.is_short_open:
            low_price = signal_data['Low']
            if low_price < take_profit:
                broker.close_all_open_deal(take_profit)
                signal = CLOSE_SELL_SIGNAL
                self.reason = 'stoploss'
        elif broker.is_long_open:
            high_price = signal_data['High']
            if high_price > take_profit:
                broker.close_all_open_deal(take_profit)
                signal = CLOSE_BUY_SIGNAL
                self.reason = 'stoploss'
        return signal

    def show_reports(self):
        signal_text = self.signal
        if self.signal == NO_SIGNAL:
            signal_text = "None"

        if self.decision == DECISION_HOLD:
            log_msg = f"Signal: {signal_text}, Decision: {self.decision}, price: {self.current_price}," \
                      f"entry_price: {self.broker.entry_price}, SL: {self.stoploss}, Force-SL: {self.force_stoploss}, " \
                      f"TP: {self.take_profit}, Support: {self.support}, Resistance: {self.resistance}"
        else:
            log_msg = f"Signal: {signal_text}, Decision: {self.decision}, price: {self.current_price}," \
                      f"entry_price: {self.broker.entry_price}, exit_price: {self.broker.exit_price}, " \
                      f"profit: {self.broker.profit}, reason: '{self.reason}', " \
                      f"SL: {self.stoploss}, Force-SL: {self.force_stoploss}, " \
                      f"TP: {self.take_profit}, Support: {self.support}, Resistance: {self.resistance}"
        print(log_msg)
