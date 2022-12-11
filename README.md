# harrypotter-fastapi

The project is a **Markov Text Generator** based on the seven Harry Potter Books Corpora. 

The original dataset can be found on kaggle from [here](https://www.kaggle.com/datasets/balabaskar/harry-potter-books-corpora-part-1-7).

## 7 Harry Potter Books

Book1: Harry Potter and the Philosophers Stone

Book2: Harry Potter and the Chamber of Secrets

Book3: Harry Potter and the Prisoner of Azkaban

Book4: Harry Potter and the Goblet of Fire

Book5: Harry Potter and the Order of the Phoenix

Book6: Harry Potter and the Half Blood Prince

Book7: Harry Potter and the Deathly Hallows

## FastAPI
The FastAPI to the example app is described below.

### Request

`get("/")`


### Response

    INFO:     Will watch for changes in these directories: ['/workspaces/harrypotter-fastapi']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [6597] using StatReload
    [nltk_data] Downloading package stopwords to
    [nltk_data]     /home/codespace/nltk_data...
    [nltk_data]   Package stopwords is already up-to-date!
    INFO:     Started server process [6605]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     71.70.176.67:0 - "GET / HTTP/1.1" 200 OK

    "message": "Welcome to the Harry Potter Text Generator API!"

### Show the content of the corpes book in the list of 7 books

`get("/list-of-books/{bookid}")`

    curl -X 'GET' \
        'https://ultraviolet0909-solid-invention-xxrrxrvjwvjh9g77-8000.preview.app.github.dev/list-of-books/1' \
        -H 'accept: application/json'

### Response 
    INFO:     71.70.176.67:0 - "GET / HTTP/1.1" 200 OK
    INFO:     71.70.176.67:0 - "GET /docs HTTP/1.1" 200 OK
    INFO:     71.70.176.67:0 - "GET /openapi.json HTTP/1.1" 200 OK
    INFO:     71.70.176.67:0 - "GET /list-of-books/1 HTTP/1.1" 200 OK

    if bookid >= 1 and bookid <= 7:
            return {"book": data}
        else:
            return {"book": "Please enter a valid book id from 1 - 7."}

### Calculate the frequency of top 20 most common words for the book with ipt id

`get("/common-words/{bookid}")`

    curl -X 'GET' \
        'https://ultraviolet0909-solid-invention-xxrrxrvjwvjh9g77-8000.preview.app.github.dev/common-words/1' \
        -H 'accept: application/json'

### Response 
    INFO:     71.70.176.67:0 - "GET /common-words/1 HTTP/1.1" 200 OK

    if bookid >= 1 and bookid <= 7:
            return {"data": result}
        else:
            return {"book": "Please enter a valid book id from 1 - 7."}

### Generate harry potter styled text based on user input

`post("/text-generator/")`

    curl -X 'POST' \
        'https://ultraviolet0909-solid-invention-xxrrxrvjwvjh9g77-8000.preview.app.github.dev/text-generator/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "sentence": "hello world",
        "n": 2,
        "book_num": 1,
        "text_length": 10
        }'
### Response
    INFO:     71.70.176.67:0 - "POST /text-generator/ HTTP/1.1" 200 OK

    {
        "message": "hello world knows nothin’ i was nothing next passageway. “what"
    }