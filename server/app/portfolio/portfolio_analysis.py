from iex import *
from blackrock import *

def get_stock_data(ticker, date_range="month"):
    """
    get the stock data for a given company (ticker) for a date_range (default="month")

    returns:
        2d array 
    """
    if date_range == "month":
        return {"start_date": "Nov 17", "end_date": "Oct 17", "prices": [5.5, 4, 3, 4, 5, 5, 6.1, 3.3]}
    else:
        return {"start_date": "Jan 1", "end_date": "Oct 17", "prices": [5.5, 4, 3, 4, 5.5, 4, 3, 4, 5.5, 4, 3, 4, 5, 5, 6.1, 3.3]}


def get_portfolio_metrics():
    """
    returns the portfolio metrics for your 

    returns:
        2d array 
    """
    return {"expectedReturns": {"monthEnd": 0, "sixMonth": 0, "fiveYear": 0}, 
            "oneYearSharpeRatio" : 0.5,
            "aBunchOfOtherStuff": "..."}

def buy(ticker, amount):
    """
    update porfolio with new purchase
    """
    return 0

def sell(ticker, amount):
    """
    update porfolio with new sell
    """
    return 0

def set_portfolio(portfolio)
    """
    set porfolio to a list fo stocks/amounts
    """
    for stock, amount in portfolio:
        buy(stock, amount)

def get_percents():
    """
    return portfolio dict with percents instead of dollar amounts
    """
    return {"stock1": .9, "stock2": .1}


