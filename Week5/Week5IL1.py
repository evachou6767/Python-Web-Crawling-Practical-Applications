import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. 設定首頁網址
url = "https://quotes.toscrape.com/"

# 2. 發送 HTTP 請求，取得網頁內容
response = requests.get(url, timeout=15)
response.raise_for_status()

# 3. 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 4. 找出首頁所有名言區塊
quote_blocks = soup.find_all("div", class_="quote")

# 5. 設定 CSV 欄位名稱
fieldnames = ["name", "born_date", "born_location", "quote", "tags"]

# 6. 開啟 CSV 檔案並寫入資料
with open("authors.csv", "w", newline="", encoding="utf-8-sig") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入欄位名稱
    writer.writeheader()

    # 7. 逐一處理每一則名言
    for block in quote_blocks:

        # 取得作者姓名
        name = block.find("small", class_="author").get_text(strip=True)

        # 取得名言內容
        quote = block.find("span", class_="text").get_text(strip=True)

        # 取得所有標籤，並以逗號分隔
        tags = [
            tag.get_text(strip=True)
            for tag in block.find_all("a", class_="tag")
        ]
        tags = ", ".join(tags)

        # 取得作者個人頁面的連結
        author_link = block.find("a", href=True, string="(about)")["href"]
        author_url = urljoin(url, author_link)

        # 8. 進入作者個人頁面，取得出生資訊
        author_response = requests.get(author_url, timeout=15)
        author_response.raise_for_status()

        author_soup = BeautifulSoup(
            author_response.text,
            "html.parser"
        )

        # 取得出生日期
        born_date_tag = author_soup.find(
            "span",
            class_="author-born-date"
        )

        born_date = (
            born_date_tag.get_text(strip=True)
            if born_date_tag
            else ""
        )

        # 取得出生地點
        born_location_tag = author_soup.find(
            "span",
            class_="author-born-location"
        )

        born_location = (
            born_location_tag.get_text(strip=True)
            if born_location_tag
            else ""
        )

        # 9. 將資料寫入 CSV
        writer.writerow({
            "name": name,
            "born_date": born_date,
            "born_location": born_location,
            "quote": quote,
            "tags": tags
        })

        print(f"已取得作者：{name}")

print("\n爬取完成！資料已儲存至 authors.csv")
print(f"首頁名言數量：{len(quote_blocks)}")