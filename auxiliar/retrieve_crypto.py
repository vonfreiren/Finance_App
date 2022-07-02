import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
import yfinance as yf
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from crypto.api import CoinGeckoAPI
def retrieve_crypto():
    cryptoList = []

    df = pd.DataFrame()
    coins = CoinGeckoAPI().get_coins()
    changes = {}
    for coin in coins:
        print (coin['name'])
        id = coin['id']
        symbol = coin['symbol']
        values = CoinGeckoAPI().get_coin_market_chart_by_id(id, 'usd', 1)
        current_price = values['prices'][-1][-1]
        price_yesterday = values['prices'][0][-1]
        change = (current_price - price_yesterday) / price_yesterday * 100
        changes[symbol] = change
    currency = 'USD'
    URL = 'https://coinmarketcap.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    crypto_symbols = soup.find_all("span", {"class": "crypto-symbol"})
    for symbol in crypto_symbols:
        cryptoList.append(symbol.text+"-"+currency)
    for span in crypto_symbols:
        price = span.find_next("span").text
        print(price)
    return cryptoList


retrieve_crypto()