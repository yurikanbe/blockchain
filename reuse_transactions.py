import requests
import json

path = "http://127.0.0.1:5000/transaction_pool"
res = requests.get(path)
transactions_dict = res.json()
received_transactions = transactions_dict["transactions"][0]

res = requests.post(path,json.dumps(received_transactions))
print(res.json())