from PIL import Image, ImageDraw, ImageFont
import requests
import pandas as pd

def fetch_top_100_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data)

def find_gainers_losers(df, period="24h"):
    percentage_change_key = f"price_change_percentage_{period}"
    if percentage_change_key not in df.columns:
        print(f"Data for {period} is not available.")
        return None, None
    sorted_df = df.sort_values(by=percentage_change_key, ascending=False)
    top_gainers = sorted_df.head(10)[["id", "symbol", percentage_change_key]]
    top_losers = sorted_df.tail(10)[["id", "symbol", percentage_change_key]]
    return top_gainers, top_losers

def draw_enhanced_crypto_data(title, data_frame, file_name, percentage_change_key):
    # ...
    # Now, use `percentage_change_key` in the function body
    # ...

    # Create a new image with white background
    width, height = 800, 400  # Adjust the height if necessary
    background_color = 'white'
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Use the default font instead of truetype
    title_font = ImageFont.load_default()
    font = ImageFont.load_default()

    # Define colors
    text_color = "black"
    gain_color = "#008000"  # Green color for gains
    loss_color = "#FF0000"  # Red color for losses
    grid_color = "#DDDDDD"  # Light grey for grid lines

    # Draw title
    title_x, title_y = 30, 20
    draw.text((title_x, title_y), title, fill=text_color, font=title_font)

    # Starting position for the data
    y_offset = title_y + 20

    # Define column starting positions
    x_offset_id = title_x
    x_offset_symbol = x_offset_id + 100
    x_offset_change = x_offset_symbol + 100

    # Draw header
    draw.text((x_offset_id, y_offset), "ID", font=font, fill=text_color)
    draw.text((x_offset_symbol, y_offset), "Symbol", font=font, fill=text_color)
    draw.text((x_offset_change, y_offset), "Price Change %", font=font, fill=text_color)

    y_offset += 20

    # Draw data
    for index, row in data_frame.iterrows():
        id, symbol, price_change = row['id'], row['symbol'], row[percentage_change_key]
        change_color = gain_color if price_change >= 0 else loss_color
        draw.text((x_offset_id, y_offset), id, font=font, fill=text_color)
        draw.text((x_offset_symbol, y_offset), symbol.upper(), font=font, fill=text_color)
        draw.text((x_offset_change, y_offset), f"{price_change:.2f}%", font=font, fill=change_color)
        y_offset += 20

    # Save the image
    image.save(file_name)

def main():
    crypto_df = fetch_top_100_cryptos()
    gainers, losers = find_gainers_losers(crypto_df, "24h")
    if gainers is not None and losers is not None:
        draw_enhanced_crypto_data("Top 10 Gainers - Last 24h", gainers, "top_gainers_enhanced.png", "price_change_percentage_24h")
        draw_enhanced_crypto_data("Top 10 Losers - Last 24h", losers, "top_losers_enhanced.png", "price_change_percentage_24h")
    else:
        print("Skipping analysis for 24h due to missing data.\n")


if __name__ == "__main__":
    main()

