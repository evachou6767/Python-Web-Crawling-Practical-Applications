
import requests
from bs4 import BeautifulSoup
import re

# 取得 Albert Einstein 作者介紹頁
url = "https://quotes.toscrape.com/author/Albert-Einstein/"
response = requests.get(url, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 取得出生日期
born_date = soup.select_one(".author-born-date").get_text(strip=True)

# 取得作者介紹
description = soup.select_one(".author-description").get_text(" ", strip=True)

# 1. 出生年：文字轉成整數
born_year = int(re.search(r"\b\d{4}\b", born_date).group())

print("1. 出生年：")
print(born_year, type(born_year))

# 2. 介紹提到的年份：去除重複並由小到大排序
years = re.findall(r"\b(?:18|19|20)\d{2}\b", description)
years = sorted(set(map(int, years)))

print("\n2. 介紹提到的年份：")
print(years)

# 3. 去世的年份：從提到 death 的句子中擷取年份
death_match = re.search(
    r"(?:death|died|passed away)[^.]{0,100}?\b((?:18|19|20)\d{2})\b",
    description,
    re.IGNORECASE
)

if death_match:
    death_year = int(death_match.group(1))
    print("\n3. 去世年：")
    print(death_year, type(death_year))

    # 4. 計算享年
    age = death_year - born_year
    print("\n4. 享年：")
    print(f"{age} 歲")
else:
    print("\n找不到去世年份，請檢查作者介紹內容。")
