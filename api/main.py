import h2o
from h2o.automl import H2OAutoML
from fastapi import FastAPI
from pydantic import BaseModel

h2o.init()
saved_model = h2o.load_model("StackedEnsemble_BestOfFamily_1_AutoML_2_20230505_53230")
app = FastAPI()

class InputData(BaseModel):
    vol_moving_avg: float
    adj_close_rolling_med: float
    symbol: str
    etf: bool
    rsi: float
    tema: float

@app.post("/predict")
def predict_trading_volume(input_data: InputData):
    # Extract input values from the request body
    vol_moving_avg = input_data.vol_moving_avg
    adj_close_rolling_med = input_data.adj_close_rolling_med
    symbol = input_data.symbol
    etf = input_data.etf
    rsi = input_data.rsi
    tema = input_data.tema
    
    frame = h2o.H2OFrame({"Symbol":symbol, "etf":etf, "rsi":rsi, "tema":tema, "vol_moving_avg":vol_moving_avg, "adj_close_rolling_med":adj_close_rolling_med})
    result = saved_model.predict(frame)
    print(result.as_data_frame()[1][0])
    # Return the predicted trading volume as a response
    return {"trading_volume": result.as_data_frame()[1][0]}