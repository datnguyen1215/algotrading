import requests
from . import candles_to_df

def get(symbol, n_candles=5000):
    """
    Get candles for a symbol.

    Parameters
    ----------
    symbol : str
        Symbol to get candles for.

    n_candles : int
        Number of candles to get.

    Returns
    -------
    list
    """
    url = f"http://localhost:3005/api/candles?limit={n_candles}&filter[symbol]={symbol}"
    r = requests.get(url)
    candles = r.json()
    return candles_to_df(candles)
