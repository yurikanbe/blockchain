import blockchain
import requests
import sys
import json
import node_list
import concurrent.futures

def http_get(path):
    res = requests.get(path)
    if res.status_code != 200:
        print("http request error")
        sys.exit()
    return res

if __name__ == "__main__":
    miner = "a9768f6b6b025e9674c021a1e24745093ca1cb55bd6e43ecd5dc82ebe943cc28e02537aff448948ce3e32551d884fa5f1b4cf17e70d20369c637399c05c3deb8" #Cさん
    blockchain = blockchain.BlockChain()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_node = {executor.submit(requests.get, "http://"+node+":8000/chain"): node for node in node_list.Node_List}
        max_chain_len = 0
        for future in concurrent.futures.as_completed(future_to_node):
            node = future_to_node[future]
            try:
                temp_dict = future.result().json()
                if blockchain.verify_chain(temp_dict):
                    if max_chain_len < len(temp_dict["blocks"]):
                        chain_dict = temp_dict
                        ip_address = node
                        max_chain_len = len(temp_dict["blocks"])
            except Exception as exc:
                print("%s generated an exception: %s" % (node, exc))
    print("%s is selected. Block length = %d" %(ip_address, len(chain_dict["blocks"])))

    blockchain.chain = chain_dict
    blockchain.set_all_block_transactions()

    res = http_get("http://" + ip_address + ":8000/transaction_pool")
    transaction_dict = res.json()
    transactions = transaction_dict["transactions"]

    transactions_copy = transactions.copy()
    all_block_transactions_copy = blockchain.all_block_transactions.copy()
    for transaction in transactions_copy:
        if (transaction not in all_block_transactions_copy) and blockchain.verify_transaction(transaction):
            all_block_transactions_copy.append(transaction)
        else:
            transactions.remove(transaction)

    transactions_copy = transactions.copy()
    all_block_transactions_copy = blockchain.all_block_transactions.copy()
    for transaction in transactions_copy:
        all_block_transactions_copy.append(transaction)
        if min(blockchain.account_calc(all_block_transactions_copy).values()) < 0:
            transactions.remove(transaction)
            all_block_transactions_copy.remove(transaction)

    blockchain.transaction_pool["transactions"] = transactions
    
    blockchain.create_new_block(miner)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_node = {executor.submit(requests.post, "http://"+node+":8000/chain", json.dumps(blockchain.chain)): node for node in node_list.Node_List}
        for future in concurrent.futures.as_completed(future_to_node):
            node = future_to_node[future]
            try:
                print(node + " : " + future.result().text)
            except Exception as exc:
                print("%s generated an exception: %s" % (node, exc))