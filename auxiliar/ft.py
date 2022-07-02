

from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
import yfinance as yf
import requests
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import re
def retrieve_crypto():
    holdings_list = []
    zones_list = []
    dict_zones = {}

    ticker='VEUR'
    exchange='AEX'
    currency = 'EUR'
    asset_type = 'etfs'

    calculate_holdings(holdings_list, dict_zones, ticker, exchange, asset_type, currency)









    #holdings
def calculate_holdings(holdings_list, dict_zones, ticker, exchange, asset_type, currency):
    api_url = 'https://markets.ft.com/data/{0}/tearsheet/holdings?s={1}:{2}:{3}'.format(asset_type, ticker, exchange, currency)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(api_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    top_holdings = soup.find_all("span", {"class": "mod-ui-table__cell__disclaimer"})
    for symbol in top_holdings:
        holdings_list.append(symbol.text+"-")
    zones = soup.find_all("span", {"class": "mod-ui-table__cell--colored__wrapper"})
    for zone in zones:
        value = zone.find_next().text
        if('%' in value):
            dict_zones[zone.text] = value

    return holdings_list, dict_zones

# summary
def calculate_summary(holdings_list, dict_zones, ticker, exchange, asset_type, currency):
    URL = 'https://markets.ft.com/data/etfs/tearsheet/summary?s=VUSA:AEX:EUR'
    URL1 = 'https://markets.ft.com/data/'
    URL2 = '/tearsheet/summary?s='
    separator = ':'

    main_url = 'https://markets.ft.com/data/{asset_type}/tearsheet/summary?s={ticker}:{exchange}:{currency}'

    main_url = URL1 + asset_type + URL2 + ticker + separator + exchange + separator + currency
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    table_rows = soup.find_all("th")
    for row in table_rows:
        if "ISIN" in row:
            isin = row.find_next().text
            return isin

    return None

retrieve_crypto()