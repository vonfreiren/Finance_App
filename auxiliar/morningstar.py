import requests
from bs4 import BeautifulSoup

from auxiliar.equivalence_map import dictOfExchangesMorningStar, dictOfExchangesMorningStar_US


def calculate_morning(ticker, market, exchange):
    morningstar_info = []
    country = market[:2]
    clean_ticker = ticker.split('.')[0]
    if is_american_exchange(country):
        exchange = retrieve_american_exchange_morningstart(exchange)
    else:
        exchange = dictOfExchangesMorningStar[country]


    url = 'https://www.morningstar.com/etfs/{0}/{1}/portfolio/'.format(exchange, clean_ticker)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        stars = soup.find("span", {"class": 'mdc-security-header__star-rating'}, href=False).attrs['title']
    except:
        stars = None
    morningstar_info.append(stars)
    return morningstar_info



def calculate_risk(ticker, market, exchange):
    morningstar_info = []
    country = market[:2]
    clean_ticker = ticker.split('.')[0]
    if is_american_exchange(country):
        exchange = retrieve_american_exchange_morningstart(exchange)
    else:
        exchange = dictOfExchangesMorningStar[country]


    url = 'https://www.morningstar.com/etfs/{0}/{1}/risk/'.format(exchange, clean_ticker)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        expenses = soup.find("span", {"class": 'mdc-security-header__star-rating'}, href=False).attrs['title']
    except:
        expenses = None
    morningstar_info.append(expenses)
    return morningstar_info




def is_american_exchange(country):
    return country == 'us'

def retrieve_american_exchange_morningstart(exchange):
    return dictOfExchangesMorningStar_US[exchange]


