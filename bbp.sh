#!/bin/bash

# This sends to default printer  - ready to run as cronjob 

# Path to the work directory
WORK_DIR="/home/work/boomerbot"
LOG_FILE="${WORK_DIR}/script_log.txt" # Define a log file path

# Delete previous Bulletin PDFs
echo "Deleting previous Bulletin PDFs..." | tee -a "$LOG_FILE"
rm -f "${WORK_DIR}/Bulletin*.pdf"

# Run your Python scripts in order. Add checks to ensure each script executes successfully.
echo "Running Python scripts to generate required files..." | tee -a "$LOG_FILE"
python3 "${WORK_DIR}/4chart.py" && echo "4chart.py completed successfully." | tee -a "$LOG_FILE" || { echo "4chart.py failed. Exiting." | tee -a "$LOG_FILE"; exit 1; }
python3 "${WORK_DIR}/top100img.py" && echo "top100img.py completed successfully." | tee -a "$LOG_FILE" || { echo "top100img.py failed. Exiting." | tee -a "$LOG_FILE"; exit 1; }
python3 "${WORK_DIR}/tpo.py" && echo "tpo.py completed successfully." | tee -a "$LOG_FILE" || { echo "tpo.py failed. Exiting." | tee -a "$LOG_FILE"; exit 1; }
python3 "${WORK_DIR}/tpoimg.py" && echo "tpoimg.py completed successfully." | tee -a "$LOG_FILE" || { echo "tpoimg.py failed. Exiting." | tee -a "$LOG_FILE"; exit 1; }

# Log PDF generation start time
echo "PDF generation started at: $(date)" | tee -a "$LOG_FILE"

# Generate your PDF and check for success
echo "Generating PDF..." | tee -a "$LOG_FILE"
python3 "${WORK_DIR}/pdf.py" && echo "PDF generated successfully." | tee -a "$LOG_FILE" || { echo "PDF generation failed. Exiting." | tee -a "$LOG_FILE"; exit 1; }

# Log PDF generation end time
echo "PDF generation finished at: $(date)" | tee -a "$LOG_FILE"

# Wait a bit for filesystem operations to settle - just to be safe
sleep 2

# Remove PNG and text files
echo "Cleaning up intermediate files..." | tee -a "$LOG_FILE"
rm -f ${WORK_DIR}/*.png
rm -f ${WORK_DIR}/*.txt

# Path to the PDF file you want to print
FILE_PATH="${WORK_DIR}/Bulletin.pdf"

# Check if the file exists and print it
if [ -f "$FILE_PATH" ]; then
    # Log before printing
    echo "Attempting to print at: $(date)" | tee -a "$LOG_FILE"
    echo "Printing the file..." | tee -a "$LOG_FILE"
    lpr -o sides=two-sided-long-edge -o ColorModel=Gray "$FILE_PATH" && echo "Sent to printer: $FILE_PATH" | tee -a "$LOG_FILE" || echo "Printing failed." | tee -a "$LOG_FILE"
else
    echo "Error: File does not exist at $FILE_PATH" | tee -a "$LOG_FILE"
fi
