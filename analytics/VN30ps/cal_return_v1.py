
def cal_return(data):
    data['return'] = ''
    data['exit_time'] = ''
    # Stop loss at x0 pips
    sl_step = 3
    # Take profit at y0 pips(R/R = 1/3)
    tp_step = 9
    for i, row in data.iterrows():
        if 915 < 100*row.name.hour + row.name.minute < 1420:
            if row['signal'] == 'long':
                # Long signal
                current_date = row.name.strftime('%Y-%m-%d ').format()
                current_time = row.name
                entry_price = row['Close']
                data_to_end_day = data[(data.index > current_time) & (data.index < current_date + ' 14:30:00')]
                max_price = 0
                exit_time = ''
                for k, wrow in data_to_end_day.iterrows():
                    if wrow['Low'] < entry_price and wrow['Low'] < entry_price - sl_step:
                        # Stop loss
                        momentum = -sl_step
                        exit_time = wrow.name
                        break
                    else:
                        if wrow['High'] > entry_price + tp_step:
                            # Take profit
                            momentum = tp_step
                            exit_time = wrow.name
                            break
                        else:
                            # Close at 02:25PM
                            momentum = wrow['Close'] - entry_price
                            exit_time = wrow.name
                data.at[i, 'return'] = momentum
                data.at[i, 'exit_time'] = exit_time
            elif row['signal'] == 'short':
                # Short signal
                current_date = row.name.strftime('%Y-%m-%d ').format()
                current_time = row.name
                entry_price = row['Close']
                data_to_end_day = data[(data.index > current_time) & (data.index < current_date + ' 14:30:00')]
                min_price = 10000
                exit_time = ''
                for k, wrow in data_to_end_day.iterrows():
                    if wrow['High'] > entry_price and wrow['High'] > entry_price + sl_step:
                        # Stop loss
                        momentum = -sl_step
                        exit_time = wrow.name
                        break
                    else:
                        if wrow['Low'] < entry_price - tp_step:
                            # Take profit
                            momentum = tp_step
                            exit_time = wrow.name
                            break
                        else:
                            # Close at 02:25PM
                            momentum = entry_price - wrow['Close']
                            exit_time = wrow.name
                data.at[i, 'return'] = momentum
                data.at[i, 'exit_time'] = exit_time
    return data
