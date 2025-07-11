from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import binascii
import json

class Transaction(BaseModel):
    time: str
    sender: str
    receiver: str
    amount: int
    signature: str

transaction_pool = {"transactions": []}
app = FastAPI()

@app.get("/transaction_pool")
def get_transaction_pool():
    return transaction_pool

@app.post("/transaction_pool")
def post_transaction(transaction :Transaction):
    transaction_dict = transaction.dict()
    if verify_transaction(transaction_dict):
        transaction_pool["transactions"].append(transaction_dict)
        return { "message" : "Transaction is posted."}

def verify_transaction(transaction):
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
        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)