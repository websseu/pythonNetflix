from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from bs4 import BeautifulSoup
import os
import json
import time

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 최상위 global 폴더 생성
base_folder_path = "global"
os.makedirs(base_folder_path, exist_ok=True)

# 각 페이지 URL 리스트
urls = {
    "films": "https://www.netflix.com/tudum/top10",
    "filmsNone": "https://www.netflix.com/tudum/top10/films-non-english",
    "tv": "https://www.netflix.com/tudum/top10/tv",
    "tvNone": "https://www.netflix.com/tudum/top10/tv-non-english"
}

# 웹드라이버 백그라운드 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 웹드라이버 설정(로컬)
# browser = webdriver.Chrome()
# browser.get("https://www.netflix.com/tudum/top10")

# 결과 데이터를 저장할 딕셔너리
data = {
    "kind": "Netflix Global",
    "date": current_date,
    "films": [],
    "filmsNone": [],
    "tv": [],
    "tvNone": []
}

# 각 URL에 대해 데이터 수집
for category, url in urls.items():
    browser.get(url)

    # 페이지가 로드될 시간을 기다림
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "weekly-lists")))
        print(f"{category} 페이지가 완전히 로드되었습니다.")
        time.sleep(3)

        # 페이지 소스 파싱
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # 정보를 저장할 리스트
        global_data = []

        # 이미지 및 각종 정보 추출
        banners = soup.select(".banner-title")
        table_rows = soup.select("tbody tr")

        for item, row in zip(banners, table_rows):
            # 이미지 추출
            image = item.select_one("picture img").get("src") if item.select_one("picture img") else "N/A"
            
            # 순위, 제목, 주차, 조회 시간, 조회 수 추출
            ranking = row.select_one("td:nth-child(1)").get_text(strip=True) if row.select_one("td:nth-child(1)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            week = row.select_one("td:nth-child(3) .wk-number").get_text(strip=True) if row.select_one("td:nth-child(3) .wk-number") else "N/A"
            hours_viewed = row.select_one("td:nth-child(4) span").get_text(strip=True) if row.select_one("td:nth-child(4) span") else "N/A"
            views = row.select_one("td:nth-child(6) span").get_text(strip=True) if row.select_one("td:nth-child(6) span") else "N/A"
            watch_id = row.get("data-id", "N/A")

            # 이미지와 함께 정보를 추가
            global_data.append({
                "rank": ranking,
                "title": title,
                "week": week,
                "hours": hours_viewed,
                "views": views,
                "image": image,
                "watchID": watch_id
            })

        # data 딕셔너리의 카테고리 항목에 데이터 추가
        data[category].extend(global_data)

    except TimeoutException:
        print("페이지 로드 실패")

# 결과를 JSON 파일로 저장
output_file_path = os.path.join(base_folder_path, f"global_{current_date}.json")
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"데이터가 {output_file_path}에 저장되었습니다.")

# 브라우저 닫기
browser.quit()