import requests

URL = "https://www.scrapethissite.com/pages/forms/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(URL, headers=HEADERS, timeout=10)

# ---------- Response（伺服器回應內容） ----------
print(f"[Response] 狀態碼 = {resp.status_code}")
print(f"[Response] Content-Type = {resp.headers.get('Content-Type')}")
print(f"[Response] 編碼 = {resp.encoding}")
print(f"[Response] 指定語系 = {resp.headers.get('Content-Language')}")
print(f"[Response] User-Agent = {resp.request.headers.get('User-Agent')}")

---------------------------------------

[Response] 狀態碼 = 200
[Response] Content-Type = text/html; charset=utf-8
[Response] 編碼 = utf-8
[Response] 指定語系 = None
[Response] User-Agent = Mozilla/5.0
