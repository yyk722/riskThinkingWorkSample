from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from pathlib import Path
import pandas as pd

import h2o
from h2o.automl import H2OAutoML

n_stocks = 10

h2o.init()

df_list = []
pathlist = Path('./stage/stocks_result').rglob('*.parquet')
for path in pathlist:
    path_in_str = str(path)
    df = pd.read_parquet(path_in_str)
    if 'etfs' in path_in_str:
        df['etf'] = True
    else:
        df['etf'] = False
    df_list.append(df)
    if len(df_list)>n_stocks:
        break

pathlist = Path('./stage/etfs_result').rglob('*.parquet')
for path in pathlist:
    path_in_str = str(path)
    df = pd.read_parquet(path_in_str)
    if 'etfs' in path_in_str:
        df['etf'] = True
    else:
        df['etf'] = False
    df_list.append(df)
    if len(df_list)>n_stocks*2:
        break

data = pd.concat(df_list)

# Assume `data` is loaded as a Pandas DataFrame
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
# Remove rows with NaN values
data.dropna(inplace=True)

# Select features and target
features = ['vol_moving_avg', 'adj_close_rolling_med', 'etf', 'Symbol', 'rsi', 'tema']
target = ['Volume']

h2o_train, h2o_test = train_test_split(data, test_size=0.2, random_state=42)
h2o_train, h2o_test = h2o.H2OFrame(h2o_train), h2o.H2OFrame(h2o_test)

h2o_train['etf'] = h2o_train['etf'].asfactor()
h2o_train['Symbol'] = h2o_train['Symbol'].asfactor()

h2o_test['etf'] = h2o_test['etf'].asfactor()
h2o_test['Symbol'] = h2o_test['Symbol'].asfactor()

aml = H2OAutoML(max_models=20, seed=1)
aml.train(x=features, y=target[0], training_frame=h2o_train)

lb = aml.leaderboard
print(lb.head(rows=lb.nrows))

perf = aml.leader.model_performance(h2o_test)
print(perf)

model_path = h2o.save_model(model=aml.get_best_model(), path="./", force=True)
print(model_path)