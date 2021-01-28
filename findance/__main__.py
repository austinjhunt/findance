#!/usr/bin/env python
# This does not work with Python 3.8
# Works with Python3.6 
import yfinance as yf,argparse,sys
import time 
from yaspin import yaspin
from yaspin.spinners import Spinners
from util import str2bool 
from findance import FinDance  
# Yahoo finance datetimes are received as UTC 
# Use Ticker module to access ticker data in more Pythonic way 
# A stock ticker reports transaction and price data for a security, updated continuously throughout the day.

parser = argparse.ArgumentParser(description='Process arguments to findance')
parser.add_argument('--handle-all-symbols', metavar='A', type=bool, nargs=1, help='whether to handle all symbols in the Nasdaq CSV file', default=False)
parser.add_argument('--symbol', metavar='S',type=str,nargs=1, help='if handling one symbol, what symbol do you want to handle? must match the record in the Nasdaq csv')
parser.add_argument('--nasdaq', metavar='n', type=str, nargs=1, help='path to the Nasdaq csv file downloaded from Stock Screener')
parser.add_argument('--output-folder', metavar='f',type=str,nargs=1, help='path to the base output folder to write output data', default='json_data')

args = parser.parse_args()
 
def main():  
    spinner = yaspin(Spinners.shark, text="Searching the market sea for data...")
    spinner.start() 
    if args.nasdaq: 
        csv_file = args.nasdaq[0]
    else:
        spinner.stop()
        print("You need to pass --nasdaq <PATH TO DOWNLOADED NASDAQ CSV>")
        sys.exit(2)
    if args.output_folder:
        if isinstance(args.output_folder,list):
            output_folder = args.output_folder[0] 
        else: 
            output_folder = args.output_folder
    time.sleep(2)
    findance = FinDance(
        csv_file=csv_file,
        output_folder_path=output_folder
        ) 
    if not str2bool(args.handle_all_symbols):
        ## Only handle one symbol
        if args.symbol: 
            symbol = args.symbol[0] 
            spinner.text = f"Collecting data locally for symbol {symbol}..."
            findance.store_symbol_ticker_data(symbol) 
            spinner.text = f"Writing data to {output_folder}..."
            findance.write_symbol_ticker_data(symbol)
        else:
            spinner.stop()
            print("You must pass either --symbol <NASDAQ SYMBOL> or --handle-all-symbols")
            sys.exit(2)
    else:
        spinner.text = f"Collecting data locally for all symbols in {csv_file}..."
        findance.store_all_symbols_ticker_data()
        spinner.text = f"Writing data to {output_folder} for all symbols in {csv_file}..."
        findance.write_all_symbol_ticker_data()
    spinner.stop()

if __name__ == "__main__": 
    main() 