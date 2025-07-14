from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import blockchain
from typing import List

class Transaction(BaseModel):
    time: str
    sender: str
    receiver: str
    amount: int
    signature: str

class Block(BaseModel):
    time: str
    transactions: List[Transaction]
    hash: str
    nonce: int

class Chain(BaseModel):
    blocks: List[Block]

blockchain = blockchain.BlockChain()
blockchain.transaction_pool = blockchain.load_transaction_pool()
blockchain.chain = blockchain.load_blockchain()
blockchain.set_all_block_transactions()
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

@app.get("/chain")
def get_chain():
    return blockchain.chain

@app.post("/chain")
def post_chain(chain: Chain):
    chain_dict = chain.dict()
    if len(chain_dict["blocks"]) <= len(blockchain.chain["blocks"]):
        return { "message" : "Received chain is ignored."}
    if blockchain.verify_chain(chain_dict):
        blockchain.replace_chain(chain_dict)
        blockchain.save_blockchain()
        blockchain.save_transaction_pool()
        return { "message" : "Chain is posted."}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)