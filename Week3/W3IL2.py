import os
import logging
import requests
import pandas as pd


# ==============================
# Logging 設定
# ==============================
FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE = os.path.join(os.getcwd(), "w03.log")

logging.basicConfig(
    level=logging.DEBUG,
    format=FMT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True
)

logger = logging.getLogger("w03")


# ==============================
# 網址
# ==============================
URL = "https://www.scrapethissite.com/pages/forms/"

try:
    logger.info("開始爬取 Scrape This Site 冰球隊伍統計表")

    # 發送 Request
    resp = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    # 記錄 HTTP 狀態碼
    logger.info("狀態碼 = %s", resp.status_code)

    # 檢查 HTTP 是否發生錯誤
    resp.raise_for_status()

    logger.info("網頁取得成功")

    # ==============================
    # 讀取表格
    # ==============================
    tables = pd.read_html(resp.text)

    logger.info("HTML 表格數量 = %s", len(tables))

    df = tables[0]

    logger.info("原始資料筆數 = %s", len(df))

    # ==============================
    # 只取前 25 筆
    # ==============================
    df = df.head(25)

    logger.info("實際取出資料筆數 = %s", len(df))

    # ==============================
    # 顯示資料
    # ==============================
    logger.debug("取得的資料：\n%s", df)

    # ==============================
    # 儲存 CSV
    # ==============================
    output_file = os.path.join(os.getcwd(), "output.csv")

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info("CSV 儲存成功：%s", output_file)

    print("爬取完成！")
    print(f"取得 {len(df)} 筆資料")
    print(f"CSV 檔案：{output_file}")
    print(f"Log 檔案：{LOG_FILE}")


except requests.exceptions.RequestException as e:

    logger.exception("HTTP Request 發生錯誤")

    print("HTTP Request 發生錯誤")
    print(e)


except ValueError as e:

    logger.exception("HTML 表格解析失敗")

    print("HTML 表格解析失敗")
    print(e)


except Exception as e:

    logger.exception("程式發生未預期錯誤")

    print("程式發生未預期錯誤")
    print(e)