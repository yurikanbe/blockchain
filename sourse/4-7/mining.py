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

if __name__ == "__main__":
    miner = "a9768f6b6b025e9674c021a1e24745093ca1cb55bd6e43ecd5dc82ebe943cc28e02537aff448948ce3e32551d884fa5f1b4cf17e70d20369c637399c05c3deb8" #Cさん
    ip_address = "127.0.0.1"
    blockchain = blockchain.BlockChain()

    res = http_get("http://" + ip_address+ ":8000/chain")
    chain_dict = res.json()
    blockchain.chain = chain_dict
    blockchain.set_all_block_transactions()

    res = http_get("http://" + ip_address + ":8000/transaction_pool")
    transaction_dict = res.json()
    transactions = transaction_dict["transactions"]

    transactions_copy = transactions.copy()
    all_block_transactions_copy = blockchain.all_block_transactions.copy()
    for transaction in transactions_copy:
        all_block_transactions_copy.append(transaction)
        if min(blockchain.account_calc(all_block_transactions_copy).values()) < 0:
            transactions.remove(transaction)
            all_block_transactions_copy.remove(transaction)
            
    blockchain.transaction_pool["transactions"] = transactions
    
    blockchain.create_new_block(miner)

    res = requests.post("http://" + ip_address + ":8000/chain", json.dumps(blockchain.chain))
    print(res.text)