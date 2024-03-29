BoomerBot collects a bunch of handy info and sends it to a printer, saving your tired eyes a bit of screentime. 

make sure to chmod +x bb.sh bbp.sh

run ./bb.sh for a pdf in current folder

run ./bbp.sh to send to a printer; edit file location & printer command as per your system

This has been running on Mac manually, plan is to set up with cron job on raspberry pi

Dependencies:

mplfinance - Used for financial charting, particularly with candlestick charts.
pandas - A powerful data manipulation and analysis library.
yfinance - A library that allows for easy access to Yahoo Finance's market data.
pycoingecko - Provides an easy way to access the CoinGecko API for cryptocurrency data.
matplotlib - A comprehensive library for creating static, animated, and interactive visualizations in Python.
