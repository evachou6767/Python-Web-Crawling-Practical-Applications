import pandas as pd
import re

# 讀取 authors.csv
df = pd.read_csv("authors.csv", encoding="utf-8-sig")

# 1. born_date：列出完整年份
print("1. born_date 的完整年份")
for born_date in df["born_date"].dropna():
    result = re.findall(r"\b\d{4}\b", str(born_date))
    print(result)

# 2. born_date：列出月份（英文單字）
print("\n2. born_date 的月份")
for born_date in df["born_date"].dropna():
    result = re.findall(
        r"\b[A-Z][a-z]+\b",
        str(born_date)
    )
    print(result)

# 3. born_location：列出每一個英文單字
print("\n3. born_location 的每一個英文單字")
for location in df["born_location"].dropna():
    result = re.findall(r"[A-Za-z]+", str(location))
    print(result)

# 4. tags：拆成一個一個標籤
print("\n4. tags 拆成一個一個標籤")
for tags in df["tags"].dropna():
    result = re.findall(r"[A-Za-z-]+", str(tags))
    print(result)