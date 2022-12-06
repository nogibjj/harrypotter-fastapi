from fastapi import FastAPI
import gunicorn
import uvicorn
from pydantic import BaseModel
from generate import generate_corpus, finish_sentence

app = FastAPI()

class Input(BaseModel): 
    sentence : str
    n : int
    book_num: int
    text_length: int

@app.get("/")
def home():
    return {'Welcome to the Harry Potter Text Generator API!'}

@app.get("/generate/{text}")
def generate(text: str): 
    return {'Generation result': text} 


@app.post("/inputs/")
def user_input(input: Input): 
    corpus = generate_corpus(input.book_num)
    ans = finish_sentence(input.sentence, input.n, corpus, input.text_length)
    return {"status": ans}
