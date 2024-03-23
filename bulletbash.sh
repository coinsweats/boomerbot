#!/bin/bash

# Run your Python scripts in order
python 4chart.py
python top100img.py
python mpa.py
python ipo.py

sleep 10

# Generate your PDF (assuming one of the scripts does this)
python pdf.py

# Remove PNG and text files
rm *.png
rm *.txt

# Print the PDF (Update with your PDF's filename)
#lp Image_Collection.pdf

