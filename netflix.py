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

# 나라 설정
countries = ["argentina"]

# 최상위 country 폴더 생성
base_folder_path = "country"
os.makedirs(base_folder_path, exist_ok=True)

# 웹드라이버 백그라운드 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 웹드라이버 설정(로컬)
# browser = webdriver.Chrome()

# 나라별로 데이터 수집
for country_code in countries:
    # 폴더명은 나라 코드를 대문자로 시작하도록 변환
    country_name = country_code.replace("-", " ").title().replace(" ", "")
    folder_path = os.path.join(base_folder_path, country_name)
    os.makedirs(folder_path, exist_ok=True)

    # 페이지 목록 설정 (Films와 TV)
    pages = [
        {
            "url": f"https://www.netflix.com/tudum/top10/{country_code}",
            "file_name": f"{folder_path}/{country_name}FilmsTop10_{current_date}.json"
        },
        {
            "url": f"https://www.netflix.com/tudum/top10/{country_code}/tv",
            "file_name": f"{folder_path}/{country_name}TvTop10_{current_date}.json"
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

        # 정보를 저장할 리스트
        films_data = []

        # .banner-title에서 title과 image를 추출
        titles_images = soup.select(".banner-title")
        titles_images_data = []
        for item in titles_images:
            title = item.select_one(".banner-image-name div").text.strip() if item.select_one(".banner-image-name div") else None
            image = item.select_one("picture img").get("src") if item.select_one("picture img") else None
            if title and image:
                titles_images_data.append({"title": title, "image": image})

        # tbody tr에서 rank_number와 watchID 추출
        film_rows = soup.select("tbody tr")
        for index, film in enumerate(film_rows):
            # wk-number 클래스에서 주간 순위 가져오기
            week_number = film.select_one(".wk-number").text.strip() if film.select_one(".wk-number") else None
            watchID = film.get("data-id")

            # title과 image 데이터가 존재할 때만 매칭
            if index < len(titles_images_data):
                film_data = titles_images_data[index]
                film_data.update({
                    "week": week_number,
                    "watchID": watchID
                })
                films_data.append(film_data)

        # 추출된 데이터를 JSON 파일로 저장
        with open(page["file_name"], 'w', encoding='utf-8') as f:
            json.dump(films_data, f, ensure_ascii=False, indent=4)
            print(f"데이터가 '{page['file_name']}' 파일에 저장되었습니다.")

# 모든 데이터 수집 완료 메시지
print("모든 나라에 대한 데이터 수집이 완료되었습니다.")

# 브라우저 종료
browser.quit()
