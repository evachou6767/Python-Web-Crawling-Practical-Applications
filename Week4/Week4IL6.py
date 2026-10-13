
import requests
from bs4 import BeautifulSoup

# 1. 網頁網址
URL = "https://books.toscrape.com/"

# 2. 取得網頁 HTML
response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=15
)
response.raise_for_status()

# 3. 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 4. 使用 select() 找出首頁所有書籍
books = soup.select("article.product_pod")

# 5. 取得前五本書的書名
for index, book in enumerate(books[:5], start=1):
    title_tag = book.select_one("h3 a")

    # 取得畫面上顯示的書名
    display_title = title_tag.get_text(strip=True)

    # 取得 title 屬性中的完整書名
    full_title = title_tag.get("title")

    print(f"第 {index} 本書")
    print(f"畫面上的書名：{display_title}")
    print(f"title 屬性的完整書名：{full_title}")
    print("-" * 60)
