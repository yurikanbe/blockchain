import requests
import pandas as pd
from datetime import datetime, timezone
from ecdsa import SigningKey, SECP256k1
import binascii
import json
import node_list
import base64

def send_transaction(secret_key_sender_str, public_key_receiver_str, coin_num, nft_data, nft_origin):
    secret_key_sender = SigningKey.from_string(binascii.unhexlify(secret_key_sender_str), curve=SECP256k1)
    public_key_sender = secret_key_sender.verifying_key
    public_key_sender_str = public_key_sender.to_string().hex()
    time_now = datetime.now(timezone.utc).isoformat()
    unsigned_transaction = { "time": time_now, "sender": public_key_sender_str, "receiver": public_key_receiver_str, "amount": coin_num, "nft_data": nft_data, "nft_origin": nft_origin }
    signature = secret_key_sender.sign(json.dumps(unsigned_transaction).encode('utf-8'))
    transaction = { "time": time_now, "sender": public_key_sender_str, "receiver": public_key_receiver_str, "amount": coin_num, "nft_data": nft_data, "nft_origin": nft_origin, "signature": signature.hex()}

    res = requests.post("http://" + node_list.Node_List[0] + ":8000/transaction_pool", json.dumps(transaction)) 
    print(res.text)

if __name__ == "__main__":
    coin_num = 0
    secret_key_sender_strA = "76f0446638f57dc78fe154f452b9a14d73b2a55d729311ec8cf482883027b05d"#Aさん
    public_key_receiver_strC = "a9768f6b6b025e9674c021a1e24745093ca1cb55bd6e43ecd5dc82ebe943cc28e02537aff448948ce3e32551d884fa5f1b4cf17e70d20369c637399c05c3deb8"#Cさん
    with open("./lerda.jpg", "rb") as f:
        img = f.read()
        NFT = base64.b64encode(img).decode('utf-8')
    
    send_transaction(secret_key_sender_strA, public_key_receiver_strC, coin_num, NFT, "")