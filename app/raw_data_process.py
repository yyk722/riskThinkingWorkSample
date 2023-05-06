import os
import zipfile
import subprocess
import pandas as pd
import os
import concurrent.futures
import time

cmd_str = 'pip install -q kaggle'
subprocess.run(cmd_str, shell=True)

os.environ['KAGGLE_USERNAME'] = "yyk722" # username from the json file
os.environ['KAGGLE_KEY'] = "18d96fe82c283d0153d782f86e597ac3" # key from the json file

cmd_str = "kaggle datasets download -d jacksoncrow/stock-market-dataset"
subprocess.run(cmd_str, shell=True)

with zipfile.ZipFile('stock-market-dataset.zip', 'r') as zip_file:
    zip_file.extractall('./')

dtypes = {
    'Symbol': str,
    'Security Name': str,
    'Date': str,
    'Open': float,
    'High': float,
    'Low': float,
    'Close': float,
    'Adj Close': float,
    'Volume': int
    }

symbols_valid_meta = pd.read_csv("symbols_valid_meta.csv")
symbols_valid_meta = symbols_valid_meta[['Symbol', 'Security Name', 'ETF']]

symbols_valid_meta_stocks = symbols_valid_meta[symbols_valid_meta.ETF=='N']
symbols_valid_meta_etfs = symbols_valid_meta[symbols_valid_meta.ETF=='Y']

symbols_valid_meta_stocks_symbol = symbols_valid_meta_stocks.Symbol.to_list()
symbols_valid_meta_stocks_security_name = symbols_valid_meta_stocks['Security Name'].to_list()
symbols_valid_meta_etfs_symbol = symbols_valid_meta_etfs.Symbol.to_list()
symbols_valid_meta_etfs_security_name = symbols_valid_meta_etfs['Security Name'].to_list()

if not os.path.exists("stocks_result"):
    os.mkdir('stocks_result')
if not os.path.exists("etfs_result"):
    os.mkdir('etfs_result')

def process_stock_file(symbol):
    df = pd.read_csv('stocks/'+symbol+'.csv')
    df['Symbol'] = symbol
    df['Security Name'] = symbols_valid_meta_stocks_security_name[symbols_valid_meta_stocks_symbol.index(symbol)]
    df = df.astype(dtypes)
    df.to_parquet('stocks_result/'+symbol+'.parquet')

# Create a thread pool with a maximum threads
max_threads_list = [16]
for max_threads in max_threads_list:
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each stock symbol to the thread pool for processing
        futures = [executor.submit(process_stock_file, symbol) for symbol in symbols_valid_meta_stocks_symbol]
        # Wait for all threads to complete
        concurrent.futures.wait(futures)
    end_time = time.time()
    execution_time = end_time - start_time
    print("STOCK Execution time:", execution_time)

def process_etf_file(symbol):
    df = pd.read_csv('etfs/'+symbol+'.csv')
    df['Symbol'] = symbol
    df['Security Name'] = symbols_valid_meta_etfs_security_name[symbols_valid_meta_etfs_symbol.index(symbol)]
    df = df.astype(dtypes)
    df.to_parquet('etfs_result/'+symbol+'.parquet')

# Create a thread pool with a maximum threads
max_threads_list = [16]
for max_threads in max_threads_list:
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each stock symbol to the thread pool for processing
        futures = [executor.submit(process_etf_file, symbol) for symbol in symbols_valid_meta_etfs_symbol]
        # Wait for all threads to complete
        concurrent.futures.wait(futures)
    end_time = time.time()
    execution_time = end_time - start_time
    print("ETF Execution time:", execution_time)