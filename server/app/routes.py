from app import app
import json
from app.accounts import accounts_analysis

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