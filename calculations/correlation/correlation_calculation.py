from datetime import datetime

import matplotlib
import pandas as pd
import yfinance as yf

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from sklearn.linear_model import LinearRegression
import textwrap

import seaborn as sns
from auxiliar.feed_security_data import preDownloadSecurityDB


def calculation_multiple(assetlist):
    img = io.BytesIO()
    df = pd.DataFrame()
    data = pd.DataFrame()
    endDate = datetime.today().strftime('%Y-%m-%d')
    missingData = False
    for item, asset in enumerate(assetlist):
        data = yf.download(asset, '2000-01-01', endDate)
        if data.empty:
            missingData = True
            return None, missingData, asset
        data['pct_change'] = data['Close'].pct_change()
        name, asset_type, exchange, market, currency, isin = preDownloadSecurityDB(asset)
        df[name] = data['pct_change']

    data.dropna()
    fig, ax = plt.subplots(figsize=(16, 12), dpi=100)
    corrMatrix = df.corr()
    heatmap = sns.heatmap(corrMatrix, vmin=corrMatrix.values.min(), vmax=1, square=True, cmap="YlGnBu", linewidths=0.1,
                          annot=True,
                          annot_kws={"fontsize": 14})

    labels = [textwrap.fill(label.get_text(), 12) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, fontsize=12, rotation=90)

    labels_y = [textwrap.fill(label.get_text(), 12) for label in ax.get_yticklabels()]
    ax.set_xticklabels(labels_y, fontsize=12, rotation=0)

    # heatmap = sns.heatmap(corrMatrix, annot=True, ax=ax, cmap='Spectral', fmt='.2f')
    ax.plot()
    fig = heatmap.get_figure()
    plt.savefig(img, format='png')
    plt.title("Asset Classes Correlation Matrix")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())

    return plot_url, missingData, asset


def correlation_two(ticker_a, ticker_b, log_returns):
    img = io.BytesIO()
    X = log_returns[ticker_a].iloc[1:].to_numpy().reshape(-1, 1)
    Y = log_returns[ticker_b].iloc[1:].to_numpy().reshape(-1, 1)
    sns.set(style="darkgrid")

    lin_regr = LinearRegression()
    lin_regr.fit(X, Y)
    Y_pred = lin_regr.predict(X)
    alpha = lin_regr.intercept_[0]
    alpha = str(round(alpha, 4))
    beta = lin_regr.coef_[0, 0]
    beta = str(round(beta, 2))
    fig, ax = plt.subplots(figsize=(20, 10), dpi=80)
    ax.scatter(X, Y)
    # sns.scatterplot(X, Y, ax=ax)
    ax.plot(X, Y_pred, c='g')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())

    # plt.show()
    return alpha, beta, plot_url
