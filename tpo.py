#
# This generates a TPO chart in ascii format
# TODO improve font, create letters or blocks rather than X, IB, POC, format opening TPO better, dynamic tick size, nicer x axis
#
import yfinance as yf
import pandas as pd
import numpy as np
from collections import defaultdict

def fetch_btc_data(days=6, interval='30m'):
    end_date = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)  # Include the current day
    start_date = end_date - pd.Timedelta(days=days)
    btc_data = yf.download('BTC-USD', start=start_date, end=end_date, interval=interval)
    return btc_data

def generate_tpo_profiles(data, days, tick_size=10, max_width=10, filename='tpo_profiles.txt'):
    profiles = defaultdict(lambda: defaultdict(str))
    days_data = []
    numerical_info = defaultdict(dict)  # To store open, close, POC for each day
    
    end_date = data.index.max().normalize()
    start_date = end_date - pd.Timedelta(days=days)

    for single_date in pd.date_range(start=start_date, end=end_date, freq='D'):
        day_data = data[data.index.normalize() == single_date]
        if day_data.empty:
            continue
        days_data.append(day_data)

    min_price = min(day_data['Low'].min() for day_data in days_data)
    max_price = max(day_data['High'].max() for day_data in days_data)
    price_range = np.arange(min_price, max_price, tick_size)

    # Generate TPO counts and determine POC for each day
    for day_data in days_data:
        tpo_count = defaultdict(str)
        first_entry_flag = True
        day_date = day_data.index[0].date()

        numerical_info[day_date]['open'] = day_data.iloc[0]['Open']
        numerical_info[day_date]['close'] = day_data.iloc[-1]['Close']

        for index, row in day_data.iterrows():
            start_block = int((row['Low'] - min_price) // tick_size)
            end_block = int((row['High'] - min_price) // tick_size)
            for block in range(start_block, end_block + 1):
                if first_entry_flag:
                    tpo_count[price_range[block]] += 'O'
                    first_entry_flag = False
                else:
                    tpo_count[price_range[block]] += 'X'
                if len(tpo_count[price_range[block]]) > max_width:
                    break

        poc_price = max(tpo_count, key=lambda k: len(tpo_count[k]))
        numerical_info[day_date]['poc'] = poc_price

        for price in price_range:
            profile_line = tpo_count[price].ljust(max_width, '.')
            if price == poc_price:
                profile_line = profile_line.replace('X', 'P', 1)
            profiles[price][day_date] = profile_line

    # Calculate the width of the price column (including the colon and space padding)
    price_col_width = max(len(str(int(price))) for price in price_range) + 2  # `2` for ': ' after price
    
    separator_line = '-' * (price_col_width + (max_width + 3) * len(days_data))
    
    with open(filename, 'w') as f:
        # Write headers
        headers = ['$'.ljust(price_col_width)] + [day_date.strftime('%d-%m-%Y').center(max_width) for day_date in sorted(numerical_info.keys())]
        f.write('  '.join(headers) + '\n')
        
        # Write separator
        f.write(separator_line + '\n')

        # Write TPO profiles
        for price in reversed(price_range):
            f.write(f"{int(price)}:".ljust(price_col_width))  # Use the calculated price column width
            for day_date in sorted(numerical_info.keys()):
                f.write(profiles[price][day_date] + ' | ')
            f.write('\n')

        # Write bottom separator
        f.write(separator_line + '\n')

        # Write numerical information header
        f.write(' ' * (price_col_width - 4))  # Adjust the space to align with the Price column
        f.write('Info'.center(max_width * len(days_data) + len(days_data) * 3))
        f.write('\n')

        # Write another separator after the 'Info' header
        f.write(separator_line + '\n')

        # Formatting the numerical info for each day under the headers
        for key in ['open', 'close', 'poc']:
            f.write(f"{key.title()}:".ljust(price_col_width))  # e.g., Open:, Close:, POC:
            for day_date in sorted(numerical_info.keys()):
                value = numerical_info[day_date][key]
                if key == 'poc':  # Assuming POC should be highlighted or formatted differently
                    info_string = f"{value:.2f}"
                else:
                    info_string = f"{value:.2f}"
                f.write(info_string.center(max_width) + ' | ')
            f.write('\n')

# Usage
days = 5
tick_size = 100
max_width = 28  # Set the maximum width for the daily TPO sections
btc_data = fetch_btc_data(days)
generate_tpo_profiles(btc_data, days, tick_size, max_width)
