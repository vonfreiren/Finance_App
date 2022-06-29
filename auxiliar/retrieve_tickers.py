import re

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
from yahoo_fin import stock_info as si
from feed_security_data import preDownloadSecurityDB
import requests
import csv
key = '9cca38e250e53fef2e85451e0c20c562'


def fetch_symbols_australia():
    australia_list =[]
    url = 'http://api.marketstack.com/v1/exchanges/XASX/tickers?access_key='+key
    result = requests.get(url).text
    results = re.split('"symbol":', result)
    for i, line in enumerate(results):
        if(i!=0):
            australia_list.append(line.split(',')[0][1:-1].replace('XASX', 'AX'))

    with open('../tickers/australia.csv', 'w', newline='') as file:
        write = csv.writer(file)
        write.writerows([australia_list])

def fetch_symbols_korea():
    korea_list=[]
    url = 'http://api.marketstack.com/v1/exchanges/XKRX/tickers?access_key='+key
    result = requests.get(url).text
    results = re.split('"symbol":', result)
    for i, line in enumerate(results):
        if(i!=0):
            korea_list.append(line.split(',')[0][1:-1].replace('XKRX', 'KS'))

    with open('../tickers/korea.csv', 'w', newline='') as file:
        write = csv.writer(file)
        write.writerows([korea_list])

def fetch_symbols_hsi():
    hsi_list=[]
    url = 'http://api.marketstack.com/v1/exchanges/XHKG/tickers?access_key='+key
    result = requests.get(url).text
    results = re.split('"symbol":', result)
    for i, line in enumerate(results):
        if(i!=0):
            hsi_list.append(line.split(',')[0][1:-1].replace('XHKG', 'HK'))

    with open('../tickers/hsi.csv', 'w', newline='') as file:
        write = csv.writer(file)
        write.writerows([hsi_list])

def fetch_symbols_japan():
    japan_list = []
    url_1 = 'http://api.marketstack.com/v1/exchanges/XFKA/tickers?access_key='+key
    url_2 = 'http://api.marketstack.com/v1/exchanges/XTKS/tickers?access_key='+key
    url_3 = 'http://api.marketstack.com/v1/exchanges/XNGO/tickers?access_key='+key
    url_4 = 'http://api.marketstack.com/v1/exchanges/XSAP/tickers?access_key='+key
    url_list = [url_1, url_2, url_3, url_4]
    for counter, url in enumerate(url_list):
        result = requests.get(url).text
        results = re.split('"symbol":', result)
        for i, line in enumerate(results):
            if(i!=0):
                replaceString = ""
                if counter==0:
                    replaceString = 'XFKA'
                if counter == 1:
                    replaceString = 'XTKS'
                if counter == 2:
                    replaceString = 'XNGO'
                if counter == 3:
                    replaceString = 'XSAP'
                japan_list.append(line.split(',')[0][1:-1].replace(replaceString, 'T'))

        with open('../tickers/japan.csv', 'w', newline='') as file:
            write = csv.writer(file)
            write.writerows([japan_list])


def fetch_symbols_china():
    china_list = []
    key = '9cca38e250e53fef2e85451e0c20c562'
    url_1 = 'http://api.marketstack.com/v1/exchanges/XSHE/tickers?access_key='+key
    url_2 = 'http://api.marketstack.com/v1/exchanges/XSHG/tickers?access_key='+key
    url_list = [url_1, url_2]
    for counter, url in enumerate(url_list):
        result = requests.get(url).text
        results = re.split('"symbol":', result)
        for i, line in enumerate(results):
            if(i!=0):
                replaceString = ""
                if counter==0:
                    replaceString = 'XSHE'
                    new_string = 'SZ'
                if counter == 1:
                    replaceString = 'XSHG'
                    new_string = 'SS'
                china_list.append(line.split(',')[0][1:-1].replace(replaceString, new_string))

        with open('../tickers/china.csv', 'w', newline='') as file:
            write = csv.writer(file)
            write.writerows([china_list])

#fetch_symbols_australia()
#fetch_symbols_korea()
#fetch_symbols_japan()
#fetch_symbols_hsi()
#fetch_symbols_china()