import requests
from bs4 import BeautifulSoup
import re

from auxiliar.equivalence_map import dictOfExchangesMorningStar, dictOfExchangesMorningStar_US




def calculate_expense_ratio(ticker):
    yahoo_info = []
    expense_ratio = ''


    url = 'https://finance.yahoo.com/quote/{0}'.format(ticker)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        text = 'Expense Ratio'
        soup = BeautifulSoup(page.content, "html.parser")

        counter_found = False
        tds = soup.find_all('td')
        for t in tds:
            if text in t.text:
                expense_ratio = t.find_next().find_next().text
    except:
        expense_ratio = None
    yahoo_info.append(expense_ratio)
    return yahoo_info
