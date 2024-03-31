BoomerBot collects a bunch of handy info and sends it to a printer, saving your tired eyes a bit of screentime. 

make sure to chmod +x bb.sh bbp.sh

run ./bb.sh for a pdf in current folder

run ./bbp.sh to send to a printer; edit file location & printer command as per your system

To run on rpi, install python3, cups-bsd, and dependencies below: 

pip3 install mplfinance pandas yfinance pycoingecko matplotlib numpy Pillow fpdf requests
