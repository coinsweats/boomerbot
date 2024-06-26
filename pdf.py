#
# The is the PDF builder for printing - it collates and formats images into a 2 page bulletin
#
from fpdf import FPDF
from datetime import datetime  # Import datetime module

class PDF(FPDF):
    def header(self):
        # Add a header to each page if needed
        self.set_font('Arial', 'B', 12)
        current_date = datetime.now().strftime("%m-%d-%Y")  # Format current date
        self.cell(10, 10, f'Market Bulletin - {current_date}', 0, 1, 'L')  # Title with current date in the header
    
    def footer(self):
        # Add a footer to each page if needed
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, ' ' + str(self.page_no()), 0, 0, 'R')  # Page number in the footer

# Helper function to calculate x position for centered image
def get_centered_x(image_width, page_width=210):
    # Convert millimeters to points for image width (assuming 72 dpi)
    image_width_pt = image_width / 0.352778
    # Convert millimeters to points for page width (assuming 72 dpi)
    page_width_pt = page_width / 0.352778
    # Calculate x position for centered image
    x = (page_width_pt - image_width_pt) / 2
    # Convert back to millimeters
    return x * 0.352778

pdf = PDF()
pdf.set_auto_page_break(auto=False)

# First Page
pdf.add_page()

# Title for the first chart
pdf.set_font("Arial", size=10)
pdf.cell(50, 10, '90-Day Candlestick Charts', 0, 1, 'L')  # Add a title before the first chart

# Add '4chart.png' on the top half of the page
pdf.image('/home/work/boomerbot/4chart.png', x=5, y=32, w=190)

# Calculate the y position for the next images (half the page height plus a small margin)
y_position = 180  # A4 page height is 297mm

# Add 'top_gainers_enhanced.png' on the bottom left half of the page
pdf.image('/home/work/boomerbot/top_gainers.png', x=20, y=y_position, w=105)

# Add 'top_losers_enhanced.png' on the bottom right half of the page
pdf.image('/home/work/boomerbot/top_losers.png', x=115, y=y_position, w=105)

# Second Page
pdf.add_page()

# Title for the content on the second page
pdf.set_font("Arial", size=10) # Set the title font
pdf.cell(0, 10, 'TPO Chart - 100 ticks', 0, 1, 'L')  # Add the title

# Get the width of the image for centering
# For this example, we assume 'tpo_image_with_border.png' has a width of 190mm
centered_x_position = get_centered_x(190)

# Add 'tpo_image_with_border.png' centered on the page
pdf.image('/home/work/boomerbot/tpo_image.png', x=centered_x_position, y=35, w=200)

# Save the PDF to a file with the current date and time appended
pdf_output = f'/home/work/boomerbot/Bulletin.pdf'
pdf.output(pdf_output)

print(f'PDF saved: {pdf_output}')


