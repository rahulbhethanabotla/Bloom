import requests
import json
from tinydb import TinyDB, Query


db = TinyDB('app/accounts/customers.json')


### username is 'HACKATHONUSER###'
### first_name is a str
### last_name is a str
### phone is a str
### savings_goal is double
### portfolio is list of ['ticker', double_val]
def create_customer(username, first_name, last_name, phone, savings_goal, portfolio):
    url = "https://gateway-staging.ncrcloud.com/cdm/consumers"

    payload = {
        "profileUsername": username,
        "firstName": first_name,
        "lastName": last_name,
        "phone": phone,
        "savingsGoal": savings_goal,
        "portfolio": portfolio
    }
    # need to remember to consistently update this
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic eb4c36d8669441f598a3f0997ab28b33',
        'nep-organization': '7d21ce6e542a4eae920f8a0e3ec248f9',
        'nep-correlation-id': '12345',
        'Date': 'Sat, 17 Oct 2020 19:05:52 GMT'
    }
    response = requests.request("POST", url, headers=headers, data=payload, auth=('da218b99-1336-45dc-8080-46f388301077', 'hackgt2020pass@'))
    
    db.insert(payload)
    


# create_customer("HACKATHONUSER074", "Tom", "Benson", "4082013554", "70.45", [["AMZN", 33.45],["MSFT", 6.32]])
# create_customer("HACKATHONUSER076", "Lila", "Carlson", "2019535950", "10.45", [["MCD", 60.45], ["ZM", 100.32], ["HON", 2.33]])
# create_customer("HACKATHONUSER126", "Kim", "Wattson", "7323109043", "7.63", [["IBM", 3.45], ["TGT",]])



### payload needs to be of form {"fieldname": newval}
### customer_username is 'HACKATHONUSER###'
def update_customer_data(payload, customer_username):
    url = "https://gateway-staging.ncrcloud.com/cdm/consumers/C7WGBO6NABQOLRHB/update"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'AccessKey eb4c36d8669441f598a3f0997ab28b33:UCptH4IXxydGDow/WDbv6laS3enbsRb+yEHPE7kIS+eZuG5VUbcJPQXSEPKphp43HYpDH+z3ubarEhHnATAciA==',
    'nep-organization': '5b16a606c8de4d7ba39af1a6e3bdae1f'
    }

    entry = Query()
    db.update(payload, entry.profileUsername == customer_username)

    response = requests.request("PUT", url, headers=headers, data = payload)


# update_customer_data({'portfolio': [('AAPL', 30.2)]}, "HACKATHONUSER107")

def get_all_customers():
    db.all()

def get_customer(username):
    customer = Query()
    print(customer)
    return db.search(customer.profileUsername == username)[0]