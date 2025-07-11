import pandas as pd
from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import binascii
import json

transaction = pd.read_pickle("signed_transaction.pkl")
public_key_A = VerifyingKey.from_string(binascii.unhexlify(transaction["sender"]), curve=SECP256k1)
signature = binascii.unhexlify(transaction["signature"])

unsigned_transaction = { 
    "time": transaction["time"], 
    "sender": transaction["sender"], 
    "receiver": transaction["receiver"], 
    "amount": transaction["amount"] 
}

try:
    public_key_A.verify(signature, json.dumps(unsigned_transaction).encode('utf-8'))
    print("トランザクションは改ざんされていません。")
except BadSignatureError:
    print("トランザクションが改ざんされています。")