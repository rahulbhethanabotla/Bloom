from app import app
import json
from app.accounts import accounts_analysis
from app.charts import charts
from flask import Response, send_file
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
    return json.dumps(accounts_analysis.get_checkings_stats())


@app.route("/plot.png")
def plot_png():
    img = charts.chart_checking_account(
        accounts_analysis.get_checkings_stats())
    return send_file(img,
                     attachment_filename='plot.png',
                     mimetype='image/png')


@app.route("/accounts/savings")
def get_savings():
    return json.dumps(accounts_analysis.get_savings_stats())


@app.route("/accounts/metrics/category")
def get_category():
    return json.dumps(accounts_analysis.get_category())


@app.route("/accounts/metrics/purchases")
def get_purchase_breakdown():
    return json.dumps(accounts_analysis.get_purchase_breakdown())


@app.route("/accounts/metrics/savings")
def get_savings_breakdown():
    return json.dumps(accounts_analysis.get_savings_breakdown())
