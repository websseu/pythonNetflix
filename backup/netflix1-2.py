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

# 1-1. Films 파일만 수집
# 1-2. Films와 Tv 데이터 수집

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 폴더 생성
folder_path = "netflixKorea"
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 백그라운드 설정 및 페이지 로드
# options = ChromeOptions()
# options.add_argument("--headless")
# browser = webdriver.Chrome(options=options)

# 웹드라이버 설정(로컬)
browser = webdriver.Chrome()

# URL과 파일 이름 설정
pages = [
    {
        "url": "https://www.netflix.com/tudum/top10/south-korea",
        "file_name": f"{folder_path}/netflixKoreaFilmsTop10_{current_date}.json"
    },
    {
        "url": "https://www.netflix.com/tudum/top10/south-korea/tv",
        "file_name": f"{folder_path}/netflixKoreaTvTop10_{current_date}.json"
    }
]

# 각 페이지에 대해 데이터 수집
for page in pages:
    # 페이지 로드
    browser.get(page["url"])

    # 페이지가 완전히 로드될 때까지 대기
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "weekly-lists"))
        )
        print(f"{page['url']} 페이지가 완전히 로드되었습니다.")
        time.sleep(5)
    except TimeoutException:
        print(f"{page['url']} 페이지 로드 실패")
        continue

    # 페이지 소스 파싱
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 영화 정보를 저장할 리스트
    films_data = []

    # 영화 리스트 선택
    films = soup.select(".banner-title")

    for film in films:
        image = film.select_one("picture img").get("src") if film.select_one("picture img") else None
        title = film.select_one(".banner-image-name div").text.strip() if film.select_one(".banner-image-name div") else None
        watch = film.select_one(".banner-expanded-negative-margin .banner-hours-graf a[href]").get("href") if film.select_one(".banner-expanded-negative-margin .banner-hours-graf a[href]") else None

        # 수집된 정보를 딕셔너리에 저장
        if title and image:
            films_data.append({
                "title": title,
                "image": image,
                "watch": watch
            })

    # 추출된 데이터를 JSON 파일로 저장
    with open(page["file_name"], 'w', encoding='utf-8') as f:
        json.dump(films_data, f, ensure_ascii=False, indent=4)
        print(f"데이터가 '{page['file_name']}' 파일에 저장되었습니다.")

# 브라우저 종료
browser.quit()
