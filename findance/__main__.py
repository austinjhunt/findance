#!/usr/bin/env python
# This does not work with Python 3.8
# Works with Python3.6 
import yfinance as yf 
from findance import FinDance 
# Yahoo finance datetimes are received as UTC 
# Use Ticker module to access ticker data in more Pythonic way 
# A stock ticker reports transaction and price data for a security, updated continuously throughout the day.

def main(): 
    findance = FinDance(
        csv_file="NASDAQ_JAN28_2021_10_06AM.csv",
        output_folder_path="json_data"
        )
    findance.store_symbol_ticker_data("MSFT")
    findance.write_symbol_ticker_data("MSFT")

if __name__ == "__main__": 
    main() 