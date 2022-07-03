import requests
from bs4 import BeautifulSoup


def calculate_ft():
    holdings_list = []
    zones_list = []
    dict_zones = {}

    ticker = 'BBVA'
    exchange = 'MCE'
    currency = 'EUR'
    asset_type = 'equities'

    calculate_profile(holdings_list, dict_zones, ticker, exchange, asset_type, currency)


def calculate_holdings(holdings_list, dict_zones, ticker, exchange, asset_type, currency):
    api_url = 'https://markets.ft.com/data/{0}/tearsheet/holdings?s={1}:{2}:{3}'.format(asset_type, ticker, exchange,
                                                                                        currency)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(api_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    top_holdings = soup.find_all("span", {"class": "mod-ui-table__cell__disclaimer"})
    for symbol in top_holdings:
        holdings_list.append(symbol.text + "-")
    zones = soup.find_all("span", {"class": "mod-ui-table__cell--colored__wrapper"})
    for zone in zones:
        value = zone.find_next().text
        if ('%' in value):
            dict_zones[zone.text] = value

    return holdings_list, dict_zones


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
    url = 'https://markets.ft.com/data/{0}/tearsheet/profile?s={1}:{2}'.format(asset_type, ticker, exchange)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    table_rows = soup.find_all("a", {"class": 'mod-ui-link'}, href=True)
    for row in table_rows:
        if 'mod-peer-analysis' in str(row):
            name = row.text
            ticker = row['href'].split('=')[-1]
            print(ticker)

    return None
