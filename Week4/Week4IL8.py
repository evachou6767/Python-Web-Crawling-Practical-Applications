
import requests
from bs4 import BeautifulSoup

# 1. 取得網站首頁
URL = "https://books.toscrape.com/"

resp = requests.get(URL, timeout=15)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "html.parser")

# 2. 使用 select() 找出首頁所有書籍
books = soup.select("article.product_pod")

print("首頁書籍數量：", len(books))

# 3. 統計各星等數量
rating_count = {
    "Five": 0,
    "Four": 0,
    "Three": 0,
    "Two": 0,
    "One": 0
}

for book in books:
    rating_tag = book.select_one("p.star-rating")
    rating = rating_tag.get("class")[1]
    rating_count[rating] += 1

print("\n===== 各星等書籍數量 =====")
print("五星：", rating_count["Five"], "本")
print("四星：", rating_count["Four"], "本")
print("三星：", rating_count["Three"], "本")
print("二星：", rating_count["Two"], "本")
print("一星：", rating_count["One"], "本")

# 4. 用一行 CSS Selector 找出所有五星書的完整書名
five_star_books = soup.select(
    "article.product_pod:has(p.star-rating.Five) h3 a[title]"
)

print("\n===== 所有五星書的完整書名 =====")
for book in five_star_books:
    print(book.get("title"))
