from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import binascii
import json
import blockchain

class Transaction(BaseModel):
    time:str
    sender:str
    receiver:str
    amount:int
    signature:str

blockchain=blockchain.Blockchain()
blockchain.transacton_pool = blockchain.load_transaction_pool()
app=FastAPI()

@app.get("/")
def root():
    return {"message": "Blockchain API", "endpoints": ["/transaction_pool"]}

@app.get("/transaction_pool")
def get_transaction_pool():
    return blockchain.transacton_pool

@app.post("/transaction_pool")
def post_transaction_pool(transaction:Transaction):
    transaction_dict = transaction.dict()
    if blockchain.verify_transaction(transaction_dict):
        if blockchain.add_transaction(transaction_dict):
            blockchain.save_transaction_pool()
            return {"massage":"Transaction is posted."}
    return {"message": "Transaction verification failed."}

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)