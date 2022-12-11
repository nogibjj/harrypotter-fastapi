# test api.py
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Harry Potter Text Generator API!"
    }


def test_get_code():
    response = client.post("/code")
    assert response.status_code == 200
    assert len(response.json()) == 8


def test_list_of_books():
    response = client.get("/list-of-books/1")
    assert response.status_code == 200
    assert len(response.json()["book"]) > 0


def test_generate():
    response = client.get("/generate-new-text/1")
    assert response.status_code == 200
    assert len(response.json()["Generation result"]) > 0


def test_top_20_common_words():
    response = client.get("/common-words/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


def test_generate_text():
    response = client.post(
        "/generate-text",
        json={"sentence": "Harry Potter", "n": 5, "book_num": 1, "text_length": 100},
    )
    assert response.status_code == 200
    assert len(response.json()["text"]) > 0


def test_hisotry():
    response = client.post("/history", json={"code": "1234567"})
    assert response.status_code == 200
    assert len(response.json()["history"]) > 0
