# 🛠️ FastAPI アプリの実行手順

## ✅ 前提条件

- Python 3.7 以上がインストールされていること
- ターミナル（コマンドプロンプト / PowerShell / bash 等）が使用できること

---

## 📦 ステップ ①：必要なパッケージをインストール

```bash
pip install fastapi uvicorn requests
```

---

## 🚀 ステップ ②：アプリを起動

```bash
uvicorn main:app --reload
```

- `--reload` をつけることでコードを変更しても自動でリロードされます（開発用）。

---

## 🌐 ステップ ③：ブラウザでアクセス

以下の URL にアクセスできます：

| URL                                                        | 概要                           |
| ---------------------------------------------------------- | ------------------------------ |
| [http://127.0.0.1:8000](http://127.0.0.1:8000)             | ルート：Hello FastAPI          |
| [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)   | Swagger UI（API ドキュメント） |
| [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | ReDoc（別 UI のドキュメント）  |

---

## 🔑 ステップ ④：外部 API の設定（任意）

`/weather` エンドポイントで天気 API を使う場合は、以下の URL で API キー（無料登録可）を取得し：

- [https://www.weatherapi.com/](https://www.weatherapi.com/)

`main.py` の中の `YOUR_KEY` を取得した API キーに置き換えてください：

```python
url = f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}"
```

---

## ✅ 動作確認の例

1. `http://127.0.0.1:8000/greet?name=太郎`
   → `{ "message": "こんにちは 太郎 さん" }`

2. Swagger UI から `/items` に `POST`：

```json
{
  "name": "apple",
  "price": 120
}
```
