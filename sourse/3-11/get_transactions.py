import requests

res = requests.get("http://xxx.xxx.xxx.xxx:8000/transaction_pool")
transactions_dict = res.json()
print(transactions_dict["transactions"])