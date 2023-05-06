import subprocess
cmd_str = 'pip install pandas-ta'
subprocess.run(cmd_str, shell=True)

#import talib.abstract as ta
import pandas_ta as pta
import os
import time
import concurrent.futures
import pandas as pd

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

if not os.path.exists("stage"):
    os.mkdir('stage')
if not os.path.exists("stage/stocks_result"):
    os.mkdir('stage/stocks_result')
if not os.path.exists("stage/etfs_result"):
    os.mkdir('stage/etfs_result')

symbols_valid_meta = pd.read_csv("symbols_valid_meta.csv")
symbols_valid_meta = symbols_valid_meta[['Symbol', 'Security Name', 'ETF']]

symbols_valid_meta_stocks = symbols_valid_meta[symbols_valid_meta.ETF=='N']
symbols_valid_meta_etfs = symbols_valid_meta[symbols_valid_meta.ETF=='Y']

symbols_valid_meta_stocks_symbol = symbols_valid_meta_stocks.Symbol.to_list()
symbols_valid_meta_stocks_security_name = symbols_valid_meta_stocks['Security Name'].to_list()
symbols_valid_meta_etfs_symbol = symbols_valid_meta_etfs.Symbol.to_list()
symbols_valid_meta_etfs_security_name = symbols_valid_meta_etfs['Security Name'].to_list()


def fe_stock_file(symbol):
    df = pd.read_parquet('stocks_result/'+symbol+'.parquet')
    df['close'] = df['Close']
    # Convert the Date column to a datetime data type
    df["Date"] = pd.to_datetime(df["Date"])

    # Set the Date column as the DataFrame's index
    df.set_index("Date", inplace=True)

    # Calculate the rolling 30-day average of the Volume column
    df["vol_moving_avg"] = df["Volume"].rolling(window=30).mean()
    df["adj_close_rolling_med"] = df["Adj Close"].rolling(window=30).median()
    
    # RSI
    df['rsi'] = pta.rsi(df['close'], length = 30)
    # TEMA - Triple Exponential Moving Average
    df["tema"] = pta.ma('tema', df['close'], length=30)

    # Drop any rows with missing values
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df = df.astype(dtypes)
    df.to_parquet('stage/stocks_result/'+symbol+'.parquet')
    
# Create a thread pool with a maximum threads
max_threads_list = [16]
for max_threads in max_threads_list:
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each stock symbol to the thread pool for processing
        futures = [executor.submit(fe_stock_file, symbol) for symbol in symbols_valid_meta_stocks_symbol]
        # Wait for all threads to complete
        concurrent.futures.wait(futures)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)

def fe_etf_file(symbol):
    df = pd.read_parquet('etfs_result/'+symbol+'.parquet')
    df['close'] = df['Close']
    # Convert the Date column to a datetime data type
    df["Date"] = pd.to_datetime(df["Date"])

    # Set the Date column as the DataFrame's index
    df.set_index("Date", inplace=True)

    # Calculate the rolling 30-day average of the Volume column
    df["vol_moving_avg"] = df["Volume"].rolling(window=30).mean()
    df["adj_close_rolling_med"] = df["Adj Close"].rolling(window=30).median()

    # RSI
    df['rsi'] = pta.rsi(df['close'], length = 30)
    # TEMA - Triple Exponential Moving Average
    df["tema"] = pta.ma('tema', df['close'], length=30)
    
    # Drop any rows with missing values
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df = df.astype(dtypes)
    df.to_parquet('stage/etfs_result/'+symbol+'.parquet')
    
# Create a thread pool with a maximum threads
max_threads_list = [16]
for max_threads in max_threads_list:
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each stock symbol to the thread pool for processing
        futures = [executor.submit(fe_etf_file, symbol) for symbol in symbols_valid_meta_etfs_symbol]
        # Wait for all threads to complete
        concurrent.futures.wait(futures)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)