import requests

res = requests.get("http://127.0.0.1:5000/transaction_pool")
transactions_dict = res.json()
print(transactions_dict["transactions"])