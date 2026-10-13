
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 網頁網址
URL = "https://www.scrapethissite.com/pages/simple/"

# 2. 取得網頁 HTML
response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
response.raise_for_status()

# 3. 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 4. 使用 select() 找出所有國家資料
cards = soup.select("div.country")

data = []

for card in cards:
    # 使用 select_one() 取得國家名稱
    country = card.select_one(".country-name").get_text(strip=True)

    # 使用 select_one() 取得人口數
    population = int(
        card.select_one(".country-population").get_text(strip=True)
    )

    data.append({
        "country": country,
        "population": population
    })

# 5. 建立 DataFrame，依人口數由大到小排序
df = pd.DataFrame(data)
df = df.sort_values(by="population", ascending=False)

# 6. 取出人口數前五大的國家
top5 = df.head(5).copy()

# 7. 顯示結果
top5["population"] = top5["population"].map(lambda x: f"{x:,}")

print("人口數前五大的國家：")
print(top5.to_string(index=False))

# 8. 儲存 CSV
top5.to_csv("top5_countries.csv", index=False, encoding="utf-8-sig")

print("\n已儲存：top5_countries.csv")
