import requests
import pandas as pd

# 網頁網址
URL = "https://www.scrapethissite.com/pages/forms/"

# User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 取得網頁
response = requests.get(URL, headers=HEADERS, timeout=10)
response.raise_for_status()

# 使用 pandas 直接讀取 HTML 表格
tables = pd.read_html(response.text)

# 取得第一個表格
df = tables[0]

# 顯示資料
print(df)

# 顯示資料筆數
print(f"\n共有 {len(df)} 筆資料")

# 存成 Excel
df.to_excel("hockey_teams.xlsx", index=False)

print("\n已完成：hockey_teams.xlsx")