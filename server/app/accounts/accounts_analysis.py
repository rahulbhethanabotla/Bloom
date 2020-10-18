from app.accounts import ncr_banking_api_requests
from app.accounts import customer_data_management

import json
import os
known_numbers = {
    "4048842018":  "HACKATHONUSER001",
    "4082013554": "HACKATHONUSER074",
    "2019535950": "HACKATHONUSER076",
    "7323109043": "HACKATHONUSER126"
}
user_accounts = dict()

print(os.getcwd())
with open("app/accounts/user_accounts.json") as json_file:
    user_accounts = json.load(json_file)

income_quintiles = [1019.666667, 2745.416667,
                    4426.916667, 6988.666667, 14564.75]
expenditure_quintiles = [2389.333333, 3372.666667,
                         4420.416667, 5931.083333, 10130.91667]


def get_username(phone):
    if phone in known_numbers:
        username = known_numbers[phone]
    else:
        username = "HACKATHONUSER001"
    return username


def display_accounts():
    for number in known_numbers.keys():
        print("NUMBER: ", number)
        username = get_username(number)
        checkings = get_checkings_stats(number)
        savings = get_savings_stats(number)
        print("CHECKINGS TRANSACTIONS: ", [t["amount"]
                                           for t in checkings["transactions"]])
        print("SAVINGS TRANSACTIONS: ", [t["amount"]
                                         for t in savings["transactions"]])
        print("CHECKINGS BALANCE/EXPENDITURES: ",
              checkings["balance"], checkings["expenditures"])
        print(savings)
        print("SAVINGS BALANCE/SAVINGS: ",
              savings["balance"], savings["savings"])


def set_up_accounts(phone):
    username = get_username(phone)
    account_response = ncr_banking_api_requests.get_specific_account_for_user(
        username, "CHECKING")
    id_string = account_response["id"]
    balance = account_response["currentBalance"]["amount"]
    transactions_dict = ncr_banking_api_requests.get_transactions_for_specific_user_account_type(
        "HACKATHONUSER001", "CHECKING")["transactions"]
    transactions = [{"date": t["transactionDate"],
                     "amount": t["amount"]["amount"]} for t in transactions_dict]
    expenditures = sum([t["amount"] for t in transactions])

    user_accounts[username] = {
        "checkings": {
            "id": id_string,
            "balance": balance,
            "transactions": transactions,
            "expenditures": expenditures
        }}

    account_response = ncr_banking_api_requests.get_specific_account_for_user(
        username, "TCL_MASTER")
    id_string = account_response["id"]
    balance = account_response["currentBalance"]["amount"]
    transactions_dict = ncr_banking_api_requests.get_transactions_for_specific_user_account_type(
        "HACKATHONUSER001", "CHECKING")["transactions"]
    transactions = [{"date": t["transactionDate"],
                     "amount": t["amount"]["amount"]} for t in transactions_dict]
    savings = sum([t["amount"] for t in transactions])
    balance += savings
    user_accounts[username]["savings"] = {
        "id": id_string,
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
    return user_accounts[get_username(phone)]["savings"]


def quintile_position(arr, num):
    result = 0
    for q in arr:
        if q < num:
            result += 1
    return result


def get_category(phone):
    income = get_savings_stats(phone)["income"]
    spending = get_checkings_stats(phone)["expenditures"]

    return {
        "incomeClass": quintile_position(income_quintiles, income),
        "spendingClass": quintile_position(expenditure_quintiles, spending),
    }


def get_purchase_breakdown(phone):
    purchases = get_checkings_stats(phone)["transactions"]
    purchases = [t["amount"] for t in purchases]

    purchases = sorted(purchases)

    large = sum(purchases[int(.75*len(purchases)):])
    small = sum(purchases[: int(.25*len(purchases))])
    total = sum(purchases)
    return {
        "largePurchasePercent": {"score": (100 * large) / total, "classAverage": 85},
        "smallPurchasePercent": {"score": (100 * small) / total, "classAverage": 15}
    }


def get_savings_breakdown(phone):
    income = get_savings_stats(phone)["income"]
    spending = get_checkings_stats(phone)["expenditures"]
    savings = income - spending
    score = min(((savings / income) / .20) * 100, 100)

    return {
        "monthlySavings": savings,
        "savingsScore": {"score": score, "classAverage": 83},
        "savingsGoal": 28
    }


def get_portfolio(phone):
    print(get_username(phone))
    customer_data = customer_data_management.get_customer(get_username(phone))
    print(customer_data)
    return {"portfolio": customer_data["portfolio"]}


def get_full_name(phone):
    # query the ncr buisness api to get name
    customer_data = customer_data_management.get_customer(get_username(phone))
    return {"firstName": customer_data["firstName"], "lastName": customer_data["lastName"]}
