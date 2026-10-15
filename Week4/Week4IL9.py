
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. 網站首頁
URL = "https://books.toscrape.com/"

headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(URL, headers=headers, timeout=15)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "html.parser")

# 2. 爬取左側所有書籍分類
category_links = soup.select(
    ".side_categories > ul > li > ul > li > a"
)

data = []

for link in category_links:
    # 取得分類名稱
    category = link.get_text(strip=True)

    # 取得完整分類網址
    category_url = urljoin(URL, link.get("href"))

    data.append({
        "category": category,
        "url": category_url
    })

# 3. 儲存為 categories.csv
df = pd.DataFrame(data, columns=["category", "url"])
df.to_csv("categories.csv", index=False, encoding="utf-8-sig")

print("===== 所有書籍分類 =====")
print(df.to_string(index=False))
print("\n分類數量：", len(df))
print("已儲存：categories.csv")

# 4. 找出 Travel 分類網址
travel_url = df.loc[df["category"] == "Travel", "url"].iloc[0]

# 5. 進入 Travel 分類頁面
travel_resp = requests.get(
    travel_url, headers=headers, timeout=15
)
travel_resp.raise_for_status()

travel_soup = BeautifulSoup(travel_resp.content, "html.parser")

# 6. 使用 select() 找出該分類的所有書籍
books = travel_soup.select("article.product_pod")

print("\n===== Travel 分類所有書名 =====")

for index, book in enumerate(books, start=1):
    title_tag = book.select_one("h3 a")
    full_title = title_tag.get("title")

    print(f"{index}. {full_title}")

print("\nTravel 分類書籍數量：", len(books))
