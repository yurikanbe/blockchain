from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import binascii
import json
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone
import node_list
import requests
from concurrent.futures import ThreadPoolExecutor

POW_DIFFICULTY_ORIGIN = 18
POW_CHANGE_BLOCK_NUM = 10
POW_TARGET_SEC = 10
REWARD_AMOUNT = 256
TRANSACTION_FILE = "./transaction_data.pkl"
BLOCKCHAIN_FILE = "./chain_data.pkl"

class BlockChain(object):
    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}
        self.first_block = {
            "time": "0000-00-00T00:00:00.000000+00:00",
            "transactions": [],
            "hash": "SimplestBlockChain",
            "nonce": 0
        }
        self.chain["blocks"].append(self.first_block)
        self.all_block_transactions = []
        self.my_address = ""
        self.current_pow_difficulty = POW_DIFFICULTY_ORIGIN

    def save_transaction_pool(self):
        pd.to_pickle(self.transaction_pool, TRANSACTION_FILE)

    def load_transaction_pool(self):
        if os.path.isfile(TRANSACTION_FILE):
            transaction_data = pd.read_pickle(TRANSACTION_FILE)
            return transaction_data
        else:
            return {"transactions": []}
        
    def add_transaction_pool(self, transaction):
        if (transaction not in self.all_block_transactions) and (transaction not in self.transaction_pool["transactions"]):
            self.transaction_pool["transactions"].append(transaction)
            return True
        else:
            return False
        
    def verify_transaction(self, transaction):
        if transaction["amount"] < 0:
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
        self.all_block_transactions = []
        for i in range(len(self.chain["blocks"])):
            block = self.chain["blocks"][i]
            for trans in block["transactions"]:
                self.all_block_transactions.append(trans)

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
        current_pow_difficulty = POW_DIFFICULTY_ORIGIN
        for i in range(len(chain["blocks"])):
            block = chain["blocks"][i]
            previous_block = chain["blocks"][i-1]
            if i == 0:
                if block != self.first_block:
                    return False
            else:
                if block["hash"] != self.hash(previous_block):
                    return False
                block_without_time = {
                    "transactions": block["transactions"],
                    "hash": block["hash"],
                    "nonce": block["nonce"]
                }
                current_pow_difficulty = self.get_pow_difficulty(chain["blocks"][:i], current_pow_difficulty)
                if format(int(self.hash(block_without_time),16),"0256b")[-current_pow_difficulty:] != '0'*current_pow_difficulty:
                    return False
                reward_trans_flg = False
                for transaction in block["transactions"]:
                    if transaction["sender"] == "Blockchain":
                        if reward_trans_flg == False:
                             reward_trans_flg = True
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
        self.current_pow_difficulty = current_pow_difficulty
        return True
          
    def replace_chain(self, chain):       
        self.chain = chain
        self.set_all_block_transactions()
        for transaction in self.all_block_transactions:
            if transaction in self.transaction_pool["transactions"]:
                self.transaction_pool["transactions"].remove(transaction)

    def create_new_block(self, miner):
        reward_transaction = {
            "time": datetime.now(timezone.utc).isoformat(),
            "sender": "Blockchain",
            "receiver": miner,
            "amount": REWARD_AMOUNT,
            "signature": "none"
        }
        transactions = self.transaction_pool["transactions"].copy()
        transactions.append(reward_transaction)
        last_block = self.chain["blocks"][-1]
        hash = self.hash(last_block)
        block_without_time = {
            "transactions": transactions,
            "hash": hash,
            "nonce": 0
        }
        self.current_pow_difficulty = self.get_pow_difficulty(self.chain["blocks"], self.current_pow_difficulty)
        while not format(int(self.hash(block_without_time),16),"0256b")[-self.current_pow_difficulty:] == '0'*self.current_pow_difficulty:
            block_without_time["nonce"] += 1
        block = {
            "time": datetime.now(timezone.utc).isoformat(),
            "transactions": block_without_time["transactions"],
            "hash": block_without_time["hash"],
            "nonce": block_without_time["nonce"]
        }
        self.chain["blocks"].append(block)

    def account_calc(self, transactions):
        accounts = {}
        transactions_copy = transactions.copy()
        for transaction in transactions_copy:
            if transaction["sender"] != "Blockchain":
                if transaction["sender"] not in accounts:
                    accounts[transaction["sender"]] = int(0)
                accounts[transaction["sender"]] -= int(transaction["amount"])
            if transaction["receiver"] not in accounts:
                accounts[transaction["receiver"]] = int(0)
            accounts[transaction["receiver"]] += int(transaction["amount"])
        return accounts
    
    def get_my_address(self):
        self.my_address = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").text
    
    def broadcast_transaction(self, transaction):
        with ThreadPoolExecutor() as executor:
            for url in node_list.Node_List:
                if url != self.my_address:
                    executor.submit(requests.post, "http://"+url+":8000/receive_transaction", json.dumps(transaction))

    def get_pow_difficulty(self, blocks, current_pow_difficulty):
        ix = len(blocks) - 1
        if (ix-1) % POW_CHANGE_BLOCK_NUM == 0 and 1 < ix:
            all_time = 0
            for i in range(POW_CHANGE_BLOCK_NUM):
                all_time += (datetime.fromisoformat(blocks[ix-i]["time"]) - datetime.fromisoformat(blocks[ix-i-1]["time"])).total_seconds()
            if all_time / POW_CHANGE_BLOCK_NUM < POW_TARGET_SEC / 2:
                current_pow_difficulty += 1
            if 1 < current_pow_difficulty and POW_TARGET_SEC * 2 < all_time / POW_CHANGE_BLOCK_NUM:
                current_pow_difficulty -= 1
        return current_pow_difficulty