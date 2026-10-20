
import pandas as pd
import re

# 讀取 authors.csv
df = pd.read_csv("authors.csv", encoding="utf-8-sig")

# 1. born_date 的「日」，不擷取年份
print("1. born_date 的日")
for born_date in df["born_date"].dropna():
    result = re.findall(r"\b\d{1,2}(?=,)", str(born_date))
    print(result)

# 2. born_date 開頭的月份
print("\n2. born_date 開頭的月份")
for born_date in df["born_date"].dropna():
    result = re.findall(r"^[A-Za-z]+", str(born_date))
    print(result)

# 3. born_location 的國家
print("\n3. born_location 的國家")

for location in df["born_location"].dropna():
    location = str(location).strip()

    if "," in location:
        # 取最後一個逗號之後的完整內容
        result = re.findall(r"[^,]+$", location)
        result = [result[0].strip()] if result else []
    else:
        # 沒有逗號時，去除開頭的介係詞 in
        result = re.findall(
            r"^(?:in\s+)?(.+)$",
            location,
            re.IGNORECASE
        )
        result = [result[0].strip()] if result else []

    print(result)


# 4. name 裡的英文縮寫，例如 J.K.
print("\n4. name 裡的英文縮寫")
for name in df["name"].dropna():
    result = re.findall(r"\b(?:[A-Z]\.){2,}", str(name))
    print(result)
