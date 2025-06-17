
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
# import requests

app = FastAPI()

# 雛型
templates = Jinja2Templates(directory="templates")

# 静的ファイル展開
app.mount("/static", StaticFiles(directory="static"), name="static")


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

@app.get("/hello", response_class=HTMLResponse)
async def hello(request: Request, name: str = "ゲスト"):
    return templates.TemplateResponse("hello.html", {
        "request": request, "name": name
    })


class ContactForm(BaseModel):
    name: str
    message: str


@app.post("/api/contact")
async def receive_contact(form: ContactForm):
    print(f"名前: {form.name}, メッセージ: {form.message}")
    return {"status": "ok"}


class Item(BaseModel):
    name: str
    price: int


# 仮のデータベース
ITEMS_DB = [
    {"name": "りんご", "price": 100},
    {"name": "みかん", "price": 80},
    {"name": "バナナ", "price": 120},
    {"name": "りんごジュース", "price": 150}
]


@app.get("/api/search", response_model=list[Item])
def search_items(keyword: str):
    results = [item for item in ITEMS_DB if keyword in item["name"]]
    return results
