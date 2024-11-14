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

# 최상위 폴더 생성
base_folder_path = "popular"
os.makedirs(base_folder_path, exist_ok=True)

# 각 페이지 URL 리스트
urls = {
    "films": "https://www.netflix.com/tudum/top10/most-popular",
    "filmsNone": "https://www.netflix.com/tudum/top10/most-popular/films-non-english",
    "tv": "https://www.netflix.com/tudum/top10/most-popular/tv",
    "tvNone": "https://www.netflix.com/tudum/top10/most-popular/tv-non-english"
}

# 웹드라이버 설정(로컬)
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 결과 데이터를 저장할 딕셔너리
data = {
    "kind": "netflix popular",
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
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "most-popular")))
        print(f"{category} 페이지가 완전히 로드되었습니다.")
        time.sleep(3)

        # 페이지 소스 파싱
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # 테이블에서 순위, 제목, 조회 시간, 조회 수 데이터 추출
        popular_data = []
        table_rows = soup.select("table.w-full tr")[1:]  # 첫 번째 행은 헤더이므로 제외

        for row in table_rows:
            rank = row.select_one("td:nth-child(1)").get_text(strip=True) if row.select_one("td:nth-child(1)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            hours_viewed = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            views = row.select_one("td:nth-child(5)").get_text(strip=True) if row.select_one("td:nth-child(5)") else "N/A"

            # 정보를 딕셔너리 형태로 저장
            popular_data.append({
                "rank": rank,
                "title": title,
                "hours_viewed": hours_viewed,
                "views": views
            })
        
        # 이미지 및 ID 추출 
        card_rows = soup.select(".all-time-cards-list .relative")  

        for i, card in enumerate(card_rows):
            if i < len(popular_data):  # 데이터 길이 초과 방지
                # 이미지 URL 추출
                image_url = card.select_one("picture img")["src"] if card.select_one("picture img") else "N/A"
                
                # watchID 추출
                watch_link = card.select_one("a")["href"] if card.select_one("a") else ""
                watch_id = watch_link.split("/")[-1] if watch_link else "N/A"
                
                # 각 popular_data 항목에 추가
                popular_data[i]["image"] = image_url
                popular_data[i]["watchID"] = watch_id
        
        # 각 카테고리에 맞게 데이터 저장
        data[category].extend(popular_data)

    except TimeoutException:
        print(f"{category} 페이지 로드 실패")

# 결과를 JSON 파일로 저장
output_file_path = os.path.join(base_folder_path, f"popular_{current_date}.json")
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"데이터가 {output_file_path}에 저장되었습니다.")

# 브라우저 닫기
browser.quit()
