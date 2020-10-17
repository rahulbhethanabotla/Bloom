import requests
import json
import time

#########################################################################################################################
# user_id:  written as HACKATHONUSER*** from 100 to 299 (101 doesn't seem to work for some reason?)


def get_user_accounts(user_id):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts?hostUserId=" + \
        str(user_id)

    payload = {}
    # need to remember to consistently update this
    headers = {
        'Authorization': 'Bearer 18MjUvvObCANTdpwsKIwVGY63UVA',
        'transactionId': 'dcb9f3bb-f8a1-4002-a1a2-acf049c8bac0',
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)
    return response.json()
#########################################################################################################################

#########################################################################################################################

def get_account_id_from_accounts(response):
    return response['accounts'][0]['id']

#########################################################################################################################
def get_user_account(account_id, user_id):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts/" + \
        str(account_id) + "?hostUserId=" + str(user_id)
    payload = {}
    headers = {
        'Authorization': 'Bearer 18MjUvvObCANTdpwsKIwVGY63UVA',
        'transactionId': 'dcb9f3bb-f8a1-4002-a1a2-acf049c8bac0',
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()
#########################################################################################################################

#########################################################################################################################
# account_id is the first value in each entry in the list of accounts generated by get_user_accounts


def get_transactions_from_account(account_id, user_id):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transactions/v1/transactions?accountId=" + \
        str(account_id) + "&hostUserId=" + str(user_id)
    payload = {}
    headers = {
        'Authorization': 'Bearer 18MjUvvObCANTdpwsKIwVGY63UVA',
        'transactionId': 'dcb9f3bb-f8a1-4002-a1a2-acf049c8bac0',
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

#########################################################################################################################

#########################################################################################################################

def get_all_transactions_for_a_user(user_id):
    all_transacs = dict()
    all_transacs["all_transactions"] = []
    for user_account in get_user_accounts(user_id)['accounts']:
        account_id = user_account['id']
        transactions_for_acct = get_transactions_from_account(account_id, user_id)
        all_transacs["all_transactions"] += [transactions_for_acct]
    return json.dumps(all_transacs)

#########################################################################################################################

#########################################################################################################################

def get_all_transactions_for_all_users():
    all_user_transactions = dict()
    all_user_transactions["transactions"] = []
    user_id = "HACKATHONUSER"
    for i in range(300):
        user_id += str(i).zfill(3)
        user_transactions = dict()
        user_transactions[user_id] = get_all_transactions_for_a_user(user_id)
        all_user_transactions["transactions"] += user_transactions
    return all_user_transactions


# print(get_all_transactions_for_all_users())
print(get_user_accounts("HACKATHONUSER00"))
print(get_user_accounts("HACKATHONUSER101"))