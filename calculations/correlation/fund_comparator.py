import matplotlib
import pandas as pd
import yfinance as yf
import numpy as np

from auxiliar.constants import RISK_FREE_RATE
from auxiliar.ft import calculate_profile, calculate_ft, calculate_ratings

from datetime import datetime
from dateutil.relativedelta import relativedelta
from GoogleNews import GoogleNews

import seaborn as sns
from auxiliar.feed_security_data import retrieveFunds, retrieveSecurityDB, preDownloadSecurityDB
from auxiliar.morningstar import calculate_morning
from auxiliar.retrieve_company_info import retrieve_info
from auxiliar.retrieve_balance_sheet import retrieve_balance_sheet
from sklearn.metrics import r2_score
import statsmodels.formula.api as smf


def calculate_funds(asset):
    df = pd.DataFrame()
    data = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    end_date = end_date
    end_date = '2022-06-30'

    price = 0
    last_change = 0
    last_pct_change = 0
    price_last_year = 0
    funds_list = []
    portfolio = []
    name_list = []
    balance_sheet = None
    morning_info = None

    start_date = datetime.today() - relativedelta(years=3)
    start_date = start_date.strftime('%Y-%m-%d')
    start_date = '2019-06-30'
    missingData = False
    data = yf.download(asset, start_date, end_date)
    if data.empty:
        return missingData, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    name, asset_type, exchange, market, currency = preDownloadSecurityDB(asset)
    if asset_type == 'EQUITY':
        funds_list, stars = calculate_ft(asset, asset_type, exchange, market, currency)
        funds_list.append(asset)
        funds_list = list(set(funds_list))
        funds_list.remove(asset)
        funds_list.insert(0, asset)
    else:
        if asset_type == 'ETF':
            balance_sheet, stars = calculate_ft(asset, asset_type, exchange, market, currency)
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

        data = data.round(3)
        if fund == asset:
            portfolio = data['Close'].values.tolist()
            name_list = pd.to_datetime(data.index).strftime('%Y-%m-%d').tolist()
            list_news = retrieveNews(name)
            price = yf.Ticker(asset).get_info()['regularMarketPrice']
            last_price = data['Close'][-1]
            #IF the latest price is loaded, we take the one before that
            if last_price == price:
                last_price = data['Close'][-2]
            last_change = price - last_price
            last_pct_change = (price - last_price)/last_price * 100
            price_last_year = data['Close'][-255]
            change_last_year = (price - price_last_year)/price_last_year * 100

            last_change = round(last_change, 3)
            last_pct_change = round(last_pct_change, 3)
            change_last_year = round(change_last_year, 3)

            if asset_type == 'EQUITY':
                balance_sheet = retrieve_balance_sheet(asset)
            company_info, financial_info = retrieve_info(asset)

            financial_info.append(stars)

        security = retrieveSecurityDB(fund)
        if (security is not None):
            fund = security.name


        start_price = data.Close[0]
        end_price = data.Close[-1]
        return_3 = (end_price - start_price) / start_price * 100 / 3 - RISK_FREE_RATE
        std_3 = (data['Close'].std() / 3) - 1
        df2 = pd.DataFrame({'Return_3': return_3, 'Std_3': std_3}, index=[fund])
        df = df.append(df2, ignore_index=False)
    security = retrieveSecurityDB(asset)
    if (security is not None):
        asset = security.name

    sharpe_ratio = df.loc[asset].Return_3/ df.loc[asset].Std_3


    values_list = []
    labels_list = []
    df = df.round(2)
    for idx, row in df.iterrows():
        d = {'x': row['Return_3']}
        d['y'] = row['Std_3']
        d['z'] = idx
        labels_list.append(idx)
        values_list.append(d)


    return missingData, asset, return_3, std_3, values_list, labels_list, price, currency, price_last_year, last_change, last_pct_change, change_last_year, list_news, company_info, financial_info, portfolio, name_list, balance_sheet


def retrieveNews(ticker):
    news = GoogleNews(period='1w')
    news.search(ticker)
    result = news.result()
    data = pd.DataFrame.from_dict(result)
    list_news = []

    for idx, row in data.iterrows():
        single_new = [row['title'], row['media'], row['date'], row['link']]
        list_news.append(single_new)

    data.head()
    return list_news


def r_squared(asset, start_date, end_date):
    index = yf.download('VOO', start_date, end_date)
    correlation_matrix = np.corrcoef(asset['Close'], index['Close'])

    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy ** 2
    r_squated_2 = r2_score(asset['Close'], index['Close'])
    asset['QQQ'] =  np.log(asset['Adj Close'] / asset['Adj Close'].shift(1))
    index['VOO'] =  np.log(index['Adj Close'] / index['Adj Close'].shift(1))

    df = pd.concat([asset['QQQ'], index['VOO']], axis=1).dropna()
    slr_sm_model = smf.ols('QQQ ~ VOO', data=df)
    slr_sm_model_ko = slr_sm_model.fit()
    print(slr_sm_model_ko.summary())
    param_slr = slr_sm_model_ko.params

    return r_squared


