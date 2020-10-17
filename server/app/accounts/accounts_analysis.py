from app.accounts import ncr_banking_api_requests
user = {
    "username" : "HACKATHONUSER101",
    "phone" : 4048842018,
    "portfolio" : {"AAPL": 50, "GOOGL": 20},
    "savingsGoal" : 50,
    "nextGoal" : 50
}

savings = {
    "id" : "kajsdf9823urkushdf",
    "balance": 100,
    "transactions": [{"date" : "2016-12-18T", "amount" : 10}]
}

checkings = {
    "id" : "kajsdf9823urkushdf",
    "balance": 150,
    "transactions": [{"date" : "2016-12-18T", "amount" : 100}]
}

accounts_metrics = {
    "largePurchases" : .80,
    "smallPurchases" : .70,
    "savingsScore" : 55
}


def init_metrics(phone_number):
    return 0

def get_checkings_stats():
    return {
            "id" : "kajsdf9823urkushdf",
            "balance": 150,
            "transactions": [{"date" : "2016-12-18T", "amount" : 100}],
            "expenditures": 100 
        }

def get_savings_stats():
    return {
            "id" : "kajsdf9823urkushdf",
            "balance": 100,
            "transactions": [{"date" : "2016-12-18T", "amount" : 10}],
            "savings": 10
        }

def get_category():
    return {
            "incomeClass" : 2,
            "spendingClass": 3,
        }

def get_purchase_breakdown():
    return {
            "largePurchasePercent" : {"score": 90, "classAverage": 80},
            "smallPurchasePercent": {"score": 10, "classAverage": 15}
        }

def get_savings_breakdown():
    return {
            "savingsScore" : {"score": 98, "classAverage": 83},
            "savingsGoal": 28
        }