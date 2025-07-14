from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return "Hello!"

if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000)