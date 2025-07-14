import pandas as pd

transaction = pd.read_pickle("signed_transaction.pkl")
print("改ざん前のトランザクション：")
print(transaction)
transaction = { "time": transaction["time"], "sender": transaction["sender"], "receiver": transaction["receiver"], "amount": 30 , "signature": transaction["signature"]}
print("改ざん後のトランザクション：")
print(transaction)
pd.to_pickle(transaction, "signed_transaction.pkl")