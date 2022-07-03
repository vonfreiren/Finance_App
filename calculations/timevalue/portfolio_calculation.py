import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
import seaborn as sns
from auxiliar.feed_security_data import preDownloadSecurityDB


def calculate_portfolio(assetList, weightList, initialValue, startDate):
    img = io.BytesIO()
    df = pd.DataFrame()
    data = pd.DataFrame()
    endDate = datetime.today().strftime('%Y-%m-%d')
    weightList = [float(i) for i in weightList]
    name = ""

    wrong_weights = sum(weightList) != 1
    missing_data = False

    for asset in assetList:
        data = yf.download(asset, startDate, endDate)
        if data.empty:
            missing_data = True
            return None, None, missing_data, wrong_weights, None, None
        name = preDownloadSecurityDB(asset)
        df[name] = data['Close']

    df = df.ffill().bfill()
    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(18, 12), dpi=100)
    aggregated = (df / df.iloc[0]) * weightList * initialValue
    if (len(assetList) > 1):
        aggregated["Portfolio"] = aggregated.values.sum(axis=1)
    aggregated.set_index(df.index)
    sns.set_style("dark")
    ax = sns.lineplot(data=aggregated, markers=False)

    ax.get_figure().autofmt_xdate()
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    if (len(assetList) > 1):
        max_value = max(aggregated['Portfolio'])
        max_value_index = aggregated[aggregated['Portfolio'] == max_value][0:1].index
        min_value = min(aggregated['Portfolio'])
        min_value_index = aggregated[aggregated['Portfolio'] == min_value][0:1].index
    else:
        max_value = max(aggregated[name])
        max_value_index = aggregated[aggregated[name] == max_value][0:1].index #there may be more than 2 values with the same max or min
        min_value = min(aggregated[name])
        min_value_index = aggregated[aggregated[name] == min_value][0:1].index
    ax.annotate('Maximum value: ' + str(round(max_value, 2)), xy=(max_value_index, max_value),
                xytext=(max_value_index, max_value+40), bbox=dict(boxstyle="Square,pad=0.2", fc="white", ec="w", lw=2))
    ax.annotate('Minimum value: ' + str(round(min_value, 2)), xy=(min_value_index, min_value),
                xytext=(min_value_index, min_value-40), bbox=dict(boxstyle="Square,pad=0.2", fc="white", ec="w", lw=2))

    ax.plot()
    plt.legend(loc=2)

    totalValue = np.sum((df / df.iloc[0]) * weightList * initialValue, axis=1)
    # print(totalValue.tail())

    total_return = (totalValue[-1] - initialValue) / initialValue
    lastDay = datetime.today().date()
    startDate  = datetime.strptime(startDate, '%Y-%m-%d').date()

    values = aggregated.values.tolist()
    values = [row[0] for row in values]
    list_lists = []
    labels = aggregated.index.values.tolist()
    labels = pd.to_datetime(aggregated.index).strftime('%Y-%m-%d').tolist()
    for column in aggregated.columns:
        list_lists.append(aggregated[column].values.tolist())


    years = (lastDay - startDate).days / 365.25
    annualized_return = total_return / years

    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    return plot_url, round(totalValue[-1], 0), missing_data, wrong_weights, total_return, annualized_return
