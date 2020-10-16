import requests

url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transactions/v1/transactions?accountId=rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU&hostUserId=HACKATHONUSER100"

payload = {}
headers = {
  'Authorization': 'Bearer D3SwtlumsU8iFC8PK8ao3pD3TLlH',
  'transactionId': 'fdd1542a-bcfd-439b-a6a1-5a064023b0ce',
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

