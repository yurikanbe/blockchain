import blockchain
import requests
import json

blockchain = blockchain.BlockChain()
blockchain.chain = requests.get("http://127.0.0.1:8000/chain").json()
blockchain.set_all_block_transactions()
print( blockchain.account_calc(blockchain.all_block_transactions) )