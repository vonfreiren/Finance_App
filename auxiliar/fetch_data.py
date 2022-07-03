from datetime import datetime, timedelta

import matplotlib
import pandas as pd
import yfinance as yf

matplotlib.use('Agg')
from yahoo_fin import stock_info as si
from feed_security_data import preDownloadSecurityDB
from parse_csv_tickers import parse_csv_symbols_country
from retrieve_crypto import retrieve_crypto

df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
df4 = pd.DataFrame()
df5 = pd.DataFrame()
df6 = pd.DataFrame()
df7 = pd.DataFrame()
df8 = pd.DataFrame()
df9 = pd.DataFrame()
df10 = pd.DataFrame()
df11 = pd.DataFrame()
df12 = pd.DataFrame()
df13 = pd.DataFrame()
df14 = pd.DataFrame()
df15 = pd.DataFrame()
df16 = pd.DataFrame()
df17 = pd.DataFrame()
df18 = pd.DataFrame()
df19 = pd.DataFrame()


def fetch_symbols():
    start_date = datetime.today() - timedelta(3)
    yesterday = datetime.today() - timedelta(1)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')

    try:
        df1 = pd.read_pickle('../tickers/sp500')
    except:
        df1 = pd.DataFrame(si.tickers_sp500())
        df1.to_pickle('tickers/sp500')

    try:
        df2 = pd.read_pickle('../tickers/nasdaq')
    except:
        df2 = pd.DataFrame(si.tickers_nasdaq())
        df2.to_pickle('tickers/nasdaq')

    try:
        df3 = pd.read_pickle('../tickers/dow')
    except:
        df3 = pd.DataFrame(si.tickers_dow())
        df3.to_pickle('tickers/dow')

    try:
        df4 = pd.read_pickle('../tickers/others')
    except:
        df4 = pd.DataFrame(si.tickers_other())
        df4.to_pickle('tickers/others')

    try:
        df5 = pd.read_pickle('../tickers/ibex35')
    except:
        df5 = pd.DataFrame(si.tickers_ibex35())
        df5.to_pickle('tickers/ibex35')

    try:
        df6 = pd.read_pickle('../tickers/cac40')
    except:
        df6 = pd.DataFrame(si.tickers_cac40())
        df6.to_pickle('tickers/cac40')
    try:
        df7 = pd.read_pickle('../tickers/cac40')
    except:
        df7 = pd.DataFrame(si.tickers_ftse_100())
        df7.to_pickle('tickers/ftse')

    try:
        df8 = pd.read_pickle('../tickers/dax')
    except:
        df8 = pd.DataFrame(si.tickers_dax())
        df8.to_pickle('tickers/dax')

    try:
        df9 = pd.read_pickle('../tickers/psi')
    except:
        df9 = pd.DataFrame(si.tickers_psi_20())
        df9.to_pickle('tickers/psi')

    try:
        df10 = pd.read_pickle('../tickers/milan')
    except:
        df10 = pd.DataFrame(si.tickers_ftse_milan())
        df10.to_pickle('tickers/milan')

    try:
        df11 = pd.read_pickle('../tickers/brazil')
    except:
        df11 = pd.DataFrame(si.tickers_ibovespa())
        df11.to_pickle('tickers/brazil')

    try:
        df12 = pd.read_pickle('../tickers/swiss')
    except:
        df12 = pd.DataFrame(si.tickers_swiss())
        df12.to_pickle('tickers/swiss')

    try:
        df13 = pd.read_pickle('../tickers/india')
    except:
        df13 = pd.DataFrame(si.tickers_nifty50())
        df13.to_pickle('tickers/india')

    try:
        df14 = pd.read_pickle('../tickers/china')
    except:
        df14 = pd.DataFrame(parse_csv_symbols_country('tickers/china'))
        df14.to_pickle('tickers/china')

    try:
        df15 = pd.read_pickle('../tickers/japan')
    except:
        df15 = pd.DataFrame(parse_csv_symbols_country('tickers/japan'))
        df15.to_pickle('tickers/japan')

    try:
        df16 = pd.read_pickle('../tickers/australia')
    except:
        df16 = pd.DataFrame(parse_csv_symbols_country('tickers/australia'))
        df16.to_pickle('tickers/australia')

    try:
        df17 = pd.read_pickle('../tickers/korea')
    except:
        df17 = pd.DataFrame(parse_csv_symbols_country('tickers/korea'))
        df17.to_pickle('tickers/korea')

    try:
        df18 = pd.read_pickle('../tickers/hsi')
    except:
        df18 = pd.DataFrame(parse_csv_symbols_country('tickers/hsi'))
        df18.to_pickle('tickers/hsi')

    try:
        df19 = pd.read_pickle('../tickers/crypto')
    except:
        df19 = pd.DataFrame(retrieve_crypto())
        df19.to_pickle('tickers/crypto')

    calculate_differences(df19)


def calculate_differences(df):
    start_date = datetime.today() - timedelta(4)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    df2 = pd.DataFrame(columns=['Difference'])
    for symbol in df.values.tolist():
        a = datetime.now()
        symbol = str(symbol)[2:-2]
        data = yf.download(symbol, start_date, end_date, interval="1h")
        if data.empty:
            print("No data for " + symbol)
        else:
            try:
                previous_day = pd.to_datetime(data.index[-1]).to_pydatetime() - timedelta(1)
                name = preDownloadSecurityDB(symbol)
                price_now = data['Close'][-1]
                previous_day_str = previous_day.strftime('%Y-%m-%d')
                price_previous_day = data.loc[start_date:previous_day_str]['Close'][-1]
                difference = (price_now - price_previous_day) / price_previous_day * 100
                df2.loc[name] = [difference]
                b = datetime.now()
                delta = b - a
                print(delta.total_seconds())
            except:
                print("No data found for " + symbol)
    return df2


fetch_symbols()
