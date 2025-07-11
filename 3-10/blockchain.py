from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import binascii
import json
import pandas as pd
import os

TRANSACTION_FILE = "./transaction_data.pkl"

class BlockChain(object):
    def __init__(self):
        self.transaction_pool = {"transactions": []}
        
    def save_transaction_pool(self):
        pd.to_pickle(self.transaction_pool, TRANSACTION_FILE)

    def load_transaction_pool(self):
        if os.path.isfile(TRANSACTION_FILE):
            transaction_data = pd.read_pickle(TRANSACTION_FILE)
            return transaction_data
        else:
            return {"transactions": []}
        
    def add_transaction_pool(self, transaction):
        if transaction not in self.transaction_pool["transactions"]:
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