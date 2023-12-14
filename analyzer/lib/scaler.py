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
    flat_data = df.values.flatten()

    # initialize scalers
    negative_scaler = MinMaxScaler(feature_range=(0, 0.5))
    positive_scaler = MinMaxScaler(feature_range=(0.5, 1))

    # perform scaling
    flat_data[flat_data < 0] = negative_scaler.fit_transform(
        flat_data[flat_data < 0].reshape(-1, 1)
    ).ravel()
    flat_data[flat_data > 0] = positive_scaler.fit_transform(
        flat_data[flat_data > 0].reshape(-1, 1)
    ).ravel()

    # reshape data back to original shape
    scaled_df = pd.DataFrame(
        flat_data.reshape(df.shape), columns=df.columns, index=df.index
    )

    return [scaled_df, positive_scaler, negative_scaler]
