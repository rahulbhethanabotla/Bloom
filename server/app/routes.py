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


def fix_cap(company_name):
    company_name = company_name.lower()
    result = []
    for word in company_name.split():
        fixed_word = word[0].upper() + word[1:]
        result.append(word)
    return " ".join(result)

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


@app.route("/checking.png")
def plot_png():
    phone = request.args['phone']
    img = charts.chart_checking_account(
        accounts_analysis.get_checkings_stats(phone))
    return send_file(img,
                     attachment_filename='checking.png',
                     mimetype='image/png')


@app.route("/purchase.png")
def purchase_png():
    phone = request.args['phone']

    img = charts.chart_purchase_breakdown(
        accounts_analysis.get_purchase_breakdown(phone))
    return send_file(img,
                     attachment_filename='purchase.png',
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
    phone = request.args['phone']  # TODO: change back
    return json.dumps(blackrock.get_portfolio_performance_chart_data(accounts_analysis.get_portfolio(phone)))


@app.route("/portfolio.png")
def portfolio_png():
    phone = request.args['phone']
    data = blackrock.get_portfolio_performance_chart_data(
        accounts_analysis.get_portfolio(phone))
    img = charts.chart_portfolio_performance(data)
    return send_file(img,
                     attachment_filename='portfolio.png',
                     mimetype='image/png')


@app.route("/graphs/portfolio/stats")
def get_portfolio_stats():
    phone = request.headers['phone']
    return json.dumps(blackrock.get_latest_performance(accounts_analysis.get_portfolio(phone)))


@app.route("/graphs/stock/performance")
def get_stock_performance_chart():
    company = translate_ticker(request.headers['company'])
    return json.dumps(blackrock.get_performance_chart_for_one_stock(company))


@app.route("/stock.png")
def stock_png():
    company = request.args['company']
    data = blackrock.get_performance_chart_for_one_stock(company)
    img = charts.chart_stock_performance(data)
    return send_file(img,
                     attachment_filename='stock.png',
                     mimetype='image/png')



@app.route("/graphs/stock/stats")
def get_stock_stats():
    company = ''
    if 'ticker' in request.headers:
        company = request.headers['ticker']
    else:
        company = translate_ticker(request.headers['company'])
    return json.dumps(blackrock.get_latest_performance_for_one_stock(company))
