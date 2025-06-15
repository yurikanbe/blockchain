from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import binascii
import json

class Transaction(BaseModel):
    time:str
    sender:str
    receiver:str
    amount:int
    signature:str

transacton_pool={"transactions":[]}
app=FastAPI()

@app.get("/transaction_pool")
def get_transaction_pool():
    return transacton_pool

@app.post("/transaction_pool")
def post_transaction_pool(transaction:Transaction):
    transaction_dict = transaction.dict()
    if verify_transaction(transaction_dict):
        transacton_pool["transactions"].append(transaction_dict)
        return {"massage":"Transaction is posted."}
    
def verify_transaction(transaction):
    public_key=VerifyingKey.from_string(binascii.unhexlify(transaction["sender"]),curve=SECP256k1)
    signature=binascii.unhexlify(transaction["signature"])
    unsigned_transaction = {
        "time":transaction["time"],
        "sender":transaction["sender"],
        "receiver":transaction["receiver"],
        "amount":transaction["amount"]
    }
    try:
        fig = public_key.verify(signature,json.dumps(unsigned_transaction).encode('utf-8'))
        return fig
    except BadSignatureError:
        return False

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)