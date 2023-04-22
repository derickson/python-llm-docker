from fastapi import FastAPI
from pydantic import BaseModel

from lib_llm import get_llm, prompt


class InputPayload(BaseModel):
    question: str
    # template: str

app = FastAPI()
llm = get_llm()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/question")
async def question(payload: InputPayload):
    answer = prompt(payload.question) #, payload.template)
    response = {"message": f"Received prompt/question: {payload.question}", "answer": {answer}}
    print(response)
    return response