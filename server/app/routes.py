from app import app
import json


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
