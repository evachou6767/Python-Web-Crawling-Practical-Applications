
import sqlite3
import pandas as pd

# =====================================
# 資料庫及 LOG 檔案路徑
# =====================================

DB_NAME = r"D:\Python_Course_Demo\quotes_sqlite.db"

LOG_NAME = r"D:\Python_Course_Demo\week_06exercise_10.log"

# 儲存所有查詢結果
results = []

# =====================================
# 連接 SQLite 資料庫
# =====================================

conn = sqlite3.connect(DB_NAME)

cursor = conn.cursor()

results.append("=" * 60)
results.append("Week 06 Exercise 10")
results.append("Quotes SQLite Database 查詢結果")
results.append("=" * 60)


# =====================================
# Q1: 利用 fetchone 查詢
# 資料表總共有幾句名言、幾位作家
# =====================================

results.append("\nQ1：名言總數及作家人數")

cursor.execute("""
    SELECT
        COUNT(quote),
        COUNT(DISTINCT author)
    FROM quotes
""")

total_quotes, total_authors = cursor.fetchone()

results.append(f"名言總數：{total_quotes} 句")
results.append(f"作家總數：{total_authors} 位")


# =====================================
# Q2: 利用 qmark style 佔位符查詢
# Albert Einstein 共幾句名言？
# 並列印前 3 句
# =====================================

results.append("\nQ2：Albert Einstein 的名言")

# 使用 qmark style 佔位符 ?
cursor.execute("""
    SELECT COUNT(*)
    FROM quotes
    WHERE author = ?
""", ("Albert Einstein",))

einstein_count = cursor.fetchone()[0]

results.append(
    f"Albert Einstein 共 {einstein_count} 句名言"
)

# 查詢前 3 句
cursor.execute("""
    SELECT quote
    FROM quotes
    WHERE author = ?
    LIMIT 3
""", ("Albert Einstein",))

einstein_quotes = cursor.fetchall()

results.append("前 3 句名言：")

for i, row in enumerate(einstein_quotes, start=1):
    results.append(f"{i}. {row[0]}")


# =====================================
# Q3: 利用 for 迴圈印出
# 句數最多的前 5 位作家
# =====================================

results.append("\nQ3：名言數量最多的前 5 位作家")

cursor.execute("""
    SELECT author, COUNT(*) AS quote_count
    FROM quotes
    GROUP BY author
    ORDER BY quote_count DESC, author ASC
    LIMIT 5
""")

top_authors = cursor.fetchall()

for i, row in enumerate(top_authors, start=1):
    author = row[0]
    count = row[1]

    results.append(
        f"{i}. {author}：{count} 句"
    )


# =====================================
# Q4: 利用 pd.read_sql_query 查詢
# tag 含有 love 的名言共幾句
# =====================================

results.append("\nQ4：Tag 含有 love 的名言數量")

sql_query = """
    SELECT quote, author, tags
    FROM quotes
    WHERE tags LIKE ?
"""

# 使用 pandas read_sql_query 查詢
df = pd.read_sql_query(
    sql_query,
    conn,
    params=("%love%",)
)

love_count = len(df)

results.append(
    f"Tag 含有 love 的名言共 {love_count} 句"
)


# =====================================
# 寫入 LOG 檔案
# =====================================

results.append("\n" + "=" * 60)
results.append("查詢完成！")
results.append("=" * 60)

# 寫入 UTF-8 編碼的 LOG 檔案
with open(LOG_NAME, "w", encoding="utf-8") as file:
    file.write("\n".join(results))

# 同時在 PowerShell 顯示查詢結果
print("\n".join(results))


# =====================================
# 關閉資料庫連線
# =====================================

conn.close()

print(f"\nLOG 檔案已儲存：{LOG_NAME}")
