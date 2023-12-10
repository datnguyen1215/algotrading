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

    return [df_scaled, scaler]

def scale_target(target):
    negative_target = target
    negative_target = negative_target.apply(lambda x: max(x, 0))

    # scale to be between -4 and 0
    scaler = MinMaxScaler(feature_range=(-4, 0))
    negative_target = scaler.fit_transform(negative_target.values.reshape(-1, 1))

    positive_target = target
    positive_target = positive_target.apply(lambda x: min(x, 0))

    # scale to be between 0 and 4
    scaler = MinMaxScaler(feature_range=(0, 4))
    positive_target = scaler.fit_transform(positive_target.values.reshape(-1, 1))

    target = negative_target + positive_target

    # need to +4 to map it from 0 to 8. Otherwise, we'll have problems with
    # classifier.
    target = target.round().astype(int) + 4

    return target