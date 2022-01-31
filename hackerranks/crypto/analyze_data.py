
import pandas as pd
from datetime import date

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
INT_TO_DOW = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}


def determine_best_day_of_week_from_data_start(filename):
    data = pd.read_csv(filename)
    data = data.reset_index()

    week_start = MON
    week_low = (MON, -1)
    week_count = 0
    lowest_day_counter = {MON: 0, TUE: 0, WED: 0, THU: 0, FRI: 0, SAT: 0, SUN: 0}
    # Expected columns: ['unix', 'low', 'high', 'open', 'close', 'volume', 'date', 'vol_fiat']
    for idx, row in data.iterrows():
        cur_date = date.fromisoformat(row['date'])
        if idx == 0:  # First record determines the start of week
            week_start = cur_date.weekday()
            week_low = (week_start, row['low'])
        elif week_start == cur_date.weekday():
            lowest_day_counter[week_low[0]] += 1
            week_low = (week_start, row['low'])
            week_count += 1

        if row['low'] < week_low[1]:
            week_low = (cur_date.weekday(), row['low'])

    # Purposefully no final wrap-up logic -> Just ignore last partial week
    pretty_print_dow_results(lowest_day_counter)


def determine_best_day_of_week_rotating_start(filename):
    data = pd.read_csv(filename)
    data = data.reset_index()

    week_start = MON
    week_low = (MON, -1)
    week_count = 0
    lowest_day_counter = {MON: 0, TUE: 0, WED: 0, THU: 0, FRI: 0, SAT: 0, SUN: 0}
    # Expected columns: ['unix', 'low', 'high', 'open', 'close', 'volume', 'date', 'vol_fiat']
    for key in lowest_day_counter:
        week_start = key
        skip = True
        print(f'### Beginning Analysis with Start of Week = {INT_TO_DOW[key]}')
        for idx, row in data.iterrows():
            cur_date = date.fromisoformat(row['date'])
            if (cur_date.weekday() != week_start) and skip:
                pass
            elif (cur_date.weekday() == week_start) and skip:
                skip = False
                week_start = cur_date.weekday()
                week_low = (week_start, row['low'])
            elif (cur_date.weekday() == week_start) and (not skip):
                lowest_day_counter[week_low[0]] += 1
                week_low = (week_start, row['low'])
                week_count += 1
            else:
                if row['low'] < week_low[1]:
                    week_low = (cur_date.weekday(), row['low'])

        # Purposefully no final wrap-up logic -> Just ignore last partial week
        pretty_print_dow_results(lowest_day_counter)
        # Reset counters for next iteration
        lowest_day_counter = {MON: 0, TUE: 0, WED: 0, THU: 0, FRI: 0, SAT: 0, SUN: 0}


def pretty_print_dow_results(dow_counter_dict):
    best_day = ('MON', 0)
    for key in dow_counter_dict:
        if dow_counter_dict[key] > best_day[1]:
            best_day = (INT_TO_DOW[key], dow_counter_dict[key])
        print(f'{INT_TO_DOW[key]} = {dow_counter_dict[key]}')
    print(f'Best DOW to Buy Crypto: {best_day[0]}')


if __name__ == "__main__":
    # determine_best_day_of_week_from_data_start('CoinbaseData_BTC-USD_20220727-20220131_DAILY.csv')
    determine_best_day_of_week_rotating_start('CoinbaseData_BTC-USD_20220727-20220131_DAILY.csv')
