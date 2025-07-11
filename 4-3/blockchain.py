from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import binascii
import json
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone

POW_DIFFICULTY = 10
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
                if format(int(self.hash(block_without_time),16),"0256b")[-POW_DIFFICULTY:] != '0'*POW_DIFFICULTY:
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
        while not format(int(self.hash(block_without_time),16),"0256b")[-POW_DIFFICULTY:] == '0'*POW_DIFFICULTY:
            block_without_time["nonce"] += 1
        block = {
            "time": datetime.now(timezone.utc).isoformat(),
            "transactions": block_without_time["transactions"],
            "hash": block_without_time["hash"],
            "nonce": block_without_time["nonce"]
        }
        self.chain["blocks"].append(block)