
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
# import requests

app = FastAPI()


# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


# GET パラメータを受け取る
@app.get("/greet")
def greet(name: str):
    return {"message": f"こんにちは {name} さん"}


# POST で JSON を受け取る
class Item(BaseModel):
    name: str
    price: float


@app.post("/items")
def create_item(item: Item):
    return {"received": item}


# クエリパラメータのバリデーション
@app.get("/search")
def search(keyword: str = Query(..., min_length=2)):
    return {"keyword": keyword}


# パスパラメータのバリデーションと例外処理
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return {"item_id": item_id}


# 外部API呼び出し（例：天気情報取得）
# 試してみたい人はAPIキーを取得して各自で取得してください。
# @app.get("/weather")
# def get_weather(city: str):
#     url = f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}"
#     res = requests.get(url)
#     return res.json()
