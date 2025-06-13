# 🗃 データベース処理教材：PostgreSQL との接続と操作の基本

この教材では、Python から PostgreSQL データベースに接続し、データの読み書きを行う方法を学びます。`psycopg2`や`SQLAlchemy`を使った実践的なコード例を交えて、基本的な SQL 操作とデータフレームへの連携を解説します。

---

## ✅ ステップ ①：環境準備

### 📌 必要ライブラリのインストール

```bash
pip install psycopg2-binary sqlalchemy pandas
```

### 📌 PostgreSQL の用意

- ローカル or クラウド（例：ElephantSQL、Render など）
- テーブル定義例：

```sql
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    date DATE,
    product TEXT,
    amount INTEGER,
    customer TEXT
);
```

---

## ✅ ステップ ②：psycopg2 で基本的な接続と操作

### 📌 データの挿入

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="testdb",
    user="postgres",
    password="yourpassword"
)
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO sales (date, product, amount, customer) VALUES (%s, %s, %s, %s)",
    ("2024-06-01", "Widget", 5, "Tanaka")
)

conn.commit()
cursor.close()
conn.close()
```

### 📌 データの取得

```python
conn = psycopg2.connect(...)
cursor = conn.cursor()

cursor.execute("SELECT * FROM sales")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
```

---

## ✅ ステップ ③：pandas との連携（SELECT 結果の DataFrame 化）

```python
import pandas as pd

conn = psycopg2.connect(...)
df = pd.read_sql("SELECT * FROM sales", conn)
print(df.head())
conn.close()
```

---

## ✅ ステップ ④：SQLAlchemy による ORM 的操作（基本）

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql+psycopg2://postgres:yourpassword@localhost/testdb")

# データ挿入（DataFrame → DB）
df = pd.DataFrame({
    "date": ["2024-06-01"],
    "product": ["Gadget"],
    "amount": [3],
    "customer": ["Suzuki"]
})
df.to_sql("sales", engine, if_exists="append", index=False)

# 読み込み（DB → DataFrame）
df2 = pd.read_sql("SELECT * FROM sales", engine)
print(df2)
```

---

## ✅ ステップ ⑤：実践課題

### 📁 課題 1：データの追加と一覧表示

- 任意のデータを挿入 → 全件表示

### 📊 課題 2：月別売上集計

- SQL または pandas で集計処理

### 📈 課題 3：売上金額が一定以上のデータだけを抽出・CSV 出力

---

### 🚀 最終ゴール

- Python と PostgreSQL を連携させて、データを読み書き・加工・保存できるようになること。
- データ分析の前処理や業務自動化に役立てる。
