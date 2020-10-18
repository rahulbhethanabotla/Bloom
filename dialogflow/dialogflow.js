// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const fetch = require('node-fetch');
const { WebhookClient, Image } = require('dialogflow-fulfillment');
const { base64encode } = require('nodejs-base64');
const unirest = require('unirest');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

const baseUrl = "https://hackgt.loca.lt";
const endpoints = {
    getChecking: '/accounts/checkings',
    getSavings: '/accounts/savings',
    getCatagory: '/accounts/metrics/category',
    getPurchaseMetrics: '/accounts/metrics/purchases',
    getSavingsMetrics: '/accounts/metrics/savings',
    getPortfolioStats: '/graphs/portfolio/stats',
    getStockStats: '/graphs/stock/stats',
    purchaseGraph: '/purchase.png',
    checkingGraph: '/checking.png',
    portfolioGraph: '/portfolio.png',
    stockGraph: '/stock.png'
};

const stocks = {
    Energy: ['Chevron Corporation', 'CVX'],
    Materials: ['Newmont Corp', 'NEM'],
    Industrials: ['FedEx Corp', 'FDX'],
    Financials: ['BlackRock, Inc.', 'BLK'],
    Health: ['Biogen Inc.', 'BIB'],
    Technology: ['NCR Corporation', 'NCR'],
    Housing: ['Equity Commonwealth', 'EQC'],
    Telecommunication: ['Zoom Video Communications Inc.', 'ZM']
}

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(async (request, response) => {
    const agent = new WebhookClient({ request, response });
    const data = parseDialogflowRequest(request);

    console.log("NEW REQUEST", JSON.stringify(request.body))

    async function accountHistoryHandler(agent) {
        let checkingResponse = await fetch(`${baseUrl}${endpoints.getChecking}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        });
        let checkingJson = await checkingResponse.json();
        const expenditures = checkingJson.expenditures;
        const recentTransactions = checkingJson.transactions;

        let savingsBreakdown = await fetch(`${baseUrl}${endpoints.getSavingsMetrics}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        })
        let savingsJson = await savingsBreakdown.json()
        const totalSavings = savingsJson.monthlySavings.score

        const message = `You spent $${expenditures} and saved a total of $${totalSavings} last month. Your most recent transactions were on ${recentTransactions[0].date} for $${recentTransactions[0].amount} and on ${recentTransactions[1].date} for $${recentTransactions[1].amount}. Let me know if you want more information about your transation history.`;
        const graphUrl = `${baseUrl}${endpoints.checkingGraph}?phone=${data.phoneNumberFrom}`
        sendMedia(graphUrl, data.phoneNumberTo, data.phoneNumberFrom);
        agent.add(message);
    }

    async function accountHistoryMoreHandler(agent) {
        let purchaseMetrics = await fetch(`${baseUrl}${endpoints.getPurchaseMetrics}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        });
        let metricsJson = await purchaseMetrics.json();

        const largePercent = metricsJson.largePurchasePercent.score.toFixed(2)
        const smallPercent = metricsJson.smallPurchasePercent.score.toFixed(2)

        let message = `Of all your purchases last month, ${largePercent}% were large purchases and ${smallPercent}% were small purchases.`
        if (largePercent <= smallPercent) {
            message += ' Gotta be careful with the little things, sometimes they can really add up!'
        }
        const graphUrl = `${baseUrl}${endpoints.purchaseGraph}?phone=${data.phoneNumberFrom}`
        sendMedia(graphUrl, data.phoneNumberTo, data.phoneNumberFrom);
        agent.add(message)
    }

    async function accountAmountHandler(agent) {
        let checkingResponse = await fetch(`${baseUrl}${endpoints.getChecking}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        });
        let checkingJson = await checkingResponse.json()
        const checkingBalance = checkingJson.balance;

        let savingsResponse = await fetch(`${baseUrl}${endpoints.getSavings}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        });
        let savingsJson = await savingsResponse.json()
        const savingsBalance = savingsJson.balance;
        
        const message = `You have $${checkingBalance} in your checking account and $${savingsBalance} in your savings account for a total balance of $${checkingBalance + savingsBalance}`;
        agent.add(message);
    }

    async function specificAccountAmountHandler(agent) {
        let account = data.parameters.account
        let message = ''
        if (account === 'checking') {
            let checkingResponse = await fetch(`${baseUrl}${endpoints.getChecking}`, {
                method: 'get',
                headers: { "phone": data.phoneNumberFrom },
            });
            let checkingJson = await checkingResponse.json()

            const balance = checkingJson.balance;
            const withdrawls = checkingJson.transactions
            const expenditures = checkingJson.expenditures

            message = `You have $${balance} in your checking account. Your expenditures for the last month were $${expenditures}. Your most recent withdrawls were on ${withdrawls[0].date} for $${withdrawls[0].amount} and on ${withdrawls[1].date} for $${withdrawls[1].amount}.`

        } else {
            let savingsResponse = await fetch(`${baseUrl}${endpoints.getSavings}`, {
                method: 'get',
                headers: { "phone": data.phoneNumberFrom },
            });
            let savingsJson = await savingsResponse.json()

            const balance = savingsJson.balance
            const deposits = savingsJson.transactions
            const income = savingsJson.income

            message = `You have $${balance} in your savings account. Your income for the last month was $${income}. Your most recent deposits were on ${deposits[0].date} for $${deposits[0].amount} and on ${deposits[1].date} for $${deposits[1].amount}.`
        }
        agent.add(message)
    }

    async function accountRecHandler(agent) {
        let savingsBreakdown = await fetch(`${baseUrl}${endpoints.getSavingsMetrics}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        })
        let savingsJson = await savingsBreakdown.json()

        const userScore = savingsJson.savingsScore.score
        const classScore = savingsJson.savingsScore.classAverage
        const savingsGoal = savingsJson.savingsGoal
        const totalSavings = savingsJson.monthlySavings.score
        let message = `You saved a total of $${totalSavings} last month. According to out state of the art Savings Score™, you have a score of ${userScore} while the average for people of similar income as you is ${classScore}.`
        if (userScore < classScore) {
            message += ` We really recommend that you save more money. You can start by changing your savings goals.`
        } else {
            message += ` Basically, you're doing awesome! You're already great at saving, but it's never bad to save more.`
        }
        agent.add(message);
    }

    async function accountGoalHandler(agent) {
        let savingsResponse = await fetch(`${baseUrl}${endpoints.getSavingsMetrics}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        })
        let savingsJson = await savingsResponse.json()

        const userScore = savingsJson.savingsScore.score
        const totalSavings = savingsJson.monthlySavings.score
        const savingsGoal = savingsJson.savingsGoal

        let message = `You saved a total of $${totalSavings} last month. You had a savings goal of ${savingsGoal} and achieved a Savings Score™ of ${userScore} last month.`
        if (savingsGoal > userScore) {
            message += " It's ok, you can do better next month!"
        } else {
            message += " Awesome job! Have you considered investing some of those savings? You can get started right here, feel free to ask me a question about stocks!"
        }
        agent.add(message)
    }

    function investRecHandler(agent) {
        if (!data.containsAllParameters) {
            return
        }
        let industry = data.parameters.industry
        let nameAndTicker = stocks[industry]
        
        let name = nameAndTicker[0]
        let ticker = nameAndTicker[1]
        
        let message = `For a ${industry.toLowerCase()} stock, I recommend that you look into ${name}.`
        if (industry === 'Technology') {
            message += ' I hear they are great at hackathons :)'
        } else if (industry === 'Telecommunication') {
            message += ' You might of heard of this company from the term \"zoom university\".'
        }
        message += ' Let me know if you would more information about this company.'
        agent.add(message)
    }

    async function investRecMoreHandler(agent) {
        let industry = data.parameters.industry
        let nameAndTicker = stocks[industry]

        let name = nameAndTicker[0]
        let ticker = nameAndTicker[1]

        let stockInfo = await fetch(`${baseUrl}${endpoints.getStockStats}`, {
            method: 'get',
            headers: { "ticker": ticker },
        })
        let stockInfoJson = await stockInfo.json()
        
        let dayPerf = stockInfoJson.oneDayPerformance.toFixed(3)
        let monthPerf = stockInfoJson.oneMonthPerformance.toFixed(3)
        let sharpeRatio = stockInfoJson.riskReturnRatioYear.toFixed(3)

        let message = `${name} stock had a return of ${dayPerf}% today and ${monthPerf}% over the past month. The stock has a Sharpe ratio of ${sharpeRatio}.`
        const graphUrl = `${baseUrl}${endpoints.stockGraph}?ticker=${ticker}`
        sendMedia(graphUrl, data.phoneNumberTo, data.phoneNumberFrom);
        agent.add(message)
    }

    async function investStockHandler(agent) {
        if (!data.containsAllParameters) {
            return
        }
        let stock = data.parameters.stock.toLowerCase()
        let stockInfo = await fetch(`${baseUrl}${endpoints.getStockStats}`, {
            method: 'get',
            headers: { "company": stock },
        })
        let stockInfoJson = await stockInfo.json()
        
        console.log('Stock Perf', stockInfoJson, JSON.stringify(stockInfoJson))
        let dayPerf = stockInfoJson.oneDayPerformance.toFixed(3)
        let monthPerf = stockInfoJson.oneMonthPerformance.toFixed(3)
        let sharpeRatio = stockInfoJson.riskReturnRatioYear.toFixed(3)

        console.log("STOCK PERF", dayPerf, monthPerf, sharpeRatio)

        let message = `${data.parameters.stock} stock had a return of ${dayPerf}% today and ${monthPerf}% over the past month. The stock has a Sharpe ratio of ${sharpeRatio}.`
        const graphUrl = `${baseUrl}${endpoints.stockGraph}?company=${encodeURI(stock)}`
        sendMedia(graphUrl, data.phoneNumberTo, data.phoneNumberFrom);
        agent.add(message)
    }

    async function investPortfolioHandler(agent) {
        console.log("IN PORTFOLIO")
        let portfolioResponse = await fetch(`${baseUrl}${endpoints.getPortfolioStats}`, {
            method: 'get',
            headers: { "phone": data.phoneNumberFrom },
        })
        let portfolioJson = await portfolioResponse.json()
        console.log("Portfolio", portfolioJson, JSON.stringify(portfolioJson))

        let dayPerf = portfolioJson.oneDayPerformance.toFixed(3)
        let monthPerf = portfolioJson.oneMonthPerformance.toFixed(3)
        let yearPerf = portfolioJson.growthLevelOverYear.toFixed(3)
        let sharpeRatio = portfolioJson.riskReturnRatio.toFixed(3)

        let message = `Your portfolio has a return of ${dayPerf}% today, ${monthPerf}% over the past month, and ${yearPerf}% over the past year. Your portfolio has a Sharpe ratio of ${sharpeRatio}.`
        const graphUrl = `${baseUrl}${endpoints.portfolioGraph}?phone=${data.phoneNumberFrom}`
        sendMedia(graphUrl, data.phoneNumberTo, data.phoneNumberFrom);
        agent.add(message)
    }

    let intentMap = new Map();
    intentMap.set('account.history', accountHistoryHandler);
    intentMap.set('account.history - more', accountHistoryMoreHandler);
    intentMap.set('account.amount', accountAmountHandler);
    intentMap.set('account.amount.specific', specificAccountAmountHandler);
    intentMap.set('account.recommendation', accountRecHandler);
    intentMap.set('account.goal', accountGoalHandler);
    intentMap.set('investment.recommendation', investRecHandler);
    intentMap.set('investment.recommendation - more', investRecMoreHandler);
    intentMap.set('investment.stock', investStockHandler);
    intentMap.set('investment.portfolio', investPortfolioHandler);
    agent.handleRequest(intentMap);
});

function parseDialogflowRequest(request) {
    const parameters = request.body.queryResult.parameters;
    const containsAllParameters = request.body.queryResult.allRequiredParamsPresent;
    const intent = request.body.queryResult.intent.displayName;
    const phoneNumberFrom = request.body.originalDetectIntentRequest.payload.From;
    const phoneNumberTo = request.body.originalDetectIntentRequest.payload.To;

    return {
        parameters: parameters,
        containsAllParameters: containsAllParameters,
        intent: intent,
        phoneNumberFrom: phoneNumberFrom,
        phoneNumberTo: phoneNumberTo,
    };
}

function sendMedia(mediaUrl, phoneNumberFrom, phoneNumberTo) {
    console.log("SENDING MEDIA");
    const accountSID = "AC19a51e2c4b2942c909ca6946e3590778";
    const authToken = "0767e30230f1053dddae91b5ed591c11";

    const authorization = base64encode(`${accountSID}:${authToken}`);
    const body = {
        'From': phoneNumberFrom,
        'To': phoneNumberTo,
        'MediaUrl': mediaUrl
    };

    const req = unirest('POST', `https://api.twilio.com/2010-04-01/Accounts/${accountSID}/Messages.json`)      
    .headers({
      'Authorization': `Basic ${authorization}`
     })
    .field('To', phoneNumberTo)
    .field('From', phoneNumberFrom)
    .field('MediaUrl', mediaUrl)
    .end(function (res) { 
        if (res.error) {
            console.log("ERROR SEDNING MEDIA");
        }
        console.log("MEDIA SENT", res.raw_body);
    });
}
