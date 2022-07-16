from datetime import datetime

import matplotlib
import pandas as pd
import yfinance as yf

matplotlib.use('Agg')

from auxiliar.feed_security_data import preDownloadSecurityDB


def calculate_worst_best(asset):
    df = pd.DataFrame()
    endDate = datetime.today().strftime('%Y-%m-%d')
    prices_list = []
    security_info = []

    missingData = False
    data = yf.download(asset, '1980-01-01', endDate)
    if data.empty:
        missingData = True
        return None, None, missingData, None
    data = data.round(3)
    price = data['Close'][-1]
    prices_list.append(price)
    price_last_year = data['Close'][-255]
    prices_list.append(price_last_year)
    price_two_years_ago = data['Close'][-255 * 2]
    prices_list.append(price_two_years_ago)
    price_three_years_ago = data['Close'][-255 * 3]
    prices_list.append(price_three_years_ago)

    data.dropna()
    data['pct_change'] = data['Close'].pct_change()
    name, asset_type, exchange, market, currency, isin = preDownloadSecurityDB(asset)
    df['Change'] = data['pct_change']
    df = df.sort_values(by='Change')
    df = df.dropna()
    df = df.mul(100).round(2).astype(str).add(' %')
    df['Price'] = data['Close']
    security_info.append(name)
    security_info.append(currency)
    security_info.append(asset)

    return df.head(10), df.tail(10), missingData, prices_list, security_info
