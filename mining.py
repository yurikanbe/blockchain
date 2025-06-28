import blockchain
import requests
import sys
import json
def http_get(path):
    res = requests.get( path)
    if res.status_code != 200:
        print("http request error")
        sys.exit()
    return res

if __name__=="__main__":
    miner=""
    ip_address="127.0.0.1"
    blockchain = blockchain.BlockChain()

    res = http_get("http://"+ip_address+":8000/transaction_pool")
    transaction_dict = res.json()
    transactions = transaction_dict["transactions"]
    blockchain.transaction_pool["transactions"] = transactions

    blockchain.create_new_block(miner)

    res = requests.post("http://"+ip_address+":8000/chain",json=blockchain.chain)
    print(res.text)