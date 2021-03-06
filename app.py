from flask import session, flash, jsonify, redirect, url_for
import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib

from auxiliar import constants
from auxiliar.equivalence_map import etfs, equities

matplotlib.use('Agg')
from flask_sqlalchemy import SQLAlchemy

from flask_assets import Environment, Bundle
from calculations.montecarlo.montecarlo_calculation import calculation
from calculations.correlation.correlation_calculation import calculation_multiple, correlation_two
from calculations.correlation.fund_comparator import calculate_funds
from calculations.timevalue.portfolio_calculation import calculate_portfolio
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import validators
from calculations.optimization.portfolio_optimization import optimize
from calculations.timevalue.calculate_worst_best_days import calculate_worst_best
from auxiliar.feed_security_data import preDownloadSecurityDB
from tasks import make_celery
from calculations.dividends.dividends import retrieve_dividends
import  random
app = Flask(__name__, static_url_path='/static/assets', static_folder='static/assets')
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})
celery = make_celery(app)

@celery.task
def my_background_task(arg1, arg2):
    print(arg1 + arg2)
    return (arg1 + arg2)


Bootstrap(app)
datepicker(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['SECRET_KEY'] = '#$%^&*tmtkttktktkt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Security(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100), unique=False, nullable=False)
    name = db.Column(db.String(300), unique=False, nullable=False)
    asset_type = db.Column(db.String(100), unique=False, nullable=False)
    exchange = db.Column(db.String(100), unique=False, nullable=True)
    market = db.Column(db.String(100), unique=False, nullable=True)
    currency = db.Column(db.String(100), unique=False, nullable=True)
    yield_amount = db.Column(db.NUMERIC(100), unique=False, nullable=True)
    category = db.Column(db.String(100), unique=False, nullable=True)
    morningstar_rating = db.Column(db.String(100), unique=False, nullable=True)
    isin = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Security %r>' % self.name


# db.drop_all()
# db.create_all()

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)


class DateForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))


X = np.random.randn(50000)
Y = np.random.randn(50000)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/montecarlo', methods=['GET', 'POST'])
def montecarlo():
    assetList = []
    if request.method == 'POST':
        for value in request.form.items():
            if ("asset" in value[0] and value[1]):
                asset = value[1].upper().split(' ')[0]
                assetList.append(asset)
    if (len(assetList) > 1 and assetList):
        plot_url, missingData, values_list, labels_list = calculation(assetList)
        if missingData:
            flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
        else:
            return render_template("montecarlo_res.html", plot_url=plot_url.decode('utf8'), values_list=values_list, labels_list=labels_list)

    return render_template("montecarlo.html")


@app.route('/dividends', methods=['GET', 'POST'])
def dividends():
    if request.method == 'POST':
        asset = request.form.get('asset')
        if (asset):
            asset = asset.split(' ')[0]
            missing_data, dividend_info, last_5, values, labels, security_info, company_info, financial_info = retrieve_dividends(asset)
            if missing_data:
                flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
            else:
                if (asset):
                    return render_template("dividends_results.html", asset=asset, dividend_info=dividend_info, last_5=last_5.to_html(classes='table-striped text-right'), values=values, labels=labels, security_info=security_info, company_info=company_info, financial_info=financial_info)

    return render_template("dividends.html")

@app.route('/funds_results/<ticker>', methods=['GET', 'POST'])
def funds_results(ticker=None):
    colors = []
    for x in range(0, 1):
        hexadecimal = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
        colors.append(hexadecimal)
    asset=ticker
    asset = asset.split(' ')[0]
    ticker = asset
    missing_data, asset_type, asset, std_3, return_3, values_list, labels_list, price, currency, price_last_year, last_change, last_pct_change, change_last_year, list_news, company_info, financial_info, portfolio, name_list, balance_sheet, performance_info = calculate_funds(
        asset)
    if missing_data:
        flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
        return redirect(url_for('compare_fund'))
    else:
        if (asset):
            if asset_type == etfs or asset_type == 'MUTUALFUND':
                return render_template("funds_results.html", ticker=ticker, asset=asset, std_3=std_3, return_3=return_3,
                                   values_list=values_list, labels_list=labels_list, price=price, currency=currency,
                                   price_last_year=price_last_year, last_change=last_change,
                                   last_pct_change=last_pct_change, change_last_year=change_last_year,
                                   list_news=list_news, company_info=company_info, financial_info=financial_info,
                                   portfolio=portfolio, colors=colors, name_list=name_list,
                                   balance_sheet=balance_sheet.to_html(classes='table-borderless-2 text-right',
                                                                       index=False, escape=False), performance_info=performance_info )
            if asset_type == equities:
                return render_template("equities_results.html", ticker=ticker, asset=asset, std_3=std_3, return_3=return_3,
                                   values_list=values_list, labels_list=labels_list, price=price, currency=currency,
                                   price_last_year=price_last_year, last_change=last_change,
                                   last_pct_change=last_pct_change, change_last_year=change_last_year,
                                   list_news=list_news, company_info=company_info, financial_info=financial_info,
                                   portfolio=portfolio, colors=colors, name_list=name_list,
                                   balance_sheet=balance_sheet.to_html(classes='table-borderless-2 text-right',
                                                                       index=False), performance_info=performance_info )
            else:
                return render_template("equities_results.html", ticker=ticker, asset=asset, std_3=std_3, return_3=return_3,
                                   values_list=values_list, labels_list=labels_list, price=price, currency=currency,
                                   price_last_year=price_last_year, last_change=last_change,
                                   last_pct_change=last_pct_change, change_last_year=change_last_year,
                                   list_news=list_news, company_info=company_info, financial_info=financial_info,
                                   portfolio=portfolio, colors=colors, name_list=name_list, performance_info=performance_info)

    flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
    return redirect(url_for('compare_fund'))
    return render_template('funds.html')


@app.route('/funds_comparator', methods=['GET', 'POST'])
def compare_fund():

    if request.method == 'POST':
        asset = request.form.get('asset')
        if (asset):
            asset = asset.split(' ')[0]
            ticker = asset
            funds_results(ticker)
            return redirect(url_for('funds_results', ticker=ticker))
        return render_template("funds.html")

    return render_template("funds.html")


@app.route('/asset_worst_best', methods=['GET', 'POST'])
def asset_worst_best():
    if request.method == 'POST':
        asset = request.form.get('asset')
        asset = asset.split(' ')[0]
        if (asset):
            df_worst, df_best, missing_data, prices_list, security_info = calculate_worst_best(asset)
            if missing_data:
                flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
            else:
                if (asset):
                    return render_template("asset_worst_best_res.html", asset=asset, df_best=df_best.to_html(classes='table text-right'), df_worst=df_worst.to_html(classes='table text-righ'), prices_list =prices_list, security_info=security_info)

    return render_template("asset_worst_best.html")


@app.route('/portfolio_optimization', methods=['GET', 'POST'])
def portfolio_optimization():


    colors = []

    for x in range(0, 15):
        hexadecimal = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
        print(x)
        colors.append(hexadecimal)

    print(colors)

    calculation_methods = constants.CALCULATION_METHODS
    assetList = []
    if request.method == 'POST':
        for value in request.form.items():
            if ("asset" in value[0] and value[1]):
                asset = value[1].upper().split(' ')[0]
                assetList.append(asset)
            initial_value = request.form.get('initialValue2')
            initial_value = float(initial_value)
            calculation_method = request.form.get('calculation_method')
            risk = request.form.get('risk')
        if (len(assetList) > 1 and assetList):
            plot_url, opt_values, df, df2, moneyLeft, missingData, values, labels = optimize(assetList, initial_value, calculation_method, risk)
            if missingData:
                flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
            else:
                if (len(assetList) > 1 and assetList):
                    return render_template("portfolio_optimization_res.html", plot_url=plot_url.decode('utf8'),
                                           optValues=opt_values, name="Opti", df=df.to_html(), df2=df2, calculation_methods=calculation_methods, moneyLeft=moneyLeft,
                                           initialValue=f'{initial_value:,}', values=values, labels=labels, colors=colors)

    return render_template("portfolio_optimization.html", calculation_methods=calculation_methods)



@app.route('/portfolio_optimization_result', methods=['GET', 'POST'])
def portfolio_optimization_result():
    calculation_methods = constants.CALCULATION_METHODS
    return render_template("portfolio_optimization.html", calculation_methods=calculation_methods)


@app.route('/portfolio_value', methods=['GET', 'POST'])
def portfolio_value():
    assetList = []
    weightList = []

    colors = []

    for x in range(0, 15):
        hexadecimal = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
        print(x)
        colors.append(hexadecimal)

    if request.method == 'POST':
        stock = request.form.get('asset')
        session['startdate'] = request.form.get('date')
        initialValue = request.form.get('initialValue')
        if stock:
            stock = stock.split(' ')[0]
            assetList.append(stock)
            weightList.append(1)
            initialValue = float(initialValue)
            plot_url, finalValue, missingData, wrong_weights, total_return, annualized_return, values, labels, dict, list_lists, portfolio, asset_labels = calculate_portfolio(assetList, weightList, initialValue,
                                                                                   session['startdate'])
            if (missingData):
                flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
            else:
                return render_template("portfolio_value_res.html", plot_url=plot_url.decode('utf8'),
                                       initialValue=f'{initialValue:,}', finalValue=f'{finalValue:,}', total_return="{0:.0%}".format(total_return), annualized_return="{0:.0%}".format(annualized_return), values = values, labels=labels, df=dict, list_lists=list_lists, portfolio=portfolio, asset_labels=asset_labels, colors=colors)
        else:
            for value in request.form.items():
                if ("asset" in value[0] and value[1]):
                    asset = value[1].upper().split(' ')[0]
                    assetList.append(asset)
                if ("weight" in value[0] and value[1]):
                    if float(value[1])>0:
                        weightList.append(value[1])
            if (len(assetList) > 1 and assetList and len(weightList) > 1 and len(weightList) == len(assetList)):
                initialValue = float(initialValue)
                weightList = [float(weight) / 100 for (weight) in weightList]
                plot_url, finalValue, missingData, wrong_weights, total_return, annualized_return, values, labels, dict, list_lists, portfolio, asset_labels = calculate_portfolio(assetList, weightList,
                                                                                       initialValue,
                                                                                       session['startdate'])
                if wrong_weights:
                    flash(constants.WRONG_WEIGHTS_PORTFOLIO_CALCULATIONS, constants.FLASH_DANGER_CATEGORY)
                elif missingData:
                    flash(constants.MISSING_DATA_TICKER, constants.FLASH_DANGER_CATEGORY)
                else:
                    if (len(assetList) > 1 and assetList):
                        return render_template("portfolio_value_res.html", plot_url=plot_url.decode('utf8'),
                                               initialValue=f'{initialValue:,}', finalValue=f'{finalValue:,}', total_return="{0:.0%}".format(total_return), annualized_return="{0:.0%}".format(annualized_return), values=values, labels=labels, df=dict, list_lists=list_lists, portfolio=portfolio, asset_labels=asset_labels, colors=colors)
            else:
                flash(constants.WRONG_WEIGHTS_ASSETS_NUMBER, constants.FLASH_DANGER_CATEGORY)
    return render_template("portfolio_value.html")








@app.route('/correlation_multiple', methods=['GET', 'POST'])
def correlation_multiple():
    assetList = []
    if request.method == 'POST':
        for value in request.form.items():
            if ("asset" in value[0] and value[1]):
                asset = value[1].upper().split(' ')[0]
                assetList.append(asset)
    if (len(assetList) > 1 and assetList):
        plot_url, missingData, missing_ticker = calculation_multiple(assetList)

        if missingData:
            flash(constants.MISSING_DATA_TICKER + ":" + missing_ticker, constants.FLASH_DANGER_CATEGORY)
        else:
            if (len(assetList) > 1 and assetList):
                return render_template("correlation_mulres.html", plot_url=plot_url.decode('utf8'))
    return render_template("correlation_multiple.html")


@app.route('/correlation', methods=['GET', 'POST'])
def correlation():
    asset = ""
    asset2 = ""
    alpha = 0
    beta = 0
    assetList = []

    if request.method == 'POST':
        asset = request.form.get('asset')
        asset2 = request.form.get('asset2')

        if (asset and asset2):
            asset = asset.split(' ')[0]
            asset2 = asset2.split(' ')[0]
            assetList.append(asset)
            assetList.append(asset2)
            log_returns, missingData, missing_ticker = fetchData(assetList)
            if (missingData != True):
                for item, instrument in enumerate(assetList):
                    name, asset_type, exchange, market, currency, isin = preDownloadSecurityDB(instrument)
                    if (item == 1):
                        assetName2 = name
                    else:
                        assetName = name

                alpha, beta, plot_url = correlation_two(asset, asset2, log_returns)

            if missingData:
                flash(constants.MISSING_DATA_TICKER + ":" + missing_ticker, category=constants.FLASH_DANGER_CATEGORY)
            else:
                if asset and asset2:
                    return render_template("correlation_res.html", asset=asset, name=assetName, asset2=asset2,
                                           name2=assetName2, alpha=alpha, beta=beta, plot_url=plot_url.decode('utf8'))

    return render_template("correlation.html")




def insertSecurityDB(asset, assetName, quoteType, exchange, market, currency, yield_amount, category,
                     morningStarRiskRating):
    security = Security(ticker=asset, name=assetName, asset_type=quoteType, exchange=exchange, market=market,
                        currency=currency, yield_amount=yield_amount, category=category,
                        morningstar_rating=morningStarRiskRating, isin="")
    db.session.add(security)
    db.session.commit()


@app.route('/correlation_result', methods=['GET'])
def correlation_result():
    return render_template("correlation.html")


def fetchData(assetList):
    endDate = datetime.today().strftime('%Y-%m-%d')
    df = pd.DataFrame()
    missingData = False
    for asset in assetList:
        data = yf.download(asset, '2000-01-01', endDate)
        if data.empty:
            missingData = True
            return None, missingData, asset
        data['pct_change'] = data['Close'].pct_change()
        df[asset] = data['pct_change']

    log_returns = df.dropna()
    return log_returns, missingData, asset


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    results = []
    query1 = db.session.query(Security.ticker, Security.name).filter(Security.name.like('%' + str(search) + '%'))
    query2 = db.session.query(Security.ticker, Security.name).filter(Security.ticker.like('%' + str(search) + '%'))
    query = query1.union(query2)
    for mv in query.all():
        results.append(mv[0]+" - "+mv[1])
    #results = [mv[0] for mv in query.all()]
    #return matching_results=(Response(json.dumps(results), mimetype='application/json'))
    return jsonify(matching_results=results)

if __name__ == '__main__':
    #task = my_background_task.apply_async(args=[10, 20], countdown=10)
    app.run(debug=True, host='0.0.0.0')
