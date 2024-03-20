import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
import requests

# Function to fetch historical BTC data from CoinGecko for the last 5 days
def fetch_btc_data_from_coingecko():
    end_date = datetime.now(timezone.utc)  # Adjusted for timezone awareness
    start_date = end_date - timedelta(days=5)

    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={end_date.timestamp()}"
    response = requests.get(url)
    data = response.json()

    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('datetime')
    df.drop(columns=['timestamp'], inplace=True)
    return df

# TPO (Market Profile) Calculation
def calculate_market_profile(df):
    # Define the price step for TPO calculation
    price_step = 50  # Adjust this as necessary to get a readable number of bins
    
    tpo_list = []
    
    # We separate the data by day and perform TPO calculation for each day
    for day in pd.date_range(start=df.index.min(), end=df.index.max(), freq='D'):
        daily_data = df[df.index.date == day.date()]
        if not daily_data.empty:
            price_min = daily_data['price'].min()
            price_max = daily_data['price'].max()
            bins = np.arange(price_min, price_max, price_step)
            labels = np.arange(len(bins)-1)
            
            daily_data['price_bin'] = pd.cut(daily_data['price'], bins=bins, labels=labels, include_lowest=True)
            
            # TPO count for each bin for the day
            tpo_count = daily_data.groupby('price_bin')['price'].agg('count')
            tpo_list.append(tpo_count)
    
    # Combine TPO counts from each day into a single DataFrame
    combined_tpo = pd.concat(tpo_list, axis=1)
    combined_tpo.columns = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D').date
    
    return combined_tpo.fillna(0).astype(int), bins

# Plotting the TPO chart
def plot_tpo_chart(tpo_data, bins):
    fig, ax = plt.subplots(figsize=(16, 12))  # Increased figure size for better readability
    
    # Set the width of the bars and the space between them
    bar_width = 0.1
    space_between_bars = 0.05
    
    # Create a TPO chart with one column per day
    for i, column in enumerate(tpo_data.columns):
        tpo_counts_for_day = tpo_data[column]
        ax.barh(tpo_counts_for_day.index.astype(int), tpo_counts_for_day.values, height=bar_width, left=i*(bar_width+space_between_bars), color='blue', edgecolor='black')
    
    # Set the y-ticks to only display every nth label to reduce density
    n = 10  # Adjust as needed
    ax.set_yticks(np.arange(len(bins))[::n])
    ax.set_yticklabels([f"{bins[i]:.2f}" for i in range(0, len(bins), n)], fontsize=8)  # Reduced font size
    
    # Set the x-ticks to label each day
    ax.set_xticks(np.arange(len(tpo_data.columns)))
    ax.set_xticklabels(tpo_data.columns, rotation=90, fontsize=8)  # Reduced font size
    
    ax.set_xlabel('Days')
    ax.set_ylabel('Price Bin')
    ax.set_title('BTC Market Profile (TPO Chart)')
    plt.tight_layout()
    plt.show()

# Main flow
btc_data = fetch_btc_data_from_coingecko()
tpo_data, bins = calculate_market_profile(btc_data)
plot_tpo_chart(tpo_data, bins)
