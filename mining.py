import blockchain
import requests
import sys
import json
def http_get(path):
    res = requests.get(path)
    if res.status_code != 200:
        print("http request error")
        sys.exit()
    return res

if __name__=="__main__":
    miner="22f5509b73761a9ededf6f90220588aa4f8dea71fe8bfa097a7b793b8c4c4b5bf432439cae55910f8c6e56141efbe99406e0ec95590e39f6077e1621596c2287"
    ip_address="127.0.0.1"
    blockchain_instance = blockchain.Blockchain()

    res = http_get("http://"+ip_address+":8000/transaction_pool")
    transaction_dict = res.json()
    transactions = transaction_dict["transactions"]
    blockchain_instance.transaction_pool["transactions"] = transactions

    blockchain_instance.create_new_block(miner)

    res = requests.post("http://"+ip_address+":8000/chain",json=blockchain_instance.chain)
    print(res.text)