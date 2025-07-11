from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import blockchain

class Transaction(BaseModel):
    time: str
    sender: str
    receiver: str
    amount: int
    signature: str

blockchain = blockchain.BlockChain()
blockchain.transaction_pool = blockchain.load_transaction_pool()
app = FastAPI()

@app.get("/transaction_pool")
def get_transaction_pool():
    return blockchain.transaction_pool

@app.post("/transaction_pool")
def post_transaction(transaction :Transaction):
    transaction_dict = transaction.dict()
    if blockchain.verify_transaction(transaction_dict):
        if blockchain.add_transaction_pool(transaction_dict):
             blockchain.save_transaction_pool()
             return { "message" : "Transaction is posted."}
        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)