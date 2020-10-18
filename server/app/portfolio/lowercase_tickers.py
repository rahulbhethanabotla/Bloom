import json

with open("./tickers.json") as json_file:
    tickers = json.load(json_file)

tickers = list(tickers.items())

tickers = [(key.lower(), value) for key, value in tickers]
tickers = dict(tickers)
# print(tickers)

with open("./tickers.json", "w") as f:
    json.dump(tickers, f)