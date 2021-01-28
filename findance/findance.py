#!/usr/bin/env python
import csv, yfinance, os, time, json, pandas as pd 
# Pronounced "find ance"
# Like finance, but we are finding things in the financial data 

class FinDance: 
    def __init__(self, csv_file=None,output_folder_path=None): 
        """ Parameters: 
        csv_file = full path OR file object pointing at a CSV file pulled from https://www.nasdaq.com/market-activity/stocks/screener containing Nasdaq data
        output_folder_path = path to output folder
        """ 
        self._validate_csv_file(csv_file)
        self._validate_output_folder_path(output_folder_path)
        self.set_nasdaq_symbols() 

        ## Initialize empty dictionary to store data for each symbol 
        self.symbols_ticker_data = {}

        # Use these keys to create data files (named after the keys) within timestamped folders for each symbol 
        self.yfinance_keys = [
            'info',
            'history',
            'actions',
            'dividends',
            'splits',
            'financials',
            'quarterly_financials',
            'major_holders',
            'institutional_holders',
            'balance_sheet',
            'quarterly_balance_sheet',
            'cashflow',
            'quarterly_cashflow',
            'earnings',
            'quarterly_earnings',
            'sustainability',
            'recommendations',
            'calendar',
            'isin',
            'options'
            ]

    
    def _validate_csv_file(self, csv_file): 
        try: 
            # Will succeed if csv_file is a path to a valid CSV file 
            self.csv_file = open(csv_file)
        except FileNotFoundError: 
            # File wasn't found
            self.csv_file = None 
        except TypeError: 
            # It is already a file object
            self.csv_file = csv_file 
    
    def _validate_output_folder_path(self,output_folder_path): 
        try:
            if os.path.exists(output_folder_path) and os.path.isdir(output_folder_path): 
                self.output_folder_path = output_folder_path
            else: 
                self.output_folder_path = None 
        except: 
            self.output_folder_path = None 

    
    def set_nasdaq_symbols(self):
        """ Method to get all of the symbols from self.csv_file """ 
        self.nasdaq_symbols = None 
        if self.csv_file: 
            dr = csv.DictReader(self.csv_file)
            # Skip header 
            self.nasdaq_symbols = [stock['Symbol'] for stock in dr]  

    def store_symbol_ticker_data(self, symbol=None): 
        """ Story a dictionary of 
            symbol: symbolTicker 
            key-value pairs in self.symbols_ticker_data 
        """
        if self.output_folder_path and symbol: 
            try: 
                symbol_ticker = yfinance.Ticker(symbol) 
                self.symbols_ticker_data[symbol] = symbol_ticker
            except:
                self.symbols_ticker_data[symbol] = None 

    def store_all_symbols_ticker_data(self): 
        """ Loop through all Nasdaq symbols and store their Ticker objects 
        in a self.symbols_ticker_data as {symbolname:symbolticker, symbolname:symbolticker, etc.}
        """ 
        if self.nasdaq_symbols: 
            for symbol in self.nasdaq_symbols: 
                ## Store symbol in self.symbols_ticker_data 
                self.store_symbol_ticker_data(symbol)

    def write_symbol_ticker_data(self, symbol=None): 
        """ Write a given symbol's ticker data to a timestamped folder for 
        that symbol in JSON format """
        if self.output_folder_path and symbol: 
            timestr = time.strftime("%Y%m%d-%H%M%S")
            symbol_folder_path = f'{self.output_folder_path}/{timestr}/{symbol}'
            try:
                os.makedirs(symbol_folder_path)
            except FileExistsError:
                pass 
            try: 
                symbolTicker = self.symbols_ticker_data[symbol]
                #json.dump(symbolTicker.info, f)
            except KeyError as e:
                print(e)
                print(self.symbols_ticker_data)

            ## Loop through the different keys offered by the Ticker 
            for key in self.yfinance_keys: 
                ticker_value_for_current_key = getattr(symbolTicker, key)
                ## Write a file in this timestamped symbol's folder for each key, named after the key.  
                try:
                    with open(f'{symbol_folder_path}/{key}.json', 'w') as f: 
                        json.dump(ticker_value_for_current_key, f)
                except TypeError as e:  
                    os.remove(f'{symbol_folder_path}/{key}.json')
                    if isinstance(ticker_value_for_current_key, pd.DataFrame):
                        # If it's a Data Frame built with Pandas, use dataframe.to_csv method
                        # to write to CSV instead of JSON
                        try: 
                            ticker_value_for_current_key.to_csv(
                               f'{symbol_folder_path}/{key}.csv' 
                            )
                        except: 
                            pass 
                

    def write_all_symbol_ticker_data(self):
        """ Loop through all symbols in self.symbols_ticker_data items and
        write their Ticker data to timestamped folders named after each symbol """ 
        if self.output_folder_path and self.symbols_ticker_data:  
            for symbolName, symbolTicker in self.symbols_ticker_data.items(): 
                self.write_symbol_ticker_data(symbol=symbolName)

                    


