import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.utils import to_categorical


def train(df):
    print("Splitting data into train and test")
    # split data into train and test
    train, test = train_test_split(df, test_size=0.2, shuffle=False)

    # split data into X and y
    X_train = train.drop(["target"], axis=1)
    y_train = train["target"]
    X_test = test.drop(["target"], axis=1)
    y_test = test["target"]
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    [y_pred, history, model] = train_nn(X_train, y_train, X_test)
    predictions = y_pred.round()

    # calculate rmse
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    # plot loss during training and accuracy
    # plt.plot(history.history["accuracy"], label="accuracy")
    # plt.legend()
    # plt.show()
    return model


def train_nn(X_train, y_train, X_test):
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(9, activation="softmax"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    history = model.fit(X_train, y_train, epochs=30, batch_size=64, verbose=1)
    y_pred = model.predict(X_test)
    return [y_pred, history, model]


def train_xgb(X_train, y_train, X_test):
    model = XGBClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred


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
