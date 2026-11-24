
import requests
import sqlite3
import time

from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin


# ==================================================
# 1. 基本設定
# ==================================================

BASE_URL = "https://quotes.toscrape.com/"

DB_NAME = "quotes_sqlite.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 台灣時區 UTC+8
TAIWAN_TIMEZONE = timezone(timedelta(hours=8))


# ==================================================
# 2. 建立 SQLite 資料庫及資料表
# ==================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (

            quote TEXT PRIMARY KEY,

            author TEXT NOT NULL,

            tags TEXT,

            page INTEGER,

            scraped_at TEXT

        )
    """)

    conn.commit()

    print("SQLite 資料庫建立成功！")

    return conn


# ==================================================
# 3. 爬取單一頁面的名言
# ==================================================

def scrape_page(url, page, conn):

    print(f"\n正在爬取第 {page} 頁...")

    # 發送 HTTP Request
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    # 檢查 HTTP 回應狀態
    response.raise_for_status()

    # 解析 HTML
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # 找出本頁所有名言區塊
    quote_list = soup.select("div.quote")

    cursor = conn.cursor()

    count = 0

    for item in quote_list:

        # ------------------------------------------
        # 擷取名言
        # ------------------------------------------

        quote_element = item.select_one("span.text")

        quote = quote_element.get_text(strip=True)

        # ------------------------------------------
        # 擷取作者
        # ------------------------------------------

        author_element = item.select_one("small.author")

        author = author_element.get_text(strip=True)

        # ------------------------------------------
        # 擷取所有 Tags
        # ------------------------------------------

        tags_list = [
            tag.get_text(strip=True)
            for tag in item.select("a.tag")
        ]

        # 多個 Tags 使用分號串接
        tags = ";".join(tags_list)

        # ------------------------------------------
        # 記錄爬取時間 ISO 8601
        # ------------------------------------------

        scraped_at = datetime.now(
            TAIWAN_TIMEZONE
        ).isoformat(timespec="seconds")

        # ------------------------------------------
        # 寫入 SQLite 資料庫
        # ------------------------------------------

        cursor.execute("""
            INSERT INTO quotes (
                quote,
                author,
                tags,
                page,
                scraped_at
            )
            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(quote)
            DO UPDATE SET

                author = excluded.author,

                tags = excluded.tags,

                page = excluded.page,

                scraped_at = excluded.scraped_at

        """, (
            quote,
            author,
            tags,
            page,
            scraped_at
        ))

        count += 1

    # 儲存目前頁面的資料
    conn.commit()

    print(f"第 {page} 頁完成！")

    print(f"取得名言：{count} 筆")

    return soup, count


# ==================================================
# 4. 爬取網站所有頁面
# ==================================================

def scrape_all_pages(conn):

    url = BASE_URL

    page = 1

    total_quotes = 0

    while url:

        try:

            # 爬取目前頁面
            soup, count = scrape_page(
                url,
                page,
                conn
            )

            total_quotes += count

            # 尋找下一頁
            next_page = soup.select_one(
                "li.next a"
            )

            if next_page:

                next_url = next_page.get("href")

                # 組合下一頁完整網址
                url = urljoin(url, next_url)

                page += 1

                # 暫停 0.5 秒，避免頻繁請求
                time.sleep(0.5)

            else:

                # 沒有下一頁，結束爬取
                url = None

        except requests.RequestException as e:

            print(f"網頁爬取發生錯誤：{e}")

            break

        except Exception as e:

            print(f"程式執行發生錯誤：{e}")

            break

    print("\n================================")

    print("所有頁面爬取作業結束！")

    print(f"總共取得名言：{total_quotes} 筆")

    print(f"總共爬取頁數：{page if total_quotes else 0} 頁")

    print("================================")


# ==================================================
# 5. 查詢 SQLite 資料庫
# ==================================================

def show_results(conn):

    cursor = conn.cursor()

    # 查詢總筆數
    cursor.execute("""
        SELECT COUNT(*)
        FROM quotes
    """)

    total = cursor.fetchone()[0]

    print("\n========== 資料庫統計 ==========")

    print(f"資料庫名稱：{DB_NAME}")

    print("資料表名稱：quotes")

    print(f"名言總筆數：{total}")

    # 查詢前五筆資料
    cursor.execute("""
        SELECT
            quote,
            author,
            tags,
            page,
            scraped_at

        FROM quotes

        ORDER BY page

        LIMIT 5
    """)

    results = cursor.fetchall()

    print("\n========== 前五筆資料 ==========")

    for row in results:

        print("\n名言：", row[0])

        print("作者：", row[1])

        print("標籤：", row[2])

        print("頁數：", row[3])

        print("爬取時間：", row[4])


# ==================================================
# 6. 主程式
# ==================================================

def main():

    print("================================")

    print("Quotes to Scrape 爬蟲程式")

    print("================================")

    conn = None

    try:

        # 建立資料庫
        conn = create_database()

        # 爬取網站所有頁面
        scrape_all_pages(conn)

        # 顯示資料庫結果
        show_results(conn)

    except sqlite3.Error as e:

        print(f"SQLite 資料庫錯誤：{e}")

    except Exception as e:

        print(f"程式發生錯誤：{e}")

    finally:

        if conn:

            conn.close()

            print("\nSQLite 資料庫連線已關閉。")


# ==================================================
# 7. 程式進入點
# ==================================================

if __name__ == "__main__":

    main()
