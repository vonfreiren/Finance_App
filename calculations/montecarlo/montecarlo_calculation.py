
import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from auxiliar.feed_security_data import preDownloadSecurityDB


def calculation(assetList):
    endDate = datetime.today().strftime('%Y-%m-%d')
    startDate = '2000-01-01'
    df = pd.DataFrame()


    for asset in assetList:
        data = yf.download(asset, startDate, endDate)
        missingData = False
        if(data.empty):
            missingData = True
            return None, True
        name = preDownloadSecurityDB(asset)
        df[name] = data['Close']


    df.dropna()


    log_returns = np.log(df / df.shift())
    n = 5000
    weights = np.zeros((n, df.shape[1]))
    exp_rtns = np.zeros(n)
    exp_vols = np.zeros(n)
    sharpe_ratios = np.zeros(n)
    for i in range(n):
        weight = np.random.random(df.shape[1])
        weight /= weight.sum()
        weights[i] = weight

        exp_rtns[i] = np.sum(log_returns.mean() * weight) * 252
        exp_vols[i] = np.sqrt(np.dot(weight.T, np.dot(log_returns.cov() * 252, weight)))
        sharpe_ratios[i] = exp_rtns[i] / exp_vols[i]

    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(6,4))  # Sample figsize in inches
    ax.scatter(exp_vols, exp_rtns, c=sharpe_ratios)
    ax.scatter(exp_vols[sharpe_ratios.argmax()], exp_rtns[sharpe_ratios.argmax()], c='r')
    ax.set_xlabel('Expected Volatility')
    ax.set_ylabel('Expected Return')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    return plot_url, missingData
