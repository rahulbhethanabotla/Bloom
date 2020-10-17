from app.accounts import ncr_banking_api_requests
import json
import os
known_numbers = {
    "4048842018" :  "HACKATHONUSER001",
    "4082013554" : "HACKATHONUSER074",
    "2019535950" : "HACKATHONUSER076",
    "7323109043" : "HACKATHONUSER126"

}
user_accounts = dict()

print(os.getcwd())
with open("app/accounts/user_accounts.json") as json_file:
    user_accounts = json.load(json_file)

income_quintiles = []
expenditure_quintiles = []
def get_username(phone):
    print('-----')
    print("Phone Number: ", phone)
    if phone in known_numbers: 
        username = known_numbers[phone]
    else:
        username = "HACKATHONUSER001"
    print("Decoded To: ", username)
    return username

def get_full_name(phone):
    # query the ncr buisness api to get name
    return 0

def display_accounts():
    for number in known_numbers.keys():
        print("NUMBER: ", number)
        username = get_username(number)
        checkings = get_checkings_stats(number)
        savings = get_savings_stats(number)
        print("CHECKINGS TRANSACTIONS: ", [t["amount"] for t in checkings["transactions"]])
        print("SAVINGS TRANSACTIONS: ", [t["amount"] for t in savings["transactions"]])
        print("CHECKINGS BALANCE/EXPENDITURES: ", checkings["balance"], checkings["expenditures"])
        print(savings)
        print("SAVINGS BALANCE/SAVINGS: ", savings["balance"], savings["savings"])

def set_up_accounts(phone):
    username = get_username(phone)
    account_response = ncr_banking_api_requests.get_specific_account_for_user(username, "CHECKING")
    id_string = account_response["id"]
    balance = account_response["currentBalance"]["amount"]
    transactions_dict = ncr_banking_api_requests.get_transactions_for_specific_user_account_type("HACKATHONUSER001", "CHECKING")["transactions"]
    transactions = [{"date": t["transactionDate"], "amount" : t["amount"]["amount"]} for t in transactions_dict]
    expenditures = sum([t["amount"] for t in transactions])


    user_accounts[username] = {
        "checkings": {
            "id" : id_string,
            "balance": balance,
            "transactions": transactions,
            "expenditures": expenditures 
        }}
    

    account_response = ncr_banking_api_requests.get_specific_account_for_user(username, "TCL_MASTER")
    id_string = account_response["id"]
    balance = account_response["currentBalance"]["amount"]
    transactions_dict = ncr_banking_api_requests.get_transactions_for_specific_user_account_type("HACKATHONUSER001", "CHECKING")["transactions"]
    transactions = [{"date": t["transactionDate"], "amount" : t["amount"]["amount"]} for t in transactions_dict]
    savings = sum([t["amount"] for t in transactions])
    balance += savings
    user_accounts[username]["savings"] = {
            "id" : id_string,
            "balance": balance,
            "transactions": transactions,
            "income": savings
        }
    
    print(json.dumps(user_accounts))
    
def get_checkings_stats(phone):
    if get_username(phone) not in user_accounts:
        set_up_accounts(phone)
    return user_accounts[get_username(phone)]["checkings"]

def get_savings_stats(phone):
    if get_username(phone) not in user_accounts:
        set_up_accounts(phone)
    return user_accounts[get_username(phone)]["checkings"]

def get_category(phone):
    return {
            "incomeClass" : 2,
            "spendingClass": 3,
        }

def get_purchase_breakdown(phone):
    return {
            "largePurchasePercent" : {"score": 90, "classAverage": 80},
            "smallPurchasePercent": {"score": 10, "classAverage": 15}
        }

def get_savings_breakdown(phone):
    return {
            "savingsScore" : {"score": 98, "classAverage": 83},
            "savingsGoal": 28
        }

def get_portfolio(phone):
    return user["portfolio"]