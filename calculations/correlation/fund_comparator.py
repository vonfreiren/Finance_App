from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import yfinance as yf
from GoogleNews import GoogleNews
from dateutil.relativedelta import relativedelta
from sklearn.metrics import r2_score

from auxiliar.constants import RISK_FREE_RATE, TRADING_DAYS
from auxiliar.feed_security_data import retrieveFunds, retrieveSecurityDB, preDownloadSecurityDB
from auxiliar.ft import calculate_ft
from auxiliar.retrieve_balance_sheet import retrieve_balance_sheet
from auxiliar.retrieve_company_info import retrieve_info
from auxiliar.yahoo import calculate_expense_ratio
from auxiliar.google import retrieve_isin

def calculate_funds(asset):
    df = pd.DataFrame()
    data = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    end_date = end_date

    price = 0
    last_change = 0
    last_pct_change = 0
    price_last_year = 0
    funds_list = []
    portfolio = []
    name_list = []
    performance_info = []
    balance_sheet = None
    morning_info = None
    financial_info = []
    company_info = []
    beta = None
    stars = None
    alpha = None
    r_squared = None
    yahoo_info = []

    start_date = datetime.today() - relativedelta(years=3)
    start_date = start_date.strftime('%Y-%m-%d')
    missingData = False
    data = yf.download(asset, start_date, end_date)
    if data.empty:
        return missingData, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    name, asset_type, exchange, market, currency, isin = preDownloadSecurityDB(asset)
    if asset_type == 'EQUITY':
        funds_list, stars, alpha, beta, r_squared = calculate_ft(asset, asset_type, exchange, market, currency, name)
        funds_list.append(asset)
        funds_list = list(set(funds_list))
        funds_list.remove(asset)
        funds_list.insert(0, asset)
    else:
        if asset_type == 'ETF' or asset_type == 'MUTUALFUND':
            balance_sheet, stars, alpha, beta, r_squared = calculate_ft(asset, asset_type, exchange, market, currency, name)
            funds_list.append(asset)
            #funds_list = funds_list + retrieveFunds()
            funds_list = list(set(funds_list))
            funds_list.remove(asset)
            funds_list.insert(0, asset)
        else:
            funds_list.append(asset)


    for fund in funds_list:
        fund = str(fund).strip("()").replace(',', '')
        data = yf.download(fund, start_date, end_date)
        data['pct_change'] = data['Close'].pct_change()
        if data.empty:
            continue
            missingData = True

        data = data.round(3)
        if fund == asset:
            yahoo_info = calculate_expense_ratio(asset)
            data['change'] = np.log(data['Close'] / data['Close'].shift())
            portfolio = data['Close'].values.tolist()
            name_list = pd.to_datetime(data.index).strftime('%Y-%m-%d').tolist()
            list_news = retrieveNews(name)
            price = yf.Ticker(asset).get_info()['regularMarketPrice']
            last_price = data['Close'][-1]
            # IF the latest price is loaded, we take the one before that
            if last_price == price:
                last_price = data['Close'][-2]
            last_change = price - last_price
            last_pct_change = (price - last_price) / last_price * 100
            try:
                price_last_year = data['Close'][-255]
            except:
                price_last_year = data['Close'][0]
            change_last_year = (price - price_last_year) / price_last_year * 100

            last_change = round(last_change, 3)
            last_pct_change = round(last_pct_change, 3)
            change_last_year = round(change_last_year, 3)

            if asset_type == 'EQUITY':
                balance_sheet = retrieve_balance_sheet(asset)
                company_info, financial_info = retrieve_info(asset)


        security = retrieveSecurityDB(fund)
        if (security is not None):
            fund = security.name
            isin_info = retrieve_isin(fund)


        start_price = data.Close[0]
        end_price = data.Close[-1]
        return_3 = (end_price - start_price) / start_price * 100 / 3

        expected_return, standard_deviation, sharpe_ratio = calculate_sharpe_ratio(data)
        sortino_ratio = calculate_sortino_ratio(data, expected_return)
        max_dd, max_dd_date = calculate_max_drawdown(data)
        calmar_ratio = calculate_calmar_ratio(data, max_dd)
        if beta:
            treynor_ratio = calculate_treynor_ratio(data, beta)
        else:
            treynor_ratio = None


        df2 = pd.DataFrame({'Return_3': expected_return, 'Std_3': standard_deviation}, index=[fund])
        performance_info.append(sharpe_ratio)
        performance_info.append(sortino_ratio)
        performance_info.append(max_dd)
        performance_info.append(max_dd_date)
        performance_info.append(calmar_ratio)
        performance_info.append(treynor_ratio)
        financial_info.append(stars)
        financial_info.append(alpha)
        financial_info.append(beta)
        financial_info.append(r_squared)
        financial_info.append(yahoo_info[0])
        df = df.append(df2, ignore_index=False)
    security = retrieveSecurityDB(asset)
    if (security is not None):
        asset = security.name

    #sharpe_ratio = df.loc[asset].Return_3 / df.loc[asset].Std_3

    values_list = []
    labels_list = []
    df = df.round(2)
    for idx, row in df.iterrows():
        d = {'x': row['Return_3']}
        d['y'] = row['Std_3']
        d['z'] = idx
        labels_list.append(idx)
        values_list.append(d)

    return missingData,asset_type, asset, return_3, standard_deviation, values_list, labels_list, price, currency, price_last_year, last_change, last_pct_change, change_last_year, list_news, company_info, financial_info, portfolio, name_list, balance_sheet, performance_info


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


def calculate_r_squared(asset, start_date, end_date):
    index = yf.download('VOO', start_date, end_date)
    correlation_matrix = np.corrcoef(asset['Close'], index['Close'])

    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy ** 2
    r_squated_2 = r2_score(asset['Close'], index['Close'])
    asset['QQQ'] = np.log(asset['Adj Close'] / asset['Adj Close'].shift(1))
    index['VOO'] = np.log(index['Adj Close'] / index['Adj Close'].shift(1))

    df = pd.concat([asset['QQQ'], index['VOO']], axis=1).dropna()
    slr_sm_model = smf.ols('QQQ ~ VOO', data=df)
    slr_sm_model_ko = slr_sm_model.fit()
    print(slr_sm_model_ko.summary())
    param_slr = slr_sm_model_ko.params

    return r_squared


def calculate_sharpe_ratio(data):
    expected_return = (data['pct_change'].mean() * TRADING_DAYS - RISK_FREE_RATE) * 100
    standard_deviation = ((data['pct_change'].std()) * np.sqrt(TRADING_DAYS)) * 100
    sharpe_ratio = (expected_return - RISK_FREE_RATE) / standard_deviation
    return round(expected_return, 3), round(standard_deviation, 3), round(sharpe_ratio, 3)


def calculate_sortino_ratio(data, expected_return):
    is_negative = data['pct_change'] < 0
    standard_deviation_negative = ((data[is_negative]['pct_change'].std()) * np.sqrt(TRADING_DAYS)) * 100
    sortino_ratio = (expected_return - RISK_FREE_RATE) / standard_deviation_negative
    return round(sortino_ratio, 3)


def calculate_max_drawdown(data):
    comp_ret = (data['pct_change'] + 1).cumprod()
    peak = comp_ret.expanding(min_periods=1).max()
    dd = (comp_ret / peak) - 1
    max_dd = abs(dd.min())
    return round(max_dd, 3), (dd.idxmin()- relativedelta(days=1)).strftime('%Y-%m-%d')


def calculate_calmar_ratio(data, max_drawdown):
    expected_return = (data['pct_change'].mean()) * 255
    calmar_ratio = expected_return / max_drawdown
    return round(calmar_ratio, 3)


def calculate_treynor_ratio(data, beta):
    expected_return = (data['pct_change'].mean()) * 255
    expected_return = expected_return - RISK_FREE_RATE
    treynor_ratio = expected_return / float(beta)
    return round(treynor_ratio, 3)

