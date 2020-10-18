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
    "transactions": [{"date" : "2020-10-16", "amount" : 10},
                    {"date" : "2020-10-16", "amount" : 10},
                    {"date" : "2020-10-15", "amount" : 10},
                    {"date" : "2020-10-13", "amount" : 10},
                    {"date" : "2020-10-7", "amount" : 10},
                    {"date" : "2020-10-6", "amount" : 10},
                    {"date" : "2020-10-5", "amount" : 10},
                    {"date" : "2020-10-3", "amount" : 10},
                    {"date" : "2020-10-1", "amount" : 10},
                     {"date": "2020-10-1", "amount": 10},
                    {"date" : "2020-9-19", "amount" : 10},
                    {"date" : "2020-9-18", "amount" : 10},
                    {"date" : "2020-9-17", "amount" : 10},
                    {"date" : "2020-9-16", "amount" : 10}]
}

checkings = {
    "id" : "kajsdf9823urkushdf",
    "balance": 300,
    "transactions": [{"date" : "2020-10-16", "amount" : 10},
                    {"date" : "2020-10-16", "amount" : 1},
                    {"date" : "2020-10-15", "amount" : 10},
                    {"date" : "2020-10-13", "amount" : 1},
                    {"date" : "2020-10-7", "amount" : 10},
                    {"date" : "2020-10-6", "amount" : 1},
                    {"date" : "2020-10-5", "amount" : 10},
                    {"date" : "2020-10-3", "amount" : 10},
                    {"date" : "2020-10-1", "amount" : 50},
                     {"date": "2020-10-1", "amount": 8},
                    {"date" : "2020-9-19", "amount" : 31},
                    {"date" : "2020-9-18", "amount" : 10},
                    {"date" : "2020-9-17", "amount" : 35},
                    {"date" : "2020-9-16", "amount" : 35}]
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
            "transactions": [
                {"date" : "2020-10-16", "amount" : 1},
                {"date" : "2020-10-16", "amount" : 10},
                {"date" : "2020-10-15", "amount" : 10},
                {"date" : "2020-10-13", "amount" : 10},
                {"date" : "2020-10-7", "amount" : 15},
                {"date" : "2020-10-6", "amount" : 10},
                {"date" : "2020-10-5", "amount" : 100},
                {"date" : "2020-10-3", "amount" : 10},
                {"date" : "2020-10-1", "amount" : 10},
                {"date": "2020-10-1", "amount": 1},
                {"date" : "2020-9-19", "amount" : 10},
                {"date" : "2020-9-18", "amount" : 40},
                {"date" : "2020-9-17", "amount" : 20},
                {"date" : "2020-9-16", "amount" : 30}],
            "expenditures": 100 
        }

def get_savings_stats():
    return {
            "id" : "kajsdf9823urkushdf",
            "balance": 100,
            "transactions": [
                {"date" : "2020-10-16", "amount" : 10},
                {"date" : "2020-10-16", "amount" : 1},
                {"date" : "2020-10-15", "amount" : 10},
                {"date" : "2020-10-13", "amount" : 1},
                {"date" : "2020-10-7", "amount" : 10},
                {"date" : "2020-10-6", "amount" : 1},
                {"date" : "2020-10-5", "amount" : 10},
                {"date" : "2020-10-3", "amount" : 10},
                {"date" : "2020-10-1", "amount" : 50},
                {"date": "2020-10-1", "amount": 8},
                {"date" : "2020-9-19", "amount" : 31},
                {"date" : "2020-9-18", "amount" : 10},
                {"date" : "2020-9-17", "amount" : 35},
                {"date" : "2020-9-16", "amount" : 35}],
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
