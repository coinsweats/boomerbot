#!/bin/bash

# Delete previous Bulletin
rm -f Bulletin*.pdf

# Run your Python scripts in order
python 4chart.py
python top100img.py
python tpo.py
python tpoimg.py

sleep 10

# Generate your PDF 
python pdf.py

# Remove PNG and text files
rm *.png
rm *.txt
