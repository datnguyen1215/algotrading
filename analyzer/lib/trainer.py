import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor, XGBClassifier
import xgboost
from sklearn.metrics import mean_squared_error, accuracy_score
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam


def train(df, target_columns=["target"]):
    # split data into train and test
    train, test = train_test_split(df, test_size=0.2, shuffle=True)

    # split data into X and y
    X_train = train.drop(target_columns, axis=1)
    y_train = train[target_columns]
    X_test = test.drop(target_columns, axis=1)
    y_test = test[target_columns]

    [y_pred, history, model] = train_xgb(X_train, y_train, X_test)

    # get mse
    mse = mean_squared_error(y_test, y_pred)
    print("mse: ", mse)

    # plot actual and prediction
    # plt.plot(y_test.values[:200], label="actual")
    # plt.plot(y_pred[:200], label="prediction")
    # plt.legend()
    # plt.show()
    return model


def train_nn(X_train, y_train, X_test):
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(4, activation="relu"))
    model.add(Dense(y_train.shape[1], activation="sigmoid"))
    # regression
    optimizer = Adam(lr=0.01)
    model.compile(optimizer=optimizer, loss="mse", metrics=["mse"])
    history = model.fit(X_train, y_train, epochs=1000, batch_size=64, verbose=1)
    y_pred = model.predict(X_test)
    return [y_pred, history, model]


def train_xgb(X_train, y_train, X_test):
    xgboost.set_config(verbosity=2)
    model = XGBRegressor(objective="reg:squarederror", n_estimators=1000, max_depth=32)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred, [], model


def get_model_cnn(data):
    model = Sequential()
    model.add(
        Conv1D(
            filters=64, kernel_size=2, activation="relu", input_shape=(data.shape[1], 1)
        )
    )
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation="relu"))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    return model
