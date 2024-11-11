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

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# location 폴더 생성
folder_path = "netflixKorea"
file_name = f"{folder_path}/{folder_path}Top10_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 백그라운드 설정 및 페이지 로드
# options = ChromeOptions()
# options.add_argument("--headless")
# browser = webdriver.Chrome(options=options)
# browser.get("https://www.netflix.com/tudum/top10/south-korea")

# 웹드라이버 설정(로컬)
browser = webdriver.Chrome()
browser.get("https://www.netflix.com/tudum/top10/south-korea")

# 페이지가 완전히 로드될 때까지 대기
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "weekly-lists"))
    )
    print("페이지가 완전히 로드되었습니다.")
    time.sleep(5)
except TimeoutException:
    print("페이지 로드 실패")
    browser.quit()
    exit()

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# print(html_source_updated)

# 영화 정보를 저장할 리스트
films_data = []

films = soup.select(".banner-title")

for film in films:
    image = film.select_one("picture img").get("src") if film.select_one("picture img") else None
    title = film.select_one(".banner-image-name div").text.strip() if film.select_one(".banner-image-name div") else None
    watch = film.select_one(".banner-expanded-negative-margin .banner-hours-graf a[href]").get("href") if film.select_one(".banner-expanded-negative-margin .banner-hours-graf a[href]") else None

    films_data.append({
        "title": title,
        "image": image,
        "watch": watch
    })

# 추출된 데이터를 JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(films_data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 '{file_name}' 파일에 저장되었습니다.")
  
# 브라우저 종료
browser.quit()