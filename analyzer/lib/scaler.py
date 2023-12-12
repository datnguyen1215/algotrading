from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd


def scale(df, scaler=None):
    # scale the data
    if scaler is None:
        scaler = MinMaxScaler()

    df_scaled = scaler.fit_transform(df[df.columns.array])
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

    return [df_scaled, scaler]


# since targets are angles of the movement, we need to scale them differently
# we'll split the target into two groups, one for positive angles and one for negative angles
# then we'll scale them separately
def scale_angle(df):
    negative_df = df.copy()
    negative_df[negative_df > 0] = 0

    negative_scaler = MinMaxScaler(feature_range=(0, 0.5))
    negative_df = negative_scaler.fit_transform(df)

    positive_df = df.copy()
    positive_df[positive_df < 0] = 0

    positive_scaler = MinMaxScaler(feature_range=(0.5, 1))
    positive_df = positive_scaler.fit_transform(df)

    df[df > 0] = positive_df
    df[df < 0] = negative_df

    return [df, positive_scaler, negative_scaler]
