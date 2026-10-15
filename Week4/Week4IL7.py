
import requests
from bs4 import BeautifulSoup

# 1. 爬取 Books to Scrape 網站首頁
URL = "https://books.toscrape.com/"

resp = requests.get(URL, timeout=15)
resp.raise_for_status()

# 2. 印出 resp.encoding
print("===== 原始編碼資訊 =====")
print("resp.encoding：", resp.encoding)
print("resp.apparent_encoding：", resp.apparent_encoding)

# 3. 使用原始 resp.text，觀察第一本書的價格
soup = BeautifulSoup(resp.text, "html.parser")

first_book = soup.select_one("article.product_pod")
price = first_book.select_one(".price_color").get_text(strip=True)

print("\n===== 原始價格 =====")
print("原始價格：", price)

# 4. 修法1：設定 resp.encoding 為 UTF-8
resp.encoding = "utf-8"

soup1 = BeautifulSoup(resp.text, "html.parser")
first_book1 = soup1.select_one("article.product_pod")
price1 = first_book1.select_one(".price_color").get_text(strip=True)

print("\n===== 修法1：resp.encoding =====")
print("修法1價格:", price1)

# 5. 修法2：使用 resp.content 原始位元組
soup2 = BeautifulSoup(resp.content, "html.parser")
first_book2 = soup2.select_one("article.product_pod")
price2 = first_book2.select_one(".price_color").get_text(strip=True)

print("\n===== 修法2：resp.content =====")
print("修法2價格:", price2)

