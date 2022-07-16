import requests
from bs4 import BeautifulSoup
import re

from auxiliar.equivalence_map import dictOfExchangesMorningStar, dictOfExchangesMorningStar_US




def retrieve_isin(name):
    yahoo_info = []

    url = "https://www.google.com/search"
    params = {"q": name+" isin"}  # add "hl":"en" to get english results
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    soup = BeautifulSoup(
        requests.get(url, params=params, headers=headers).content, "html.parser"
    )
    try:
        isins = re.findall('([A-Z]{2}[0-9]{1}[A-Z0-9]{9})', soup.text)
        isin = max(set(isins), key = isins.count)
    except:
        isin = ""

    yahoo_info.append(isin)
    print(isin)
    print(name)
    return yahoo_info
