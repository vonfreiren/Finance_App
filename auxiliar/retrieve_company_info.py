import yfinance as yf


def retrieve_info(ticker):
    company_info = []
    financial_info = []

    data_2 = yf.Ticker(ticker).get_info()
    summary = data_2['longBusinessSummary']
    sector = data_2['sector']
    industry = data_2['industry']
    country = data_2['country']
    website = data_2['website']
    exchange_2 = data_2['exchange']

    company_info.append(summary)
    company_info.append(sector)
    company_info.append(industry)
    company_info.append(country)
    company_info.append(website)
    company_info.append(exchange_2)

    eps = data_2['trailingEps']
    currentPrice = data_2['currentPrice']
    pe = round(currentPrice / eps, 3)
    debt_equity_ratio = data_2['debtToEquity']
    beta = data_2['beta']

    financial_info.append(eps)
    financial_info.append(currentPrice)
    financial_info.append(pe)
    financial_info.append(debt_equity_ratio)
    financial_info.append(beta)

    return company_info, financial_info



    ret