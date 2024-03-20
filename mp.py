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

# Corrected TPO (Market Profile) Calculation
def calculate_market_profile(df):
    price_min = df['price'].min()
    price_max = df['price'].max()
    price_step = 50  # Adjust this as necessary to get a readable number of bins

    # Creating price bins
    bins = np.arange(price_min, price_max, price_step)
    labels = np.arange(len(bins)-1)  # Corrected to have one fewer label than bins

    # Binning data
    df['price_bin'] = pd.cut(df['price'], bins=bins, labels=labels, include_lowest=True)

    # Count occurrences for TPO with observed parameter set explicitly
    tpo_count = df.groupby('price_bin', observed=True)['price'].agg('count')

    return tpo_count, bins



# Plotting the TPO chart
def plot_tpo_chart(tpo_count, bins):
    # You may increase the figure size here for better readability
    plt.figure(figsize=(12, 10))  # Adjust the size as needed
    plt.barh(tpo_count.index.astype(int), tpo_count.values, color='blue', edgecolor='black')

    # Only label every nth bin to prevent overcrowding (n can be adjusted as needed)
    n = 5  # Adjust this as necessary to reduce label density
    plt.yticks(ticks=np.arange(len(bins))[::n], labels=[f"{bins[i]:.2f}" for i in range(0, len(bins), n)])
    plt.xlabel('TPO Count')
    plt.ylabel('Price Bin')
    plt.title('BTC Market Profile (TPO Chart)')
    plt.tight_layout()
    plt.show()
# Main flow
btc_data = fetch_btc_data_from_coingecko()
tpo_count, bins = calculate_market_profile(btc_data)
plot_tpo_chart(tpo_count, bins)
