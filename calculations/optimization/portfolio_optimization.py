
import matplotlib

from auxiliar import constants

matplotlib.use('Agg')
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from datetime import datetime
import base64
import io
from auxiliar.feed_security_data import preDownloadSecurityDB
import numpy as np


def optimize(assetList, initialValue, calculation_method, risk):
    endDate = datetime.today().strftime('%Y-%m-%d')
    df = pd.DataFrame()
    missing_data = False

    for asset in assetList:
        data = yf.download(asset, '2000-01-01', endDate)
        if(data.empty):
            missing_data = True
            return None, None, None, None, None, missing_data

        name = preDownloadSecurityDB(asset)
        df[name] = data['Close']


    df.dropna()

    latest_prices = get_latest_prices(df)



    mu = mean_historical_return(df)
    S = CovarianceShrinkage(df).ledoit_wolf()


    ef = EfficientFrontier(mu, S)
    if(calculation_method== constants.SHARPE_RATIO):
        weights = ef.max_sharpe()
    elif (calculation_method == constants.MIN_VOLATILITY):
            weights = ef.min_volatility()

    elif (calculation_method == constants.MAX_RETURN):
        weights = ef._max_return()

    elif (calculation_method == constants.MAX_QUADRATIC_UTILITY):
        weights = ef.max_quadratic_utility()

    elif (calculation_method == constants.SPECIFIC_RISK):

        risk = adapt_risk(risk)
        weights = ef.efficient_risk(risk)

    else:
        weights= ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    ef.portfolio_performance(verbose=True)


    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=initialValue)

    allocation, leftover = da.greedy_portfolio()

    df2 = pd.DataFrame(allocation, index=[0])
    df3 = df2
    for column in df2:
        df3[column] = df[column].values[-1] * df2[column]


    print(df3.iloc[0])
    values = df2.values.flatten()
    img = io.BytesIO()
    fig, ax = plt.subplots()
    sns.set_style("darkgrid")

    ax = sns.barplot(x= df2.columns,y=values)


    df = pd.DataFrame(allocation, index=[0])
    for price in latest_prices:
        print(price)
        print(df.index)
        if price in df:
            df['total_value'] = price * df

    values = df.values.flatten()
    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(14,10), dpi=120)
    sns.set_style("darkgrid")
    print(df)

    ax = sns.barplot(x= df.columns,y=values)
    #ax = df.plot(kind="bar", stacked=False)
    ax.set(xlabel="")
    plt.savefig(img, format='png')

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())

    fig2, ax2 = plt.subplots(figsize=(6,6), dpi=50)
    img2 = io.BytesIO()
    sns.set_style("darkgrid")

    ax2 = plt.pie(df3.iloc[0], labels=df3.columns, autopct='%.0f%%', pctdistance=0.4, labeldistance=0.5, rotatelabels=False)
    plt.savefig(img2, format='png')
    img2.seek(0)
    plot_url_2 = base64.b64encode(img2.getvalue())

    df3 = df3.reset_index(drop=True)
    df3 = dict(df3.to_dict('list'))

    for k, v in df3.items():
        print(v[0])
        df3[k] = np.array(v[0])

    return plot_url_2, allocation, df2, df3, leftover, missing_data

def adapt_risk(risk):
    if risk:
        risk = float(risk)
        if risk > 1:
            risk = risk / 100
        else:
            risk = risk

    return risk






