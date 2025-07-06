# 📂 フォルダ監視バッチツール - README

このプロジェクトは、Windows 環境にてフォルダを監視し、ファイルが追加された際に自動でバッチ処理を実行する常駐ツールです。トレイアイコンとして起動し、GUI なしでバックグラウンド処理を行います。

---

## 📁 プロジェクト構成

```txt
folder_watch_tool/
├── .env                            # 設定ファイル
├── base_batch.py                   # 基底バッチインタフェース
├── main.bat                        # 仮想環境でのメイン実行用バッチ
├── main.pyw                        # メイン実行スクリプト（常駐）
├── my_batch.py                     # バッチ処理の具体的な実装
├── README.md                       # 本ファイル
├── requirements.txt                # 必要ライブラリ一覧
└── template_batch.txt              # バッチ処理の雛型
```

---

## 🧩 必要環境

- OS: Windows 10 以降
- Python: 3.8 以上

---

## ⚙️ セットアップ手順（venv 使用）

```bash
# 1. プロジェクトディレクトリに移動
cd folder_watch_tool

# 2. 仮想環境の作成
python -m venv venv

# 3. 仮想環境の有効化（Windows）
venv\Scripts\activate

# 4. ライブラリのインストール
pip install -r requirements.txt
```

**requirements.txt** の内容：

```txt
pystray
watchdog
python-dotenv
pillow
```

---

## 📄 `.env` 設定例

```env
WATCH_DIR=watch
DONE_DIR=done
DOING_DIR=doing
ERROR_DIR=error
BATCH_MODULE=my_batch
BATCH_CLASS=MyBatch
```

---

## 🚀 起動方法

```bash
# バックグラウンドで常駐プログラムを起動（ダブルクリックも可）
start main.pyw
```

タスクトレイにアイコンが表示され、フォルダ監視が開始されます。

### ✋ 終了方法

- タスクトレイのアイコンを右クリック →「終了」を選択

---

## 🛠 バッチ処理のカスタマイズ

- `my_batch.py` にて、任意の処理を `MyBatch` クラスの `run(filepath: str)` に実装します。
- 戻り値が `True` の場合は `DONE_DIR` に移動、`False` または例外時は `ERROR_DIR` に移動されます。

---

## 📎 補足

- 複数ファイルの同時処理には対応していません（順次処理）
- `.pyw` 拡張子によりコンソール非表示で起動されます
- 実行ファイル化（例：`pyinstaller`）も可能です

---
