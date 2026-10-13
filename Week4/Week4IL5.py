
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re

# 1. 列表頁網址
url = "https://www.scrapethissite.com/pages/frames/?frame=i"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # 2. 取得列表頁 HTML
    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )
    response.raise_for_status()

    # 3. HTML 轉成 DOM tree
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. 找出所有 Learn more 連結
    links = soup.select("a")

    detail_urls = []

    for link in links:
        link_text = link.get_text(" ", strip=True)

        if "Learn more" in link_text:
            href = link.get("href")

            if href:
                detail_url = urljoin(url, href)

                if detail_url not in detail_urls:
                    detail_urls.append(detail_url)

    print("找到詳細頁網址數量：", len(detail_urls))

    # 5. 逐一取得詳細資料
    data = []

    for detail_url in detail_urls:
        detail_response = requests.get(
            detail_url,
            headers=headers,
            timeout=15
        )
        detail_response.raise_for_status()

        detail_soup = BeautifulSoup(
            detail_response.text,
            "html.parser"
        )

        # 6. 取得 family
        title = detail_soup.select_one("h3")
        family = title.get_text(strip=True) if title else ""

        # 7. 取得詳細介紹文字
        paragraphs = detail_soup.select("p")

        description = " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        # 8. 解析 common_name
        common_match = re.search(
            r'more commonly known as\s*["“](.+?)["”]',
            description,
            re.IGNORECASE
        )

        common_name = (
            common_match.group(1)
            if common_match else ""
        )

        # 9. 解析 discovered_year
        year_match = re.search(
            r'first discovered in\s+(\d{4})',
            description,
            re.IGNORECASE
        )

        discovered_year = (
            year_match.group(1)
            if year_match else ""
        )

        # 10. 解析 discovered_by
        discoverer_match = re.search(
            r'discovered in\s+\d{4}\s+by\s+([^.]+)',
            description,
            re.IGNORECASE
        )

        discovered_by = (
            discoverer_match.group(1).strip()
            if discoverer_match else ""
        )

        # 11. 取得圖片網址
        image_tag = detail_soup.select_one("img")

        image_url = ""

        if image_tag:
            image_src = image_tag.get("src", "")
            if image_src:
                image_url = urljoin(detail_url, image_src)

        # 12. 加入資料清單
        data.append({
            "family": family,
            "common_name": common_name,
            "discovered_year": discovered_year,
            "discovered_by": discovered_by,
            "image_url": image_url
        })

        print(
            f"已取得：{family} | "
            f"{common_name} | "
            f"{discovered_year} | "
            f"{discovered_by}"
        )

    # 13. 建立 DataFrame
    columns = [
        "family",
        "common_name",
        "discovered_year",
        "discovered_by",
        "image_url"
    ]

    df = pd.DataFrame(data, columns=columns)

    # 14. 儲存 CSV
    df.to_csv(
        "turtles.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== Turtle Data =====")
    print(df.to_string(index=False))
    print("\n資料筆數：", len(df))
    print("已儲存：turtles.csv")

except requests.exceptions.RequestException as e:
    print("網路請求錯誤：", e)

except Exception as e:
    print("程式執行錯誤：", e)


