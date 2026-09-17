import threading
import time
import urllib.request
import os

URLS = [
    ("python_logo.png", "https://www.python.org/static/img/python-logo.png"),
    ("github.txt", "https://raw.githubusercontent.com/python/cpython/main/README.rst")
]


def download(name, url):
    """Скачивает файл и сохраняет на диск"""
    start = time.time()
    try:
        urllib.request.urlretrieve(url, name)
        size = os.path.getsize(name) / 1024  # В КБ
        elapsed = time.time() - start
        print(f"{name}: {size:.1f} КБ за {elapsed:.2f} сек")
    except Exception as e:
        print(f"{name}: ошибка — {e}")


start = time.time()
for name, url in URLS:
    download(name, url)
print(f"Общее время: {time.time() - start:.2f} сек")

start = time.time()

threads = []
for name, url in URLS:
    t = threading.Thread(target=download, args=(name, url))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Общее время: {time.time() - start:.2f} сек")

# Убираем за собой
#for name, _ in URLS:
    #if os.path.exists(name):
        #os.remove(name)
