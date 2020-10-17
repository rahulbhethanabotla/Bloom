// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const fetch = require('node-fetch');
const { WebhookClient, Image } = require('dialogflow-fulfillment');
const { base64encode } = require('nodejs-base64');
const unirest = require('unirest')

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

const baseUrl = "https://hackgt.loca.lt";
const endpoints = {
    test: '/brian',
    getChecking: '/accounts/checkings',
    getSavings: '/accounts/savings',
    getCatagory: '/accounts/metrics/category',
    getPurchaseMetrics: '/accounts/metrics/purchases',
    getSavingsMetrics: '/accounts/metrics/savings',
};

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(async (request, response) => {
    const agent = new WebhookClient({ request, response });
    const data = parseDialogflowRequest(request);

    function welcomeHandler(agent) {
        agent.add(`Welcome to my agent!`);
    }

    function fallbackHandler(agent) {
        agent.add(`I didn't understand`);
        agent.add(`I'm sorry, can you try again?`);
    }

    function accountHistoryHandler(agent) {
        console.log(agent);
        agent.add('Sending a new message');
        sendMedia('https://avatars1.githubusercontent.com/u/36980416?s=200&v=4', data.phoneNumberTo, data.phoneNumberFrom);
    }

    function accountInvestHandler(agent) {
        
    }

    function accountPerfHandler(agent) {
        
    }

    function accountRecHandler(agent) {
        
    }

    function investRecHandler(agent) {
        
    }

    function investRecQueryHandler(agent) {
        
    }

    function investStockHandler(agent) {
        
    }

    // switch(data.intent) {
    //     case 'account.history':
    //         break;
    //     case 'account.invest':
    //         break;
    //     case 'account.performance':
    //         break;
    //     case 'account.recommendation':
    //         break;
    //     case 'investment.recommendation':
    //         break;
    //     case 'investment.recommendation.query':
    //         break;
    //     case 'investment.stock':
    //         break;
    //     case 'Default Fallback Intent':
    //         break;
    //     case 'Default Welcome Intent':
    //         break;
    //     default:
    //         console.log(`Unknown intent: ${data.intent}`)
    //         break;
    // }

    let intentMap = new Map();
    intentMap.set('account.history', accountHistoryHandler);
    intentMap.set('account.invest', accountInvestHandler);
    intentMap.set('account.performance', accountPerfHandler);
    intentMap.set('account.recommendation', accountRecHandler);
    intentMap.set('investment.recommendation', investRecHandler);
    intentMap.set('investment.recommendation.query', investRecQueryHandler);
    intentMap.set('investment.stock', investStockHandler);
    intentMap.set('Default Welcome Intent', welcomeHandler);
    intentMap.set('Default Fallback Intent', fallbackHandler);
    agent.handleRequest(intentMap);

    // const apiResponse = await fetch(`${baseUrl}${endpoints.test}`, {
    //     method: 'post',
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(request.body)
    // })
    // console.log("Response from api", JSON.stringify(apiResponse))
    // console.log("AFTER RESPONSE")
    // response.send(buildChatResponse("I'm inside the function here right now"));
});

function parseDialogflowRequest(request) {
    const parameters = request.body.queryResult.parameters;
    const containsAllParameters = request.body.allRequiredParamsPresent;
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

function buildChatResponse(message) {
    return JSON.stringify({ fulfillmentText: message });
}

function sendMedia(mediaUrl, phoneNumberFrom, phoneNumberTo) {
    console.log("SENDING MEDIA");
    const accountSID = "AC19a51e2c4b2942c909ca6946e3590778";
    const authToken = "2d8ab5b8d9b10c265cbd5d6c6bce8a62";

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


    // fetch(`https://api.twilio.com/2010-04-01/Accounts/${AccountSID}/Messages.json`, {
    //     method: 'post',
    //     headers: {'Authorization': `Basic ${authorization}`},
    //     body: JSON.stringify(body)
    // })
    // .then(res => console.log("Response from twillio: ", res))
    // .catch(err => console.log(`Error in twilio: ${err}`))
}
