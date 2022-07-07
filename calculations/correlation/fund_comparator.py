import matplotlib
import pandas as pd
import yfinance as yf

from auxiliar.ft import calculate_profile, calculate_ft

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from datetime import datetime
from dateutil.relativedelta import relativedelta

import seaborn as sns
from auxiliar.feed_security_data import retrieveFunds, retrieveSecurityDB, preDownloadSecurityDB


def calculate_funds(asset):
    img = io.BytesIO()
    df = pd.DataFrame()
    data = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    end_date = end_date

    price = 0
    last_change = 0
    last_pct_change = 0
    price_last_year = 0
    funds_list = []


    start_date = datetime.today() - relativedelta(years=3)
    start_date = start_date.strftime('%Y-%m-%d')
    missingData = False
    name, asset_type, exchange, market, currency = preDownloadSecurityDB(asset)
    if asset_type == 'EQUITY':
        funds_list = calculate_ft(asset, asset_type, exchange, market, currency)
        funds_list.append(asset)
        funds_list = list(set(funds_list))
        funds_list.remove(asset)
        funds_list.insert(0, asset)
    else:
        funds_list.append(asset)
        funds_list = funds_list + retrieveFunds()
        funds_list = list(set(funds_list))
        funds_list.remove(asset)
        funds_list.insert(0, asset)

    for fund in funds_list:
        fund = str(fund).strip("()").replace(',','')
        data = yf.download(fund, start_date, end_date)
        if data.empty:
            continue
            missingData = True

        data = data.round(2)
        if fund == asset:
            price = yf.Ticker(asset).get_info()['regularMarketPrice']
            last_price = data['Close'][-1]
            last_change = price - last_price
            last_pct_change = (price - last_price)/last_price * 100
            price_last_year = data['Close'][-255]
            change_last_year = (price - price_last_year)/price_last_year* 100

            last_change = round(last_change, 2)
            last_pct_change = round(last_pct_change, 2)
            change_last_year = round(change_last_year, 2)


        security = retrieveSecurityDB(fund)
        if (security is not None):
            fund = security.name


        start_price = data.Close[0]
        end_price = data.Close[-1]
        return_3 = (end_price - start_price) / start_price * 100 / 3
        std_3 = data['Close'].std() / 3
        df2 = pd.DataFrame({'Return_3': return_3, 'Std_3': std_3}, index=[fund])
        df = df.append(df2, ignore_index=False)

    security = retrieveSecurityDB(asset)
    if (security is not None):
        asset = security.name

    fig, ax = plt.subplots()
    sharpe_ratio = df.loc[asset].Return_3/ df.loc[asset].Std_3

    scatter = sns.scatterplot(data=df, x='Return_3', y='Std_3')

    values_list = []
    labels_list = []
    df = df.round(2)
    for idx, row in df.iterrows():
        d = {'x': row['Return_3']}
        d['y'] = row['Std_3']
        d['z'] = idx
        labels_list.append(idx)
        values_list.append(d)
        plt.text(row['Return_3'], row['Std_3'], idx)
    ax.set_xlabel("Return")
    ax.set_ylabel("Standard Deviation")

    print(values_list)
    print(labels_list)


    ax.plot()
    fig = scatter.get_figure()
    plt.savefig(img, format='png')
    plt.title("Asset Classes Correlation Matrix")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())

    return plot_url, missingData, asset, return_3, std_3, values_list, labels_list, price, price_last_year, last_change, last_pct_change, change_last_year
