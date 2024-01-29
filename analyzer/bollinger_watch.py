#!/usr/bin/python3
import requests
import argparse
import ta
import time
from lib.metatrader.expert import Expert
from lib.metatrader.server import start_server, accept_client
import pandas as pd

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1194178710497140746/dZyEYCVABWEcgYcMRq-LYI55bghrt2wu1f6Uo-uX8YV5J9X66X1aA14aJkGW1ey75e99"

SYMBOL = [
    "AUDCHF",
    "AUDJPY",
    "AUDUSD",
    "AUDCAD",
    "AUDNZD",
    "CADCHF",
    "CADJPY",
    "CHFJPY",
    "EURAUD",
    "EURCAD",
    "EURCHF",
    "EURGBP",
    "EURJPY",
    "EURUSD",
    "EURNZD",
    "GBPAUD",
    "GBPCHF",
    "GBPJPY",
    "GBPUSD",
    "GBPCAD",
    "GBPNZD",
    "NZDCAD",
    "NZDCHF",
    "NZDJPY",
    "NZDUSD",
    "USDCAD",
    "USDCHF",
    "USDJPY",
]


def get_data(symbol, timeframe, expert):
    data = expert.get_candles(symbol, timeframe, 500)
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    df = df.sort_index()

    # add bollingerband period = 30
    df["bb_upper"] = ta.volatility.bollinger_hband(df["close"], window=30, window_dev=2)
    df["bb_lower"] = ta.volatility.bollinger_lband(df["close"], window=30, window_dev=2)

    # add rsi period = 13
    df["rsi"] = ta.momentum.rsi(df["close"], window=13)

    return df


def is_high_above_upper_band(candle):
    return candle["high"] > candle["bb_upper"]


def is_low_below_lower_band(candle):
    return candle["low"] < candle["bb_lower"]


def is_rsi_above_70(candle):
    return candle["rsi"] > 70


def is_rsi_below_30(candle):
    return candle["rsi"] < 30


def main(args):
    timeframe = args.timeframe
    server_socket = start_server()
    client_socket = accept_client(server_socket)
    expert = Expert(client_socket)

    # for every minute, check if there is a signal
    while True:
        for symbol in SYMBOL:
            df = get_data(symbol, timeframe, expert)
            candle = df.iloc[-1]

            if is_high_above_upper_band(candle) and is_rsi_above_70(candle):
                message = {
                    "content": f"{symbol}, touched upper band, rsi > 70",
                    "username": "Bollinger Watch",
                }
                requests.post(DISCORD_WEBHOOK, message)
                print(message["content"])

            if is_low_below_lower_band(candle) and is_rsi_below_30(candle):
                message = {
                    "content": f"{symbol}, touched lower band, rsi < 30",
                    "username": "Bollinger Watch",
                }
                requests.post(DISCORD_WEBHOOK, message)
                print(message["content"])

        time.sleep(60)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", type=str, default="5Min")
    args = parser.parse_args()
    main(args)
