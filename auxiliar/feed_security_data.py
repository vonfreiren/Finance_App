
import matplotlib



matplotlib.use('Agg')

from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
import yfinance as yf
import datetime


app = Flask(__name__)
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
    name = db.Column(db.String(100), unique=False, nullable=False)
    asset_type = db.Column(db.String(100), unique=False, nullable=False)
    exchange = db.Column(db.String(100), unique=False, nullable=True)
    market = db.Column(db.String(100), unique=False, nullable=True)
    currency = db.Column(db.String(100), unique=False, nullable=True)
    yield_amount = db.Column(db.NUMERIC(100), unique=False, nullable=True)
    category = db.Column(db.String(100), unique=False, nullable=True)
    morningstar_rating = db.Column(db.String(100), unique=False, nullable=True)
    isin = db.Column(db.String(100), unique=False, nullable=True)
    create_date = db.Column(db.Date(), unique=False, nullable=True)

    def __repr__(self):
        return '<Security %r>' % self.name


def preDownloadSecurityDB(instrument):
    assetName = ""
    security = retrieveSecurityDB(instrument)
    if (security is not None):
        assetName = security.name
    else:
        assetName, quoteType, exchange, market, currency, yield_amount, category, morningStarRiskRating = retrieveAssetName(
            instrument)
        insertSecurityDB(instrument, assetName, quoteType, exchange, market, currency, yield_amount,
                         category, morningStarRiskRating)
    return assetName


def retrieveSecurityDB(asset):
    security = db.session.query(Security).filter_by(ticker=asset).first()
    return security


def insertSecurityDB(asset, assetName, quoteType, exchange, market, currency, yield_amount, category,
                     morningStarRiskRating):
    security = Security(ticker=asset, name=assetName, asset_type=quoteType, exchange=exchange, market=market,
                        currency=currency, yield_amount=yield_amount, category=category,
                        morningstar_rating=morningStarRiskRating, isin="", create_date=datetime.datetime.now())
    db.session.add(security)
    db.session.commit()


def retrieveAssetName(ticker):
    assetInfo = yf.Ticker(ticker).get_info()
    shortName = assetInfo['shortName'] if 'shortName' in assetInfo else None
    quoteType = assetInfo['quoteType'] if 'quoteType' in assetInfo else None
    exchange = assetInfo['exchange'] if 'exchange' in assetInfo else None
    market = assetInfo['market'] if 'market' in assetInfo else None
    currency = assetInfo['currency'] if 'currency' in assetInfo else None
    if 'yield' in assetInfo:
        yield_amount = assetInfo['yield']
    else:
        yield_amount = None
    if 'category' in assetInfo:
        category = assetInfo['category']
    else:
        category = None
    if 'morningStarRiskRating' in assetInfo:
        morningStarRiskRating = assetInfo['morningStarRiskRating']
    else:
        morningStarRiskRating = None

    return shortName, quoteType, exchange, market, currency, yield_amount, category, morningStarRiskRating



