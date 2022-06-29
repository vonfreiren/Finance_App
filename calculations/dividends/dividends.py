
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import seaborn as sns

from auxiliar.feed_security_data import preDownloadSecurityDB

matplotlib.use('Agg')


def retrieve_dividends(asset):
    missingData = False
    data = yf.Ticker(asset).get_dividends()
    if len(data) == 0:
        missingData = True
        return None, missingData, None, None
    data.dropna()
    asset = preDownloadSecurityDB(asset)
    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(16, 12), dpi=150)
    sns.set_style("dark")
    ax = sns.lineplot(data=data, markers=True, marker="*")
    df = data.to_frame()
    mean = data.mean()
    last_5 =df.tail()


    #fig, ax = plt.subplots(figsize=(14,10), dpi=120)
    #ax = sns.barplot(x= data.index,y=data)

    ax.get_figure().autofmt_xdate()
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.plot()
    plt.savefig(img, format='png',edgecolor='blue', facecolor='white', transparent=False, dpi=500)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())




    return plot_url, missingData, mean, last_5
