from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd

def scale(df):
    # save the time column for later use
    index = df.index

    # scale the data
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[df.columns.array])
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    
    # use time as index
    df_scaled.index = index

    return df_scaled
