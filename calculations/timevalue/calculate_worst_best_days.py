
import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

from auxiliar.feed_security_data import preDownloadSecurityDB



def calculate_worst_best(asset):
    df = pd.DataFrame()
    endDate = datetime.today().strftime('%Y-%m-%d')
    missingData = False
    data = yf.download(asset, '1980-01-01', endDate)
    if data.empty:
        missingData = True
        return None, None, missingData
    data.dropna()
    data['pct_change'] = data['Close'].pct_change()
    name, asset_type, exchange, market, currency = preDownloadSecurityDB(asset)
    calculate_holdings(asset, exchange, market, currency)
    df[asset] = data['pct_change']
    df = df.sort_values(by=asset)
    df = df.dropna()
    df = df.mul(100).round(2).astype(str).add(' %')



    return df.head(10), df.tail(10), missingData
