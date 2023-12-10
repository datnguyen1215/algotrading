import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH=os.getenv("MODEL_PATH")
SCALER_PATH=os.getenv("SCALER_PATH")
SYMBOL=os.getenv("SYMBOL")
N_CANDLES=os.getenv("N_CANDLES")