import requests
import json

CHCEK_URL = "https://oqty2e65b9.execute-api.us-east-1.amazonaws.com/prod/hp_text/id"
UPDATE_URL = "https://oqty2e65b9.execute-api.us-east-1.amazonaws.com/prod/hp_text"
FETCH_URL = "https://oqty2e65b9.execute-api.us-east-1.amazonaws.com/prod/hp_text"


def _update(tid, array):
    while True:
        resp = requests.post(UPDATE_URL, json={"id": tid, "texts": array}, timeout=60)
        if resp.json().get("statusCode", 0) == 200:
            return resp.json().get("body", "")


def new_key(tid):
    _update(tid, [])
    return True


def exist(tid):
    req = requests.get(CHCEK_URL, params={"id": tid}, timeout=60)
    return req.json()


def insert(tid, text):
    data = _get_data(tid)
    data.append(text)
    return _update(tid, data)


def _get_data(tid):
    req = requests.get(FETCH_URL, params={"id": tid}, timeout=60)
    data = json.loads(req.text)
    return data


def get_texts(tid):
    return _get_data(tid)


# delete based on index and code
def delete(tid, index):
    data = _get_data(tid)
    if len(data) <= index or index < 0:
        return "Invalid Operation"
    data.pop(index)
    return _update(tid, data)


if __name__ == "__main__":
    print(exist("test"))
    print(get_texts("test"))
    print(new_key("hello world123"))
    print(insert("test", "hello"))
    print(get_texts("test"))
    print(delete("test", 1))
    print(get_texts("test"))
