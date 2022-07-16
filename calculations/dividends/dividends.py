
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import seaborn as sns
import pandas as pd
from auxiliar.feed_security_data import preDownloadSecurityDB
from auxiliar.ft import calculate_ft
from auxiliar.retrieve_company_info import retrieve_info

matplotlib.use('Agg')


def retrieve_dividends(asset):
    missingData = False
    security_info = []
    dividend_info = []
    company_info = []
    financial_info = []
    data = yf.Ticker(asset).get_dividends()
    if len(data) == 0:
        missingData = True
        return missingData, None, None, None, None
    data.dropna()
    data = data.round(2)
    name, asset_type, exchange, market, currency, isin = preDownloadSecurityDB(asset)
    security_info.append(name)
    security_info.append(currency)
    security_info.append(asset)

    company_info, financial_info = retrieve_info(asset)


    df = data.to_frame()
    mean = data.mean().round(2)
    last_5 = df.tail(5)
    mean_5 = last_5.values.mean()
    mean_5 = round(mean_5, 2)
    dividend_info.append(mean)
    dividend_info.append(mean_5)

    values = df.values.tolist()
    values = [row[0] for row in values]
    list_lists = []
    labels = df.index.values.tolist()
    labels = pd.to_datetime(df.index).strftime('%Y-%m-%d').tolist()
    for column in df.columns:
        list_lists.append(df[column].values.tolist())





    return missingData, dividend_info, last_5, values, labels, security_info, company_info, financial_info
