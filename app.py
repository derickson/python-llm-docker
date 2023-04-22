from fastapi import FastAPI
from lib_llm import get_llm

app = FastAPI()
llm = get_llm()

@app.get("/")
async def root():
    return {"message": "Hello World"}