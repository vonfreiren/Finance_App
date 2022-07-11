import yfinance as yf


def retrieve_info(ticker):
    company_info = []
    financial_info = []

    data_2 = yf.Ticker(ticker).get_info()
    summary = data_2['longBusinessSummary'] if 'longBusinessSummary' in data_2 else None
    sector = data_2['sector'] if 'sector' in data_2 else None
    industry = data_2['industry'] if 'industry' in data_2 else None
    country = data_2['country'] if 'country' in data_2 else None
    website = data_2['website'] if 'website' in data_2 else None
    exchange_2 = data_2['exchange'] if 'exchange' in data_2 else None

    company_info.append(summary)
    company_info.append(sector)
    company_info.append(industry)
    company_info.append(country)
    company_info.append(website)
    company_info.append(exchange_2)

    eps = data_2['trailingEps'] if 'trailingEps' in data_2 else None
    currentPrice = data_2['currentPrice'] if 'currentPrice' in data_2 else None
    pe = None
    if eps:
        pe = round(currentPrice / eps, 3)
    debt_equity_ratio = data_2['debtToEquity'] if 'debtToEquity' in data_2 else None
    beta = data_2['beta'] if 'beta' in data_2 else None

    financial_info.append(eps)
    financial_info.append(currentPrice)
    financial_info.append(pe)
    financial_info.append(debt_equity_ratio)
    financial_info.append(beta)

    return company_info, financial_info


