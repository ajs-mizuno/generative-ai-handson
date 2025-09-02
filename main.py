
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
# staticフォルダに配置しているHTMLとブラウザのURLを直接紐づける
# http://127.0.0.1:8000/static/basic.html
# http://127.0.0.1:8000/static/query.html
# http://127.0.0.1:8000/static/search.html
app.mount("/static", StaticFiles(directory="static"), name="static")

###############################################################################
# 基本的な書き方
###############################################################################


# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


# GET パラメータを受け取る
@app.get("/greet")
def greet(name: str):
    return {"message": f"こんにちは {name} さん"}


###############################################################################
# 画面と紐づけたWebサービスの実装方法
###############################################################################

# 画面に用意した入力項目のデータ型
class ContactForm(BaseModel):
    name: str
    message: str


# 画面から送信されたデータを次の画面に表示する
@app.get("/hello", response_class=HTMLResponse)
async def hello(request: Request, name: str = "ゲスト"):
    return templates.TemplateResponse("hello.html", {
        "request": request, "name": name
    })


# 画面入力したデータを確認する
@app.post("/api/contact")
async def receive_contact(form: ContactForm):
    print(f"名前: {form.name}, メッセージ: {form.message}")
    return {"status": "ok"}


###############################################################################
# Webサービス上でのデータの取得・更新・検索など
###############################################################################

# データ構造の定義
class Item(BaseModel):
    name: str
    price: float


# 仮のデータベース
# 本来はデータベース等に保存する
ITEMS_DB = [
    {"name": "りんご", "price": 100},
    {"name": "みかん", "price": 80},
    {"name": "バナナ", "price": 120},
    {"name": "りんごジュース", "price": 150}
]


# データを取得する(全件)
@app.get("/items")
def create_item():
    return {"received": ITEMS_DB}


# データを取得する（1件を指定）
@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        return ITEMS_DB[item_id]
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")


# データを登録する
@app.post("/items")
def create_item(item: Item):
    ITEMS_DB.append(item)
    return {"received": item}


# データをk更新する
@app.put("/items/{item_id}")
def create_item(item_id: int, item: Item):
    try:
        # 削除してから再登録
        ITEMS_DB.pop(item_id)
        ITEMS_DB.append(item)
        return {"update": item}
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")


# データを削除する
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        return {"deleted": ITEMS_DB.pop(item_id)}
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")


# 検索機能の応用
@app.get("/api/search", response_model=list[Item])
def search_items(keyword: str):
    results = [item for item in ITEMS_DB if keyword in item["name"]]
    return results


###############################################################################
# 応用的な使い方の一例
###############################################################################

# クエリパラメータのバリデーション
# 画面から送られてきたデータに対してデータのチェックなどをフレームワークで実装することも可能
# keywordに設定する文字数は最低2文字以上の長さに設定する
# http://127.0.0.1:8000/search →keywordがないのでNG
# http://127.0.0.1:8000/search?keyword=a →1文字なのでNG
# http://127.0.0.1:8000/search?keyword=ab →2文字なのでOK
@app.get("/search")
def search(keyword: str = Query(..., min_length=2)):
    return {"keyword": keyword}


###############################################################################
# 外部API呼び出し（例：天気情報取得）
# 試してみたい人はAPIキーを取得して各自で取得してください。
###############################################################################

# @app.get("/weather")
# def get_weather(city: str):
#     url = f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}"
#     res = requests.get(url)
#     return res.json()
