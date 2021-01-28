# findance (pronounced: find ance)
A small-but-growing package for finding and collecting financial data from Nasdaq and expanding upon the scope of the data using the Yahoo! Finance API which is nicely wrapped by the open source project [yfinance](https://github.com/ranaroussi/yfinance)

## Usage
To start, clone the repository. 
``` git clone https://github.com/austinjhunt/findance ```
Then, go to the [Nasdaq Stock Screener](https://www.nasdaq.com/market-activity/stocks/screener), apply any filters you wish to apply to narrow down the scope to stocks you are interested in, and choose "Download CSV". 

Next, move that file you downloaded to the root of this project (or just make a note of its current path). 

Create a virtual environment with Python3.6, activate it, and install the requirements.
``` 
python3.6 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt 
```

Now, you can use the findance package. 
### Parameters
-  ```--nasdaq``` ; this is the most important parameter; use this to tell the package what Nasdaq CSV file you want to use as your source of symbols.  
-  ```--handle-all-symbols``` ; if you want to collect and write out data for ALL symbols in your Nasdaq files, pass this followed by a '1' for 'True'.
-  ```--symbol``` ; if you do not use --handle-all-symbols, you need to specify which symbol you want to collect the data for. Pick a symbol from your Nasdaq CSV. It needs to match. 
-  ```--output-folder``` ; this tells the package where to write the data that it collects from Yahoo! Finance. In this folder, the package will create a timestamped folder with subfolders for either all symbols or just the one symbol you specified (dependent on --handle-all-symbols or --symbol); each symbol folder will contain a set of CSV/JSON files built from the Yahoo! Finance historical data for that symbol. The default output folder is json_data in the root of this project. There is already sample data in that folder to give you an idea of the structure. 

### Example:

``` python findance --nasdaq NASDAQ_JAN28_2021_10_06AM.csv --symbol MSFT ```
The above invocation would tell findance to use the file NASDAQ_JAN28_2021_10_06AM.csv pulled from the [Nasdaq Stock Screener](https://www.nasdaq.com/market-activity/stocks/screener) and to only pull data for the MSFT stock symbol. Since no --output-folder argument was passed, the default json_data folder is used as the output folder. 