from app import app
import json
from app.accounts import accounts_analysis
from app.charts import charts
from flask import Response, send_file, request
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from app.portfolio import blackrock

with open("app/portfolio/tickers.json") as json_file:
    ticker_mapping = json.load(json_file)
tickers = set([value["ticker"] for key, value in ticker_mapping.items()])


def translate_ticker(name):
    if name in tickers:
        return name
    elif name in ticker_mapping:
        return ticker_mapping[name]["ticker"]
    else:
        return 'NCR'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/brian")
def get_webhook():
    brian = {
        "name": "Brian",
        "age": "21",
        "drink": "vodka"
    }

    return json.dumps(brian)


@app.route("/accounts/checkings")
def get_checkings():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_checkings_stats(phone))


@app.route("/plot.png")
def plot_png():
    if(bool(request.args['phone'])):
        phone = request.args['phone']
    else:
        phone = request.headers['phone']
    img = charts.chart_checking_account(
        accounts_analysis.get_checkings_stats(phone))
    return send_file(img,
                     attachment_filename='plot.png',
                     mimetype='image/png')


@app.route("/accounts/savings")
def get_savings():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_savings_stats(phone))


@app.route("/accounts/metrics/category")
def get_category():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_category(phone))


@app.route("/accounts/metrics/purchases")
def get_purchase_breakdown():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_purchase_breakdown(phone))


@app.route("/accounts/metrics/savings")
def get_savings_breakdown():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_savings_breakdown(phone))


@app.route("/portfolio")
def get_portfolio():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_portfolio(phone))


@app.route("/name")
def get_full_name():
    phone = request.headers['phone']
    return json.dumps(accounts_analysis.get_full_name(phone))


@app.route("/graphs/portfolio/performance")
def get_portfolio_performance_chart():
    phone = request.headers['phone']
    return json.dumps(blackrock.get_portfolio_performance_chart_data(accounts_analysis.get_portfolio(phone)))


@app.route("/graphs/portfolio/stats")
def get_portfolio_stats():
    phone = request.headers['phone']
    return json.dumps(blackrock.get_latest_performance(accounts_analysis.get_portfolio(phone)))


@app.route("/graphs/stock/performance")
def get_stock_performance_chart():
    company = translate_ticker(request.headers['company'])
    return json.dumps(blackrock.get_performance_chart_for_one_stock(company))


@app.route("/graphs/stock/stats")
def get_stock_stats():
    company = translate_ticker(request.headers['company'])
    return json.dumps(blackrock.get_latest_performance_for_one_stock(company))
