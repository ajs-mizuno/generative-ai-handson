# 📄 my_batch.py：バッチ処理クラスの実装例
from base_batch import BatchInterface


class MyBatch(BatchInterface):
    def run(self, filepath: str) -> bool:
        try:
            # 例：ファイルの内容を読み取り、変換処理を行い、結果を保存する
            with open(filepath, mode="r", encoding="utf-8") as f:
                text = f.read()

            # ここに任意の変換処理を記述（例：全角→半角変換など）
            converted = text.upper()  # 仮処理：大文字化

            # 変換データを出力
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(converted)

            return True
        except Exception as e:
            print(f"[MyBatch] エラー: {e}")
            return False
