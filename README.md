BoomerBot collects a bunch of handy info and sends it to a printer, saving your tired eyes a bit of screentime. 

Currently running on rpi1 with 1024mb swapfile 

make sure to chmod +x bb.sh bbp.sh

designed to run as 'work' user in a /home/work/boomerbot folder, otherwise will need changes for file locations in each script  

run ./bb.sh for a pdf in current folder

run ./bbp.sh to send to a printer; will print on system default printer 

To run on rpi, install python3, cups-bsd, and dependencies below: 

pip3 install mplfinance pandas yfinance pycoingecko matplotlib numpy Pillow fpdf requests
