#
# This creates an image from the tpo.py TPO text file
#
# TODO - format image a bit better

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Load the text file
with open('tpo_profiles.txt', 'r') as f:
    lines = f.readlines()

# Determine the maximum width of the text
max_width = max(len(line) for line in lines)

# Assume each character is about 10 pixels wide and 20 pixels tall, adjust as needed
char_width = 13
char_height = 20

# Create an image with enough width to hold the longest line and height for all lines
image_width = max_width * char_width
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
    draw.text((x, y), line.strip('\n'), font=font, fill='black')
    y += char_height  # Move down to draw the next line

# Border size and color
border_size = 2  # Thickness of the border
border_color = 'black'

# Calculate new image size (original size + border)
new_image_width = image.width + border_size * 4
new_image_height = image.height + border_size * 10

# Create a new image with the new size and white background
new_img = Image.new('RGB', (new_image_width, new_image_height), 'white')

# Paste the original image onto the new image, centered
new_img.paste(image, (border_size, border_size))

# Initialize the drawing context for the new image
draw = ImageDraw.Draw(new_img)

# Draw a black rectangle for the border
draw.rectangle(
    [(0, 0), (new_image_width - 1, new_image_height - 1)], 
    outline=border_color, 
    width=border_size
)

# Save the new image with the border
output_path = 'tpo_image_with_border.png'
new_img.save(output_path)

output_path


output_path
