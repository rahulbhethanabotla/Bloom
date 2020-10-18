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
    json_PData = {
        "performanceData": performanceData
    }
    return json.dumps(json_PData)

# returns how your portfolio has been doing recently
# proportional change in performance in the last month, ditto performance today, level is proportionally how much it has grown since start date, return weighted by risk over one year
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
    info = {
        "oneMonthPerformance": latest_performance['oneMonth'],
        "oneDayPerformance": latest_performance['oneDay'],
        "growthLevelOverYear": latest_performance['level'],
        "riskReturnRatio": latest_performance['oneYearSharpeRatio']
    }
    return json.dumps(info)


# ticker is a string pls e.g. AAPL
def get_performance_chart_for_one_stock(ticker):
    url = "https://www.blackrock.com/tools/hackathon/performance?apiVersion=v1&endDate=20201016&identifiers=" + ticker + "&startDate=20200101"
    payload = {
        "apiVersion" :  "v1",
        "endDate" :  "20201016",
        "identifiers" :  ticker,
        "startDate" :  "20200101"
    }
    response = requests.request("GET", url, headers={}, data=payload)
    json_data = json.loads(response.text)
    performance_chart = json_data['resultMap']['RETURNS'][0]['performanceChart']
    return json.dumps({"performanceData": performance_chart})



# ticker is a string pls e.g. AAPL
def get_latest_performance_for_one_stock(ticker):
    url = "https://www.blackrock.com/tools/hackathon/performance?apiVersion=v1&endDate=20201016&identifiers=" + ticker + "&startDate=20200101"
    payload = {
        "apiVersion" :  "v1",
        "endDate" :  "20201016",
        "identifiers" :  ticker,
        "startDate" :  "20200101"
    }
    response = requests.request("GET", url, headers={}, data=payload)
    json_data = json.loads(response.text)
    latest_performance = json_data['resultMap']['RETURNS'][0]['latestPerf']
    pertinent_info = (latest_performance['oneMonth'], latest_performance['oneDay'], latest_performance['oneYearSharpeRatio'])
    pInfo = {
        "oneMonthPerformance": latest_performance['oneMonth'],
        "oneDayPerformance": latest_performance['oneDay'],
        "riskReturnRatioYear": latest_performance['oneYearSharpeRatio']
    }
    return json.dumps(pInfo)

