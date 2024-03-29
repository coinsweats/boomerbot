#
# This creates an image from the tpo.py TPO text file
#
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Load the text file
with open('tpo_profiles.txt', 'r') as f:
    lines = f.readlines()

# Strip the right whitespace and find the maximum width of the text
lines = [line.rstrip() for line in lines]  # Remove any trailing whitespace from each line
max_width = max(len(line) for line in lines)  # Updated to calculate width based on trimmed lines

# Assume each character is about 10 pixels wide and 20 pixels tall, adjust as needed
char_width = 13
char_height = 20

# Create an image with enough width to hold the longest line and height for all lines
image_width = max_width * char_width  # Updated width calculation based on trimmed lines
image_height = len(lines) * char_height
image = Image.new('RGB', (image_width, image_height), color='white')

# Use a monospaced font
font = ImageFont.truetype('CourierNewBold.ttf', 20)

# Initialize the drawing context
draw = ImageDraw.Draw(image)

# Starting position for the first line
x, y = 0, 0

# Draw each line of text
for line in lines:
    draw.text((x, y), line, font=font, fill='black')  # Removed .strip('\n') since we already stripped the lines
    y += char_height  # Move down to draw the next line

# No need to create a larger image with a border, just save the image
output_path = 'tpo_image.png'
image.save(output_path)

output_path



