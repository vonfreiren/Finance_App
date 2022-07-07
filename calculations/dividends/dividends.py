
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import seaborn as sns
import pandas as pd
from auxiliar.feed_security_data import preDownloadSecurityDB
from auxiliar.ft import calculate_ft

matplotlib.use('Agg')


def retrieve_dividends(asset):
    missingData = False
    data = yf.Ticker(asset).get_dividends()
    if len(data) == 0:
        missingData = True
        return None, missingData, None, None, None, None
    data.dropna()
    name, asset_type, exchange, market, currency = preDownloadSecurityDB(asset)


    calculate_ft(asset, asset_type, exchange, market, currency)

    df = data.to_frame()
    mean = data.mean()
    last_5 = df.tail()

    values = df.values.tolist()
    values = [row[0] for row in values]
    list_lists = []
    labels = df.index.values.tolist()
    labels = pd.to_datetime(df.index).strftime('%Y-%m-%d').tolist()
    for column in df.columns:
        list_lists.append(df[column].values.tolist())





    return missingData, mean, last_5, values, labels
