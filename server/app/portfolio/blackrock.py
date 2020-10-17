import requests
import json


# generates performance data
# input can literally be the portfolio variable from customer object
# takes the form: [["SNAP", 30.3], ["AAPL", 23.4], .....]
def get_portfolio_performance_chart_data(portfolio):
    url = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?apiVersion=v1&calculateExpectedReturns=true&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&endDate=20201016&includeChartData=true&positions="
    startdateurl = "&startDate=20200101"
    portfolio_url_string = ""
    for position in portfolio:
        portfolio_url_string += position[0] + "~" + str(position[1]) + "%7C"
    portfolio_url_string = portfolio_url_string[:-3]
    url = url + portfolio_url_string + startdateurl
    payload = {
        "apiVersion" :  "v1",
        "calculateExpectedReturns" :  "true",
        "calculateExposures" :  "true",
        "calculatePerformance" :  "true",
        "calculateRisk" :  "true",
        "calculateStressTests" :  "true",
        "endDate" :  "20201016",
        "includeChartData" :  "true",
        "positions" :  "AAPL~50|TWTR~50",
        "startDate" :  "20200101"
    }
    headers = {

    }
    response = requests.request('GET', url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    performanceData = json_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['performanceChart']
    return performanceData

# print(get_portfolio_performance_chart_data([["AAPL", 30.3], ["SNAP", 12.3]]))


# returns how your portfolio has been done 
def get_latest_performance(portfolio):
    url = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?apiVersion=v1&calculateExpectedReturns=true&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&endDate=20201016&includeChartData=true&positions="
    startdateurl = "&startDate=20200101"
    portfolio_url_string = ""
    for position in portfolio:
        portfolio_url_string += position[0] + "~" + str(position[1]) + "%7C"
    portfolio_url_string = portfolio_url_string[:-3]
    url = url + portfolio_url_string + startdateurl
    payload = {
        "apiVersion" :  "v1",
        "calculateExpectedReturns" :  "true",
        "calculateExposures" :  "true",
        "calculatePerformance" :  "true",
        "calculateRisk" :  "true",
        "calculateStressTests" :  "true",
        "endDate" :  "20201016",
        "includeChartData" :  "true",
        "positions" :  "AAPL~50|TWTR~50",
        "startDate" :  "20200101"
    }
    headers = {

    }
    response = requests.request('GET', url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    latest_performance = json_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['latestPerf']
    pertinent_info = (latest_performance['oneMonth'], latest_performance['oneDay'], latest_performance['level'], latest_performance['sinceStartDateSharpeRatio'])
    return pertinent_info

print(get_latest_performance([["AAPL", 30.3], ["SNAP", 12.3]]))