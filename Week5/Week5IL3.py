import pandas as pd
import re

# 讀取 authors.csv
df = pd.read_csv("authors.csv", encoding="utf-8-sig")

# 1. born_date：列出所有數字
print("1. born_date 所有的數字")
for born_date in df["born_date"].dropna():
    result = re.findall(r"\d", str(born_date))
    print(result)

# 2. born_location：列出所有大寫字母
print("\n2. born_location 所有大寫字母")
for location in df["born_location"].dropna():
    result = re.findall(r"[A-Z]", str(location))
    print(result)

# 3. tags：列出所有非小寫字母的字元
print("\n3. tags 所有非小寫字母的字元")
for tags in df["tags"].dropna():
    result = re.findall(r"[^a-z]", str(tags))
    print(result)

# 4. quote：列出所有標點符號
print("\n4. quote 所有的標點符號")
for quote in df["quote"].dropna():
    result = re.findall(r"[^\w\s]", str(quote))
    print(result)