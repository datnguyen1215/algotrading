import pandas as pd

def candles_to_df(candles):
    """
    Convert candles to a dataframe.

    Parameters
    ----------
    candles : list
        List of candles.

    Returns
    -------
    pandas.DataFrame
        Dataframe of candles.
    """
    df = pd.DataFrame(candles)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df.drop(["symbol"], axis=1, inplace=True)
    return df
