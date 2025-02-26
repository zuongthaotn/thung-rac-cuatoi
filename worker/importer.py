from worker import *
from func import get_pivot_value_for_fibo


class Importer(Worker):
    def __init__(self):
        super().__init__()

    def do_action(self):
        super().do_action()

        if not self._validated_time():
            return

        """ Finding new chance to open deal"""
        self.find_new_chance()
        if self.changed:
            self.handle_worker_data('update')

    def find_new_chance(self):
        last_data = self.last_data
        self.signal = self._calculate_open_deal_signal(last_data)
        if self.signal != NO_SIGNAL:
            self._check_position()
            self.make_decision()
            if self.decision != DECISION_NONE:
                """ Calculating stoploss & take profit"""
                self.cal_ep_sl_tp(last_data)
                self.broker.set_stoploss(self.stoploss)
                self.broker.set_force_stoploss(self.force_stoploss)
                self.broker.set_take_profit(self.take_profit)
                if self.decision == DECISION_LONG:
                    self.broker.open_long_deal(self.expected_price, order_type="MTL")
                elif self.decision == DECISION_SHORT:
                    self.broker.open_short_deal(self.expected_price, order_type="MTL")
                if self.mode == 'live':
                    self.broker.pull_deal_data()
                    self.broker.set_risk_reward()
                self.changed = True

    def _check_position(self):
        self.position = BAD_POSITION

    def _calculate_open_deal_signal(self, signal_data):
        signal = NO_SIGNAL
        if 100 * signal_data.name.hour + signal_data.name.minute == 900:
            return self._calculate_open_deal_signal_9h(signal_data)
        elif signal_data['cross_fibo'] != '':
            signal = NO_SIGNAL
        self.signal = signal
        return self.signal

    def _calculate_open_deal_signal_9h(self, signal_data):
        signal = NO_SIGNAL
        if signal_data['Close'] < signal_data['fibo_0']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 0)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 0, 'risk_reward')
            if fibo_up_mean_return > 2.9 and fibo_up_risk_reward > 2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_0'] < signal_data['Close'] < signal_data['fibo_236']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 236)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 236, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 0)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 0, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_236'] < signal_data['Close'] < signal_data['fibo_382']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 382)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 382, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 236)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 236, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_382'] < signal_data['Close'] < signal_data['fibo_5']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 5)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 5, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 382)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 382, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_5'] < signal_data['Close'] < signal_data['fibo_618']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 618)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 618, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 5)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 5, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_618'] < signal_data['Close'] < signal_data['fibo_786']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 786)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 786, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 618)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 618, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_786'] < signal_data['Close'] < signal_data['fibo_1']:
            fibo_up_mean_return = get_pivot_value_for_fibo(signal_data, 1)
            fibo_up_risk_reward = get_pivot_value_for_fibo(signal_data, 1, 'risk_reward')
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 786)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 786, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            elif fibo_down_mean_return > 2.9 and fibo_down_risk_reward > 2.9 and \
                    fibo_up_risk_reward > -2.9 and fibo_up_mean_return > -2.9:
                signal = BUY_SIGNAL
        elif signal_data['fibo_1'] < signal_data['Close']:
            fibo_down_mean_return = get_pivot_value_for_fibo(signal_data, 1)
            fibo_down_risk_reward = get_pivot_value_for_fibo(signal_data, 1, 'risk_reward')
            if fibo_down_mean_return < -2.9 and fibo_down_risk_reward < -2.9:
                signal = SELL_SIGNAL
            # other cases wait for crossing
        self.signal = signal
        return self.signal

    def cal_ep_sl_tp(self, last_data):
        expected_price = last_data['Close']
        if self.signal == BUY_SIGNAL:
            self.expected_price = expected_price
            self.force_stoploss = last_data['min_prev'] - 0.1
            risk = expected_price - last_data['min_prev']
            self.stoploss = self.force_stoploss
            self.take_profit = self.expected_price + RR * risk
        elif self.signal == SELL_SIGNAL:
            self.expected_price = expected_price
            self.force_stoploss = last_data['max_prev'] + 0.1
            self.stoploss = self.force_stoploss
            risk = last_data['max_prev'] - expected_price
            self.take_profit = self.expected_price - RR * risk

    def show_reports(self):
        signal_text = self.signal
        if self.signal == NO_SIGNAL:
            signal_text = "None"

        if self.decision == DECISION_NONE:
            log_msg = f"Signal: {signal_text}, Support: {self.support}, Resistance: {self.resistance}"
        else:
            log_msg = f"Signal: {signal_text}, Decision: {self.decision}, price: {self.current_price}," \
                      f"expected_price: {self.expected_price}, SL: {self.stoploss}, Force-SL: {self.force_stoploss}, " \
                      f"TP: {self.take_profit}, Support: {self.support}, Resistance: {self.resistance}"
        print(log_msg)

    def _validated_time(self):
        current_time = self.current_time
        if 100 * current_time.hour + current_time.minute < 900 or 100 * current_time.hour + current_time.minute > 1401:
            return False
        return True
