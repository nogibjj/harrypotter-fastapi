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


def test_top_20_common_words():
    response = client.get("/common-words/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


def test_hisotry():
    response = client.get("/history/1234567")
    assert response.status_code == 200
    assert len(response.json()["message"]) > 0
