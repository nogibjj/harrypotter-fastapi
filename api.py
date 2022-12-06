from fastapi import FastAPI
from pydantic import BaseModel
from generate import generate_corpus, finish_sentence
from dataanalysis import get_freq

app = FastAPI()

class Input(BaseModel): 
    sentence : str
    n : int
    book_num: int
    text_length: int

@app.get("/")
def home():
    return {'message': 'Welcome to the Harry Potter Text Generator API!'}

# Show the content of the corpes book in the list of 7 books
@app.get("/list-of-books/{bookid}")
def list_of_books(bookid: int): 
    if bookid >= 1 and bookid <= 7:
        text_file = open('Data/Book' + str(bookid) + '.txt', "r", encoding="utf-8")
        data = text_file.read()
        text_file.close()
        data = data.replace("\n", "").replace("\r", "")
        return {"book" : data}
    else: 
        return {"book": "Please enter a valid book id from 1 - 7."}

@app.get("/generate-new-text/{id}")
def generate(id: int): 
    return {'Generation result': id} 

# Calculate the frequency of top 20 most common words for the book with input id
@app.get("/frequency-of-top-20-most-common-words/{bookid}")
def common_words(bookid: int): 
    if bookid >= 1 and bookid <= 7:
        result = get_freq(bookid)
        return {"data": result}
    else: 
        return {"message": "Please enter a valid book id from 1 - 7."}

# Generate harry potter styled text based on user input
@app.post("/inputs/")
def user_input(input: Input): 
    corpus = generate_corpus(input.book_num)
    ans = finish_sentence(input.sentence, input.n, corpus, input.text_length)
    return {"message": ans}
