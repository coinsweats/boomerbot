#
# This creates two tables top top gainers / losers from coingecko
# TODO - format table better, nice lines, better text formatting, borders
#
from PIL import Image, ImageDraw, ImageFont
import requests
import pandas as pd

# Replace 'arial.ttf' with the full path to your font file on your system
FONT_PATH = 'arial.ttf'
FONT_SIZE = 14
LINE_COLOR = "#C0C0C0"  # A light shade of gray for monochrome appearance
TEXT_COLOR = "black"    # Set all text to black
BACKGROUND_COLOR = "white"

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
    # Define column positions and widths
    column_details = {
        "Token": {"x_offset": 10, "width": 180},
        "Symbol": {"x_offset": 200, "width": 80},
        "Price Change %": {"x_offset": 290, "width": 110}
    }

    # Load fonts
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Calculate image height dynamically based on the number of data rows
    row_height = FONT_SIZE + 10
    image_height = 60 + (len(data_frame) + 1) * row_height

    # Create an image with white background
    image = Image.new('RGB', (600, image_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # Draw the title at the top
    title_font = ImageFont.truetype(FONT_PATH, FONT_SIZE + 4)
    draw.text((10, 10), title, fill=TEXT_COLOR, font=title_font)

    # Draw header background
    header_height = 30
    header_y_start = 50
    header_y_end = header_y_start + header_height
    draw.rectangle(
        [(column_details["Token"]["x_offset"], header_y_start),
         (column_details["Price Change %"]["x_offset"] + column_details["Price Change %"]["width"], header_y_end)],
        fill=LINE_COLOR
    )

    # Draw the header text for each column
    for column, details in column_details.items():
        draw.text(
            (details["x_offset"], header_y_start + (header_height - FONT_SIZE) // 2),
            column,
            fill=TEXT_COLOR,
            font=font
        )

    # Draw each row of data
    y_offset = header_y_end + 5
    for index, row in data_frame.iterrows():
        token_name = ' '.join(word.capitalize() for word in row['id'].replace('-', ' ').split())
        symbol_text = row['symbol'].upper()
        price_change_text = f"{row[percentage_change_key]:.2f}%"
        
        draw.text((column_details["Token"]["x_offset"], y_offset), token_name, fill=TEXT_COLOR, font=font)
        draw.text((column_details["Symbol"]["x_offset"], y_offset), symbol_text, fill=TEXT_COLOR, font=font)
        draw.text(
            (column_details["Price Change %"]["x_offset"], y_offset),
            price_change_text,
            fill=TEXT_COLOR,  # Set text color to black
            font=font
        )
        y_offset += row_height

    # Save the image
    image.save(file_name)

def main():
    crypto_df = fetch_top_100_cryptos()
    gainers, losers = find_gainers_losers(crypto_df, "24h")
    if gainers is not None and losers is not None:
        draw_enhanced_crypto_data("Top 10 Gainers - Last 24h", gainers, "top_gainers.png", "price_change_percentage_24h")
        draw_enhanced_crypto_data("Top 10 Losers - Last 24h", losers, "top_losers.png", "price_change_percentage_24h")
    else:
        print("Skipping analysis for 24h due to missing data.\n")

# Run the script
if __name__ == "__main__":
    main()

