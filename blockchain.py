from ecdsa import BadSignatureError, VerifyingKey, SECP256k1
import binascii
import json
import pandas as pd
import os
import hashlib
from datetime import datetime, timezone

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