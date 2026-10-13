
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 網頁網址
url = "https://www.scrapethissite.com/pages/forms/"

try:
    # 2. 取得網頁
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    # 檢查 HTTP 狀態碼
    print("Status Code:", response.status_code)
    response.raise_for_status()

    # 3. 解析 HTML 原始碼
    soup = BeautifulSoup(response.text, "html.parser")

    # 使用 select() 取得第一頁所有隊伍資料
    teams = soup.select("tr.team")

    # 儲存資料
    data = []

    for team in teams:
        # 使用 select_one() 取得各欄位文字
        team_name = team.select_one("td.name").get_text(strip=True)
        year = team.select_one("td.year").get_text(strip=True)
        wins = team.select_one("td.wins").get_text(strip=True)
        losses = team.select_one("td.losses").get_text(strip=True)
        win_pct = team.select_one("td.pct").get_text(strip=True)
        goals_for = team.select_one("td.gf").get_text(strip=True)
        goals_against = team.select_one("td.ga").get_text(strip=True)
        diff = team.select_one("td.diff").get_text(strip=True)

        # 將資料加入清單
        data.append({
            "team_name": team_name,
            "year": year,
            "wins": wins,
            "losses": losses,
            "win_pct": win_pct,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "diff": diff
        })

    # 4. 轉換成 DataFrame
    df = pd.DataFrame(data)

    print("\n===== Hockey Teams 統計表 =====")
    print(df)
    print("\n資料筆數：", len(df))

    # 5. 儲存成 CSV
    df.to_csv(
        "hockey_teams.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n已成功儲存：hockey_teams.csv")

except requests.exceptions.RequestException as e:
    print("網路請求錯誤：", e)

except Exception as e:
    print("程式執行錯誤：", e)
