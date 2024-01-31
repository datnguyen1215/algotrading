#!/usr/bin/python3
import pandas as pd
from preprocess import candles

def main():
    test = pd.DataFrame()
    last_data = test.iloc[-1]
    print(last_data)
    pass

if __name__ == '__main__':
    main()