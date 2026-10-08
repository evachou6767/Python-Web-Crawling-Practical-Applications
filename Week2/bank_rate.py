from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from io import StringIO
import time

URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

print("開始爬取臺灣銀行本日牌告匯率...")

# Chrome 設定
options = Options()
options.add_argument("--start-maximized")

# 開啟 Chrome
driver = webdriver.Chrome(options=options)

try:
    # 開啟臺灣銀行網站
    driver.get(URL)

    print("已開啟臺灣銀行網站")

    # 等待網頁載入
    time.sleep(5)

    # 找到匯率表格
    table = driver.find_element(By.CSS_SELECTOR, "table")

    # 取得表格 HTML
    table_html = table.get_attribute("outerHTML")

    # 讀取表格
    df = pd.read_html(StringIO(table_html))[0]

    print("\n取得的匯率資料：")
    print(df)

    print(f"\n共有 {len(df)} 筆資料")

    # -------------------------
    # 整理欄位名稱
    # -------------------------

    # 如果是兩層欄位，將兩層合併成一層
    if isinstance(df.columns, pd.MultiIndex):
        new_columns = []

        for col in df.columns:
            # 取得兩層欄位名稱
            col1 = str(col[0]).strip()
            col2 = str(col[1]).strip()

            # 如果第二層是 Unnamed，就只保留第一層
            if "Unnamed" in col2:
                new_columns.append(col1)
            else:
                new_columns.append(f"{col1}_{col2}")

        df.columns = new_columns

    print("\n整理後的欄位：")
    print(df.columns.tolist())

    # -------------------------
    # 儲存 Excel
    # -------------------------

    df.to_excel(
        "20260922.xlsx",
        index=False
    )

    print("\n完成！")
    print("已建立：20260922.xlsx")

finally:
    driver.quit()