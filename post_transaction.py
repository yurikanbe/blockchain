import requests
import pandas as pd
import datetime
from ecdsa import SigningKey, SECP256k1
import binascii
import json

coin_num=3
secret_key_sender_str="547c287895cb17b5c5180818c1cf7c7f40dc5800e8a1c83651e70e275c3a9f5b"
public_key_receiver_str="22f5509b73761a9ededf6f90220588aa4f8dea71fe8bfa097a7b793b8c4c4b5bf432439cae55910f8c6e56141efbe99406e0ec95590e39f6077e1621596c2287"

secret_key_sender=SigningKey.from_string(binascii.unhexlify(secret_key_sender_str),curve=SECP256k1)
public_key_sender=secret_key_sender.verifying_key
public_key_sender_str=public_key_sender.to_string().hex()
time_now=datetime.datetime.now(datetime.timezone.utc).isoformat()
unsigned_transaction={"time":time_now,"sender":public_key_sender_str,"receiver":public_key_receiver_str,"amount":coin_num}
signature=secret_key_sender.sign(json.dumps(unsigned_transaction).encode('utf-8'))
transaction={"time":time_now,"sender":public_key_sender_str,"receiver":public_key_receiver_str,"amount":coin_num,"signature":signature.hex()}

res=requests.post("http://34.56.171.147:8000/transaction_pool",json.dumps(transaction))
print(res.text)

pd.to_pickle(transaction,"signed_transaction.pkl")