
def cal_return(data):
    data['min_price'] = ''
    data['max_price'] = ''
    data['return'] = ''
    data['exit_time'] = ''
    data['entry_price'] = ''
    data['exit_price'] = ''
    # Stop loss at x0 pips
    sl_step = 4
    # Take profit at y0 pips(R/R = 1/3)
    tp_step = 9
    for i, row in data.iterrows():
        if 100*row.name.hour + row.name.minute < 1425:
            if row['cross'] != '':
                momentum = 0
                current_date = row.name.strftime('%Y-%m-%d ').format()
                current_time = row.name
                entry_price = row['Close']
                data_to_end_day = data[(data.index > current_time) & (data.index < current_date + ' 14:30:00')]
                max_price = row['Close']
                min_price = row['Close']
                exit_time = ''
                exit_price = 0
                for k, wrow in data_to_end_day.iterrows():
                    if wrow['Low'] < min_price:
                        min_price = wrow['Low']
                    if wrow['High'] > max_price:
                        max_price = wrow['High']
                    if max_price > entry_price:
                        if wrow['Close'] < max_price - sl_step or wrow['Close'] > entry_price + tp_step:
                            # Trailing stoploss 1
                            # Take profit
                            momentum = wrow['Close'] - entry_price
                            exit_time = wrow.name
                            exit_price = wrow['Close']
                            break
                    if min_price < entry_price:
                        if wrow['Close'] > min_price + sl_step or wrow['Close'] < entry_price - tp_step:
                            # Trailing stoploss 2
                            # Take profit
                            momentum = wrow['Close'] - entry_price
                            exit_time = wrow.name
                            exit_price = wrow['Close']
                            break
                    if 100*row.name.hour + row.name.minute == 1425:
                        # Close at 02:25PM
                        momentum = wrow['Close'] - entry_price
                        exit_time = wrow.name
                        exit_price = wrow['Close']
                        break
                data.at[i, 'return'] = momentum
                data.at[i, 'entry_price'] = entry_price
                data.at[i, 'exit_price'] = exit_price
                data.at[i, 'exit_time'] = exit_time
                data.at[i, 'min_price'] = min_price
                data.at[i, 'max_price'] = max_price
    return data
