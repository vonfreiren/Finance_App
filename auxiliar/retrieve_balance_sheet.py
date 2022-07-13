import yfinance as yf
import pandas as pd
from datetime import datetime


def retrieve_balance_sheet(ticker):
    company_info = []
    financial_info = []
    last_balance_sheet = pd.DataFrame()
    pd.options.display.float_format = '{:,.2f}'.format

    data_2 = yf.Ticker(ticker).get_balancesheet()
    last_balance_sheet[datetime.strftime(data_2.columns[0], '%Y-%m-%d')] = data_2.iloc[:,0]
    last_balance_sheet[datetime.strftime(data_2.columns[1], '%Y-%m-%d')] = data_2.iloc[:,1]
    last_balance_sheet['Change'] = data_2.iloc[:,0] - data_2.iloc[:,1]
    last_balance_sheet.style.format({'Change': "{0:+g}"})
    last_balance_sheet.insert(0, 'Concept', data_2.index.values)

    return last_balance_sheet


