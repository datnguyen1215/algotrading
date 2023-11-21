from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def scale(df):
    # save the time column for later use
    index = df.index
    
    print(df.head(15))

    # scale the data
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    
    # use time as index
    df_scaled.index = index
    
    return df_scaled