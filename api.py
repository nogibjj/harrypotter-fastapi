from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generate import generate_corpus, finish_sentence
from dataanalysis import get_freq
from DB import dynamo_micros
import uuid

app = FastAPI()


class Input(BaseModel):
    sentence: str
    n: int
    book_num: int
    text_length: int


@app.get("/")
def home():
    return {"message": "Welcome to the Harry Potter Text Generator API!"}


@app.post("/code")
def get_code():
    code = str(uuid.uuid1())[:8]
    if dynamo_micros.new_key(code):
        return code
    return {"message": "system error in storage"}


# Show the content of the corpes book in the list of 7 books
@app.get("/list-of-books/{bookid}")
def list_of_books(bookid: int):
    if bookid >= 1 and bookid <= 7:
        text_file = open("Data/Book" + str(bookid) + ".txt", "r", encoding="utf-8")
        data = text_file.read()
        text_file.close()
        data = data.replace("\n", "").replace("\r", "")
        return {"book": data}
    else:
        return {"book": "Please enter a valid book id from 1 - 7."}


@app.get("/generate-new-text/{id}")
def generate():
    return {"Generation result": id}


# Calculate the frequency of top 20 most common words for the book with ipt id
@app.get("/common-words/{bookid}")
def top_20_common_words(bookid: int):
    if bookid >= 1 and bookid <= 7:
        result = get_freq(bookid)
        return {"data": result}
    else:
        return {"message": "Please enter a valid book id from 1 - 7."}


# Generate harry potter styled text based on user input
@app.post("/text-generator/")
def text_generator(ipt: Input, code: str = ""):
    if code and not dynamo_micros.exist(code):
        return {"message": "Code is not existed"}
    corpus = generate_corpus(ipt.book_num)
    ans = finish_sentence(ipt.sentence, ipt.n, corpus, ipt.text_length)
    if code:
        # if code is not empty, store it inside DynamoDB
        dynamo_micros.insert(code, ans)
    return {"message": ans}


# Check history texts by code
@app.get("/history/{code}")
def get_history(code: str):
    if not dynamo_micros.exist(code):
        return {"message": "code is not existed"}
    data = dynamo_micros.get_texts(code)
    msg = {}
    for i, text in enumerate(data):
        msg[i] = text
    return {"message": msg}


@app.get("/history/delete/{code}/{index}")
def delete_history(code: str, index: int):
    if not dynamo_micros.exist(code):
        return {"message": "code is not existed"}
    return dynamo_micros.delete(code, index)


@app.post("/download/{code}")
async def download(code: str):
    if not dynamo_micros.exist(code):
        return {"message": "code is not existed"}
    filepath = "static/" + str(uuid.uuid1()) + "_" + code + ".txt"
    data = dynamo_micros.get_texts(code)
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(data)
    return FileResponse(filepath, filename=f"{code}.txt".format(code=code))
