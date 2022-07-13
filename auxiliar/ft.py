import requests
from bs4 import BeautifulSoup
import pandas as pd
from auxiliar.equivalence_map import dictOfExchanges, equities, etfs, dictOfUSExchanges


def calculate_ft(ticker, asset_type, exchange, market, currency):
    holdings_list = []
    zones_list = []
    dict_zones = {}

    if(asset_type == 'EQUITY'):
        asset_type = equities

    if(asset_type.lower() in etfs):
        asset_type = etfs

    inv_dictOfExchanges = {v: k for k, v in dictOfExchanges.items()}

    if '.' in ticker:
        replace_value = inv_dictOfExchanges.get(ticker[-3:])
        if replace_value:
            exchange = replace_value
            ticker = ticker.replace(ticker[-3:], replace_value)


    if(asset_type == equities):
        holdings_list = calculate_profile(ticker, exchange, asset_type)
    if(asset_type == etfs):
        holdings_list = calculate_holdings(holdings_list, dict_zones, ticker, exchange, asset_type, currency)
        stars = calculate_ratings(ticker, exchange, asset_type, currency)

    return holdings_list, stars


def calculate_ratings(ticker, exchange, asset_type, currency):
    if ':' not in ticker:
        ticker = ticker+':'+dictOfUSExchanges[exchange]
    api_url = 'https://markets.ft.com/data/{0}/tearsheet/ratings?s={1}:{2}'.format(asset_type, ticker,
                                                                                        currency)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(api_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        stars = len(soup.find('span', attrs={'data-mod-stars-highlighted': True}).findChildren("i", recursive=False))
    except:
        stars = None
    return stars

def calculate_holdings(holdings_list, dict_zones, ticker, exchange, asset_type, currency):
    holdings_list = []
    weights_list = []
    if ':' not in ticker:
        ticker = ticker+':'+dictOfUSExchanges[exchange]
    api_url = 'https://markets.ft.com/data/{0}/tearsheet/holdings?s={1}:{2}'.format(asset_type, ticker,
                                                                                        currency)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(api_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    top_holdings = soup.find_all("span", {"class": "mod-ui-table__cell__disclaimer"})
    for symbol in top_holdings:
        holdings_list.append(symbol.text + "-")
    percentages = soup.find_all("td", {"class": "mod-top-ten__holdings-row-allocation"})
    for counter, percentage in enumerate(percentages):
        weight = percentage.find_previous()
        weights_list.append(weight.text)

    zones = soup.find_all("span", {"class": "mod-ui-table__cell--colored__wrapper"})
    for zone in zones:
        value = zone.find_next().text
        if ('%' in value):
            dict_zones[zone.text] = value

    holdings_list = ammend_tickers(holdings_list)
    weights_list = weights_list[:len(holdings_list)]
    data_tuples = list(zip(holdings_list, weights_list))
    balance_sheet = pd.DataFrame(data_tuples, columns=['Company', 'Allocation'])

    return balance_sheet

def ammend_tickers(holdings_list):
    new_holding_list = []
    for holding in holdings_list:
        ticker = holding.split(':')[-1][:3]
        if ticker in dictOfUSExchanges.keys():
            holding = holding.split(':')[0]
            new_holding_list.append(holding)
        else:
            exchange = holding[-5:].replace('-', '')
            replace_value = dictOfExchanges.get(exchange)
            if replace_value:
                holding = holding.replace(exchange, replace_value)
            new_holding_list.append(holding.split('-')[0])

    return new_holding_list


# summary
def calculate_summary(holdings_list, dict_zones, ticker, exchange, asset_type, currency):
    URL = 'https://markets.ft.com/data/{0}/tearsheet/summary?s={1}:{2}:{3}'.format(asset_type, ticker, exchange,
                                                                                   currency)
    URL1 = 'https://markets.ft.com/data/'
    URL2 = '/tearsheet/summary?s='
    separator = ':'

    main_url = 'https://markets.ft.com/data/{asset_type}/tearsheet/summary?s={ticker}:{exchange}:{currency}'
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


def calculate_profile(ticker, exchange, asset_type):
    url = 'https://markets.ft.com/data/{0}/tearsheet/profile?s={1}'.format(asset_type, ticker)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    new_holdings_list = []
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    table_rows = soup.find_all("a", {"class": 'mod-ui-link'}, href=True)
    for row in table_rows:
        if 'mod-peer-analysis' in str(row):
            name = row.text
            ticker = row['href'].split('=')[-1]
            if '.' in ticker:
                ticker = ticker.replace(ticker[ticker.find('.')], '')
            if ':' in ticker:
                replace_value = dictOfExchanges.get(ticker[-4:])
                if replace_value:
                    ticker = ticker.replace(ticker[-4:], replace_value)
                    print(ticker)
                    new_holdings_list.append(ticker)
    return new_holdings_list


