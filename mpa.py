import yfinance as yf
import pandas as pd
import numpy as np
from collections import defaultdict

def fetch_btc_data(days=6, interval='30m'):
    end_date = pd.Timestamp.now().normalize()
    start_date = end_date - pd.Timedelta(days=days)
    btc_data = yf.download('BTC-USD', start=start_date, end=end_date, interval=interval)
    return btc_data

def generate_tpo_profiles(data, tick_size=10, filename='tpo_profiles.txt'):
    profiles = defaultdict(lambda: defaultdict(str))
    days_data = []

    for i in range(1, 6):
        day_data = data[data.index.normalize() == data.index[0].normalize() + pd.Timedelta(days=i)]
        if day_data.empty:
            continue
        days_data.append(day_data)

    min_price = min(day_data['Low'].min() for day_data in days_data)
    max_price = max(day_data['High'].max() for day_data in days_data)
    price_range = np.arange(min_price, max_price, tick_size)
    
    # Generate TPO counts for each day
    for day_data in days_data:
        tpo_count = defaultdict(str)
        first_entry_flag = True  # Flag to mark the first entry of the day

        for index, row in day_data.iterrows():
            start_block = int((row['Low'] - min_price) // tick_size)
            end_block = int((row['High'] - min_price) // tick_size)
            for block in range(start_block, end_block + 1):
                if first_entry_flag:
                    tpo_count[price_range[block]] += 'O'
                    first_entry_flag = False
                else:
                    tpo_count[price_range[block]] += 'X'

        for price in price_range:
            profiles[price][day_data.index[0].date()] = tpo_count[price].ljust(len(day_data), '.')

    # Write combined TPO chart for all days to a file
    with open(filename, 'w') as f:
        for price in reversed(price_range):
            f.write(f"{int(price)}:")
            for day in sorted(profiles[price].keys()):
                # Add padding or vertical line separator
                f.write(profiles[price][day] + ' | ')
            f.write('\n')  # Newline for next price level


days = 4
tick_size = 100
btc_data = fetch_btc_data(days)
generate_tpo_profiles(btc_data, tick_size)
