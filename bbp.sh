#!/bin/bash

# This bash file sends bulletin to local printer - set for windows currently 
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

# Print the PDF Bulletin*.pdf
# python print.py
#!/bin/bash

# The path to the file you want to print
FILE_PATH="/Users/work/Desktop/bulletinbot/Bulletin.pdf"

# Check if the file exists
if [ -f "$FILE_PATH" ]; then
    # Print the file
    lpr "$FILE_PATH"
    echo "Sent to printer: $FILE_PATH"
    # File does not exist
    echo "Error: File does not exist at $FILE_PATH"
fi


