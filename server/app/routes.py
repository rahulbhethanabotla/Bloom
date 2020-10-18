from app import app
import json
from app.accounts import accounts_analysis
from flask import request

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