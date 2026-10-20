import re
import pandas as pd


def get_country(location):
    """使用正規表示法從出生地辨識國家。"""

    if pd.isna(location) or not str(location).strip():
        return "Unknown"

    location = str(location).strip()

    # 國家名稱與常見縮寫的正規表示式
    country_patterns = [
        (r"\b(?:USA|U\.S\.A\.|United States(?: of America)?|The United States)\b", "USA"),
        (r"\b(?:UK|United Kingdom|England|Scotland|Wales|Northern Ireland)\b", "United Kingdom"),
        (r"\bFrance\b", "France"),
        (r"\bGermany\b", "Germany"),
        (r"\bItaly\b", "Italy"),
        (r"\bSpain\b", "Spain"),
        (r"\bCanada\b", "Canada"),
        (r"\bAustralia\b", "Australia"),
        (r"\bIreland\b", "Ireland"),
        (r"\bJapan\b", "Japan"),
        (r"\bChina\b", "China"),
        (r"\bIndia\b", "India"),
        (r"\bRussia\b", "Russia"),
        (r"\bAustria\b", "Austria"),
        (r"\bSwitzerland\b", "Switzerland"),
        (r"\bBelgium\b", "Belgium"),
        (r"\bNetherlands\b", "Netherlands"),
        (r"\bPortugal\b", "Portugal"),
        (r"\bGreece\b", "Greece"),
        (r"\bSweden\b", "Sweden"),
        (r"\bNorway\b", "Norway"),
        (r"\bDenmark\b", "Denmark"),
        (r"\bPoland\b", "Poland"),
        (r"\bNew Zealand\b", "New Zealand"),
    ]

    for pattern, country in country_patterns:
        if re.search(pattern, location, flags=re.IGNORECASE):
            return country

    # 美國出生地有時只寫城市、州名，沒有 USA
    us_states = (
        r"Alabama|Alaska|Arizona|Arkansas|California|Colorado|"
        r"Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|"
        r"Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|"
        r"Maryland|Massachusetts|Michigan|Minnesota|Mississippi|"
        r"Missouri|Montana|Nebraska|Nevada|New Hampshire|"
        r"New Jersey|New Mexico|New York|North Carolina|"
        r"North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|"
        r"Rhode Island|South Carolina|South Dakota|Tennessee|"
        r"Texas|Utah|Vermont|Virginia|Washington|West Virginia|"
        r"Wisconsin|Wyoming"
    )

    if re.search(
        rf"(?:^|,\s*)(?:{us_states})(?:,\s*[^,]+)?$",
        location,
        flags=re.IGNORECASE
    ):
        return "USA"

    return "Unknown"


# 讀取 CSV
df = pd.read_csv("authors.csv", encoding="utf-8-sig")

# 依出生地辨識國家
df["country"] = df["born_location"].apply(get_country)

# 同一作者可能有多則名言，統計前先去重
authors_unique = df.drop_duplicates(subset=["name"])

# 統計各國作者人數
country_counts = authors_unique["country"].value_counts()

print("各國作者人數：")
print(country_counts.to_string())