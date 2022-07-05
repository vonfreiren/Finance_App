import matplotlib
import pandas as pd
import yfinance as yf

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from datetime import datetime
from dateutil.relativedelta import relativedelta

import seaborn as sns
from auxiliar.feed_security_data import retrieveFunds, retrieveSecurityDB


def calculate_funds(asset):
    img = io.BytesIO()
    df = pd.DataFrame()
    data = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    end_date = '2022-05-31'
    funds_list = []
    funds_list.append(asset)
    funds_list = funds_list + retrieveFunds()
    print(funds_list)
    funds_list = list(set(funds_list))
    funds_list.remove(asset)
    funds_list.insert(0, asset)
    print(funds_list)

    start_date = datetime.today() - relativedelta(years=3)
    start_date = start_date.strftime('%Y-%m-%d')
    missingData = False
    for fund in funds_list:
        fund = str(fund).strip("()").replace(',','')
        data = yf.download(fund, start_date, end_date)
        print(fund)
        if data.empty:
            missingData = True
            return None, missingData, asset, None, None


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
    print(df2)
    sharpe_ratio = df.loc[asset].Return_3/ df.loc[asset].Std_3

    scatter = sns.scatterplot(data=df, x='Return_3', y='Std_3')

    values_list = []
    labels_list = []
    pd.options.display.float_format = '{:.2f}'.format

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

    return plot_url, missingData, asset, return_3, std_3, values_list, labels_list
