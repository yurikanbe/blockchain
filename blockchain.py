from ecdsa import BadSignatureError, VerifyingKey, SECP256k1
import binascii
import json
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone
import node_list
import requests 
from concurrent.futures import ThreadPoolExecutor

POW_DIFFICULTY = 10
REWARD_AMOUNT = 256
TRANSACTION_FILE = "./transaction_data.pkl"
BLOCKCHAIN_FILE = "./blockchain_data.pkl"

class Blockchain:
    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}
        self.first_block = {
            "time": "0000-00T00:00:00.000000+00:00",
            "transactions": [],
            "hash": "SimplestBlockChain",
            "previous_hash": None,
            "nonce": 0,
        }
        self.chain["blocks"].append(self.first_block)
        self.all_block_transaction = []
        self.my_address = ""

    def save_transaction_pool(self):
        pd.to_pickle(self.transaction_pool, TRANSACTION_FILE)

    def load_transaction_pool(self):
        if os.path.exists(TRANSACTION_FILE):
            transaction_data = pd.read_pickle(TRANSACTION_FILE)
            return transaction_data
        else:
            return {"transactions": []}

    def add_transaction(self, transaction):
        if self.verify_transaction(transaction):
            self.transaction_pool["transactions"].append(transaction)
            return True
        else:
            return False

    def verify_transaction(self, transaction):
        if transaction["amount"] <= 0:
            return False
        public_key = VerifyingKey.from_string(binascii.unhexlify(transaction["sender"]), curve=SECP256k1)
        signature = binascii.unhexlify(transaction["signature"])
        unsigned_transaction = {
            "time": transaction["time"],
            "sender": transaction["sender"],
            "receiver": transaction["receiver"],
            "amount": transaction["amount"]
        }
        try:
            flg = public_key.verify(signature, json.dumps(unsigned_transaction).encode('utf-8'))
            return flg
        except BadSignatureError:
            return False

    def hash(self, block):
        hash = hashlib.sha256(json.dumps(block).encode('utf-8')).hexdigest()
        return hash

    def set_all_block_transactions(self):
        self.all_block_transaction = []
        for i in range(len(self.chain["blocks"])):
            block = self.chain["blocks"][i]
            for transaction in block["transactions"]:
                self.all_block_transaction.append(transaction)

    def save_blockchain(self):
        pd.to_pickle(self.chain, BLOCKCHAIN_FILE)

    def load_blockchain(self):
        if os.path.isfile(BLOCKCHAIN_FILE):
            blockchain_data = pd.read_pickle(BLOCKCHAIN_FILE)
            return blockchain_data
        else:
            temp_chain = {"blocks": []}
            temp_chain["blocks"].append(self.first_block)
            return temp_chain

    def verify_chain(self, chain):
        all_block_transactions = []
        for i in range(len(chain["blocks"])):
            block = chain["blocks"][i]
            
            if i == 0:
                if block != self.first_block:
                    return False
            else:
                previous_block = chain["blocks"][i-1]
                if block["hash"] != self.hash(previous_block):
                    return False
                    
                block_without_time = {
                    "transactions": block["transactions"],
                    "hash": block["hash"],
                    "nonce": block["nonce"],
                }
                block_hash = self.hash(block_without_time)
                binary_hash = format(int(block_hash, 16), '0256b')
                suffix = binary_hash[-POW_DIFFICULTY:]
                required_suffix = '0' * POW_DIFFICULTY
                
                if suffix != required_suffix:
                    return False
                    
            reward_trans_fig = False
            for transaction in block["transactions"]:
                if transaction["sender"] == "Blockchain":
                    if not reward_trans_fig:
                        reward_trans_fig = True
                    else:
                        return False
                    if transaction["amount"] != REWARD_AMOUNT:
                        return False
                else:
                    if self.verify_transaction(transaction) == False:
                        return False
                if transaction not in all_block_transactions:
                    all_block_transactions.append(transaction)
                else:
                    return False
                if all_block_transactions != []:
                    if min(self.account_calc(all_block_transactions).values()) < 0:
                        return False
        return True

    def replace_chain(self, chain):
        self.chain = chain
        self.set_all_block_transactions()
        for transaction in self.all_block_transaction:
            if transaction in self.transaction_pool["transactions"]:
                self.transaction_pool["transactions"].remove(transaction)
    
    def create_new_block(self, miner):
        reward_transaction = {
            "time":datetime.now(timezone.utc).isoformat(),
            "sender":"Blockchain",
            "receiver":miner,
            "amount":REWARD_AMOUNT,
            "signature":"none"
        }
        transaction = self.transaction_pool["transactions"].copy()
        transaction.append(reward_transaction)
        last_block = self.chain["blocks"][-1]
        hash = self.hash(last_block)
        block_without_time = {
            "transactions":transaction,
            "hash":hash,
            "nonce":0,
        }
        while not format(int(self.hash(block_without_time),16),'0256b')[-POW_DIFFICULTY:] == '0'*POW_DIFFICULTY:
            block_without_time["nonce"] += 1
        block = {
            "time":datetime.now(timezone.utc).isoformat(),
            "transactions":block_without_time["transactions"],
            "hash":block_without_time["hash"],
            "nonce":block_without_time["nonce"],
        }
        self.chain["blocks"].append(block)


    def account_calc(self,transactions):
        accounts={}
        transactions_copy = transactions.copy()
        for transaction in transactions_copy:
            # sender側の計算（Blockchainの場合はスキップ）
            if transaction["sender"] != "Blockchain":
                if transaction["sender"] not in accounts:
                    accounts[transaction["sender"]] = int(0)
                accounts[transaction["sender"]] -= int(transaction["amount"])
            
            # receiver側の計算（すべてのトランザクションで実行）
            if transaction["receiver"] not in accounts:
                accounts[transaction["receiver"]] = int(0)
            accounts[transaction["receiver"]] += int(transaction["amount"])
        return accounts
    
    def get_my_address(self):
        try:
            # 汎用的な外部サービスを使用（AWS/GCP/ローカル全対応）
            response = requests.get("https://api.ipify.org", timeout=5)
            self.my_address = response.text
        except:
            # エラー時はローカルホストにフォールバック
            self.my_address = "127.0.0.1"

    def broadcast_transaction(self,transaction):
        with ThreadPoolExecutor() as executor:
            for url in node_list.node_list:
                if url != self.my_address:
                    executor.submit(requests.post,f"http://{url}:8000/receive_tranaction",json.dumps(transaction))