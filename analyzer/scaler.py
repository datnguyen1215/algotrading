from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd

def scale(df, scaler=None, excluded_columns=[]):
    # save the exclude
    tmp = df[excluded_columns]
    
    # drop it from the current data frame
    df = df.drop(excluded_columns, axis=1)

    # save the time column for later use
    index = df.index

    # scale the data
    if scaler is None:
        scaler = MinMaxScaler()

    df_scaled = scaler.fit_transform(df[df.columns.array])
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    
    # use time as index
    df_scaled.index = index
    
    # add the excluded columns back
    df_scaled[excluded_columns] = tmp

    return [df_scaled, scaler]

def scale_target(target):
    negative_target = target.copy()
    negative_target[negative_target > 0] = 0

    # scale to be between -4 and 0
    scaler = MinMaxScaler(feature_range=(-4, 0))
    negative_target = scaler.fit_transform(negative_target.values.reshape(-1, 1))

    positive_target = target.copy()
    positive_target[positive_target < 0] = 0

    # scale to be between 0 and 4
    scaler = MinMaxScaler(feature_range=(0, 4))
    positive_target = scaler.fit_transform(positive_target.values.reshape(-1, 1))

    target = negative_target + positive_target

    return target