from fastapi import FastAPI
import gunicorn
import uvicorn
import uuid 
import io 
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
    return {'Message': 'Welcome to the Harry Potter Text Generator API!'}

@app.get("/list-of-books/{bookid}")
def list_of_books(bookid: int): 
    if bookid >= 1 and bookid <= 7:
        text_file = open('Data/Book' + str(bookid) + '.txt', "r", encoding="utf-8")
        data = text_file.read().strip()
        text_file.close()
        return {"book" : data}
    else: 
        return {"book": "Please enter a valid book id from 1 - 7."}


@app.get("/generate-new-text/{id}")
def generate(id: int): 
    return {'Generation result': id} 


@app.post("/inputs/")
def user_input(input: Input): 
    corpus = generate_corpus(input.book_num)
    ans = finish_sentence(input.sentence, input.n, corpus, input.text_length)
    return {"status": ans}
