import re

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
from yahoo_fin import stock_info as si
from feed_security_data import preDownloadSecurityDB
import requests
import csv



def parse_csv_symbols_country(name):
    ticker_list = []
    with open(name+'.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

        for ticker in data:
            for tick in ticker:
                ticker_list.append(tick)

        print(ticker_list)
    return ticker_list
