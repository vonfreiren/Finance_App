import matplotlib

matplotlib.use('Agg')
import csv


def parse_csv_symbols_country(name):
    ticker_list = []
    with open(name + '.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

        for ticker in data:
            for tick in ticker:
                ticker_list.append(tick)

        print(ticker_list)
    return ticker_list
