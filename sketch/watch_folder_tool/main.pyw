# 📦 フォルダ監視バッチツール（Windows/トレイ常駐）

# ライブラリ要件：
# pip install pystray watchdog python-dotenv pillow
import os
import time
import shutil
import threading
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image

from base_batch import BatchInterface

# .env の読み込み
load_dotenv()
WATCH_DIR = os.getenv("WATCH_DIR", "watch")
DOING_DIR = os.getenv("DOING_DIR", "doing")
DONE_DIR = os.getenv("DONE_DIR", "done")
ERROR_DIR = os.getenv("ERROR_DIR", "error")
BATCH_MODULE = os.getenv("BATCH_MODULE", "my_batch")
BATCH_CLASS = os.getenv("BATCH_CLASS", "MyBatch")


# 動的にバッチクラスを読み込む
def load_batch():
    module = importlib.import_module(BATCH_MODULE)
    cls = getattr(module, BATCH_CLASS)
    if not issubclass(cls, BatchInterface):
        raise TypeError("バッチクラスはBatchInterfaceを継承している必要があります")
    return cls()


# ファイルイベントハンドラ
class WatchHandler(FileSystemEventHandler):
    def __init__(self, batch_processor):
        self.batch = batch_processor

    def on_created(self, event):
        if event.is_directory:
            return
        original_path = event.src_path
        filename = os.path.basename(original_path)
        time.sleep(1)  # 書き込み終了待機
        try:
            # 作業中ディレクトリに移動
            os.makedirs(DOING_DIR, exist_ok=True)
            doing_path = os.path.join(DOING_DIR, filename)
            shutil.move(original_path, doing_path)
            # バッチ処理を実行
            success = self.batch.run(doing_path)
            dest = DONE_DIR if success else ERROR_DIR
        except Exception as e:
            print(f"エラー: {e}")
            dest = ERROR_DIR
        os.makedirs(dest, exist_ok=True)
        shutil.move(doing_path, os.path.join(dest, os.path.basename(filename)))


# トレイアイコン処理
class TrayApp:
    def __init__(self):
        self.icon = Icon("Watcher")
        self.icon.menu = Menu(Item("終了", self.quit))
        self.icon.icon = Image.new("RGB", (64, 64), "gray")
        self.observer = None

    def start(self):
        batch = load_batch()
        event_handler = WatchHandler(batch)
        self.observer = Observer()
        self.observer.schedule(event_handler, WATCH_DIR, recursive=False)
        self.observer.start()
        threading.Thread(target=self.icon.run).start()

    def quit(self, icon, item):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.icon.stop()


if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(DOING_DIR, exist_ok=True)
    os.makedirs(DONE_DIR, exist_ok=True)
    os.makedirs(ERROR_DIR, exist_ok=True)
    TrayApp().start()
