import requests
import json


# generates performance data
# input can literally be the portfolio variable from customer object
# takes the form: [["SNAP", 30.3], ["AAPL", 23.4], .....]
def get_portfolio_performance_chart_data(portfolio):
    url = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?apiVersion=v1&calculateExpectedReturns=true&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&endDate=20201016&includeChartData=true&positions="
    startdateurl = "&startDate=20200101"
    

    portfolio_strings = []
    for ticker, amount in portfolio["portfolio"]:
        portfolio_strings.append("%s~%d" % (ticker, amount))

    portfolio_url_string = "%7C".join(portfolio_strings)

    # for position in portfolio:
    #     portfolio_url_string += position[0] + "~" + str(position[1]) + "%7C"
    # portfolio_url_string = portfolio_url_string[:-3]
    # print("PUS:", portfolio_url_string)
    url = url + portfolio_url_string + startdateurl
    
    for ticker, amount in portfolio["portfolio"]:
        portfolio_strings.append("%s~%d" % (ticker, amount))
    
    # print("|".join(portfolio_strings))
    payload = {
        "apiVersion" :  "v1",
        "calculateExpectedReturns" :  "true",
        "calculateExposures" :  "true",
        "calculatePerformance" :  "true",
        "calculateRisk" :  "true",
        "calculateStressTests" :  "true",
        "endDate" :  "20201016",
        "includeChartData" :  "true",
        "positions" :  "|".join(portfolio_strings),
        "startDate" :  "20200101"
    }
    headers = {

    }
    response = requests.request('GET', url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    # print(json_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0].keys())
    performanceData = json_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['performanceChart']
    json_PData = {
        "performanceData": performanceData
    }
    return json_PData

# returns how your portfolio has been doing recently
# proportional change in performance in the last month, ditto performance today, level is proportionally how much it has grown since start date, return weighted by risk over one year
def get_latest_performance(portfolio):
    url = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?apiVersion=v1&calculateExpectedReturns=true&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&endDate=20201016&includeChartData=true&positions="
    startdateurl = "&startDate=20200101"
    

    portfolio_strings = []
    for ticker, amount in portfolio["portfolio"]:
        portfolio_strings.append("%s~%d" % (ticker, amount))

    portfolio_url_string = "%7C".join(portfolio_strings)

    # for position in portfolio:
    #     portfolio_url_string += position[0] + "~" + str(position[1]) + "%7C"
    # portfolio_url_string = portfolio_url_string[:-3]
    # print("PUS:", portfolio_url_string)
    url = url + portfolio_url_string + startdateurl
    
    for ticker, amount in portfolio["portfolio"]:
        portfolio_strings.append("%s~%d" % (ticker, amount))
    
    # print("|".join(portfolio_strings))
    payload = {
        "apiVersion" :  "v1",
        "calculateExpectedReturns" :  "true",
        "calculateExposures" :  "true",
        "calculatePerformance" :  "true",
        "calculateRisk" :  "true",
        "calculateStressTests" :  "true",
        "endDate" :  "20201016",
        "includeChartData" :  "true",
        "positions" :  "|".join(portfolio_strings),
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
        "riskReturnRatio": latest_performance['sinceStartDateSharpeRatio']
    }
    return info


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
    return {"performanceData": performance_chart}



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
    return pInfo

