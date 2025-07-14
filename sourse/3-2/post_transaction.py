import requests
import pandas as pd
import datetime
from ecdsa import SigningKey, SECP256k1
import binascii
import json

coin_num = 3
secret_key_sender_str = "76f0446638f57dc78fe154f452b9a14d73b2a55d729311ec8cf482883027b05d"
public_key_receiver_str = "f37996d4748fd4ccd58bb00fe73a3636ea1c6600a25a4a1bb22627b01d274d7ce1d717c7e9b79394c8a260e2337f1d8eac78b66f94bbdebddd5804fb8e0369b1"

secret_key_sender = SigningKey.from_string(binascii.unhexlify(secret_key_sender_str), curve=SECP256k1)
public_key_sender = secret_key_sender.verifying_key
public_key_sender_str = public_key_sender.to_string().hex()
time_now = datetime.datetime.now(datetime.timezone.utc).isoformat()
unsigned_transaction = { "time": time_now, "sender": public_key_sender_str, "receiver": public_key_receiver_str, "amount": coin_num }
signature = secret_key_sender.sign(json.dumps(unsigned_transaction).encode('utf-8'))
transaction = { "time": time_now, "sender": public_key_sender_str, "receiver": public_key_receiver_str, "amount": coin_num , "signature": signature.hex()}

res = requests.post("http://xxx.xxx.xxx.xxx:8000/transaction_pool", json.dumps(transaction)) 
print(res.text)