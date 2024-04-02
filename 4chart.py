#
#  This script generates 4 90 day candlestick charts for BTCUSD / ETHUSD / ETHBTC / SPX
#  The script then collects these charts and combines into one image
#
import mplfinance as mpf
import pandas as pd
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_crypto_data(coin_id, vs_currency, days):
    cg = CoinGeckoAPI()
    historical_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)
    dates = [datetime.fromtimestamp(data_point[0]/1000, tz=timezone.utc) for data_point in historical_data['prices']]
    prices = [data_point[1] for data_point in historical_data['prices']]
    df = pd.DataFrame(data={'Price': prices}, index=pd.to_datetime(dates, utc=True))
    df['Open'] = df['High'] = df['Low'] = df['Close'] = df['Price']
    df_ohlc = df.resample('1D').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})
    df_ohlc.index = pd.DatetimeIndex(df_ohlc.index)
    return df_ohlc

def get_spx_data(days):
    spx = yf.Ticker("^GSPC")
    hist = spx.history(period=f"{days}d")
    df_ohlc = hist[['Open', 'High', 'Low', 'Close']]
    df_ohlc.index = pd.DatetimeIndex(df_ohlc.index)
    return df_ohlc

def plot_chart(df_ohlc, filename):
    mpf.plot(
        df_ohlc, 
        type='candle', 
        style='classic', 
        ylabel='', 
        savefig=dict(
            fname=filename,
            dpi=100,
            pad_inches=0.25
        )
    )

def display_charts_on_one_page(image_paths, titles, ncols=2, output_file='4chart.png'):
    nrows = (len(image_paths) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, nrows * 5))
    
    axes = axes.flatten() if nrows > 1 else [axes]
    
    for ax, image_path, title in zip(axes, image_paths, titles):
        img = mpimg.imread(image_path)
        ax.imshow(img)
        ax.annotate(title, xy=(0.5, 0.95), xycoords='axes fraction', ha='center', va='center', fontsize=10)
        ax.axis('off')
    
    for i in range(len(image_paths), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')  # This saves the figure to a file
    plt.close(fig)  # Close the figure to prevent display if running in an interactive environment


# Generate charts without embedded titles
image_files = [
    '/home/work/boomerbot/BTCUSD_90_day_candlestick.png',
    '/home/work/boomerbot/ETHUSD_90_day_candlestick.png',
    '/home/work/boomerbot/ETHBTC_90_day_candlestick.png',
    '/home/work/boomerbot/SPX_90_day_candlestick.png'
]

# Plot and save the individual charts
plot_chart(get_crypto_data('bitcoin', 'usd', 90), image_files[0])
plot_chart(get_crypto_data('ethereum', 'usd', 90), image_files[1])
plot_chart(get_crypto_data('ethereum', 'btc', 90), image_files[2])
plot_chart(get_spx_data(90), image_files[3])

# Display all charts on one page
titles = ['BTCUSD', 'ETHUSD', 'ETHBTC', 'SPX']
display_charts_on_one_page(image_files, titles)
display_charts_on_one_page(image_files, titles, output_file='/home/work/boomerbot/4chart.png')


