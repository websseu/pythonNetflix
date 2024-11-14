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
countries = [
    "argentina", "australia", "austria", "bahamas", "bahrain", "bangladesh",
    "belgium", "bolivia", "brazil", "bulgaria", "canada", "chile", "colombia",
    "costa-rica", "croatia", "cyprus", "czech-republic", "denmark", "dominican-republic",
    "ecuador", "egypt", "el-salvador", "estonia", "finland", "france", "germany",
    "greece", "guatemala", "honduras", "hong-kong", "hungary", "iceland", "india",
    "indonesia", "israel", "italy", "jamaica", "japan", "jordan", "kenya", "kuwait",
    "latvia", "lebanon", "lithuania", "luxembourg", "malaysia", "maldives", "malta",
    "mauritius", "mexico", "morocco", "netherlands", "new-zealand", "nicaragua",
    "nigeria", "norway", "oman", "pakistan", "panama", "paraguay", "peru",
    "philippines", "poland", "portugal", "qatar", "romania", "saudi-arabia",
    "serbia", "singapore", "slovakia", "slovenia", "south-africa", "south-korea",
    "spain", "sri-lanka", "sweden", "switzerland", "taiwan", "thailand", "trinidad",
    "turkey", "ukraine", "united-arab-emirates", "united-kingdom", "united-states",
    "uruguay", "venezuela", "vietnam"
]


# 주간 설정 (수집할 날짜들)
# weeks = [
#     "2024-11-03", 
#     "2024-10-27", "2024-10-20", "2024-10-13", "2024-10-06",
#     "2024-09-29", "2024-09-22", "2024-09-15", "2024-09-08", "2024-09-01",
#     "2024-08-25", "2024-08-18", "2024-08-11", "2024-08-04", 
#     "2024-07-28", "2024-07-21", "2024-07-14", "2024-07-07", 
#     "2024-06-30", "2024-06-23", "2024-06-16", "2024-06-09", "2024-06-02",
#     "2024-05-26", "2024-05-19", "2024-05-12", "2024-05-05",
#     "2024-04-28", "2024-04-21", "2024-04-14", "2024-04-07",
#     "2024-03-31", "2024-03-24", "2024-03-17", "2024-03-10", "2024-03-03",
#     "2024-02-25", "2024-02-18", "2024-02-11", "2024-02-04",
#     "2024-01-28", "2024-01-21", "2024-01-14", "2024-01-07",
#     "2023-12-31", "2023-12-24", "2023-12-17", "2023-12-10", "2023-12-03",
#     "2023-11-26", "2023-11-19", "2023-11-12", "2023-11-05",
#     "2023-10-29", "2023-10-22", "2023-10-15", "2023-10-08", "2023-10-01",
#     "2023-09-24", "2023-09-17", "2023-09-10", "2023-09-03", 
#     "2023-08-27", "2023-08-20", "2023-08-13", "2023-08-06", 
#     "2023-07-30", "2023-07-23", "2023-07-16", "2023-07-09", "2023-07-02", 
#     "2023-06-25", "2023-06-18", "2023-06-11", "2023-06-04", 
#     "2023-05-28", "2023-05-21", "2023-05-14", "2023-05-07", 
#     "2023-04-30", "2023-04-23", "2023-04-16", "2023-04-09", "2023-04-02", 
#     "2023-03-26", "2023-03-19", "2023-03-12", "2023-03-05", 
#     "2023-02-26", "2023-02-19", "2023-02-12", "2023-02-05", 
#     "2023-01-29", "2023-01-22", "2023-01-15", "2023-01-08", "2023-01-01", 
#     "2022-12-25", "2022-12-18", "2022-12-11", "2022-12-04", 
#     "2022-11-27", "2022-11-20", "2022-11-13", "2022-11-06", 
#     "2022-10-30", "2022-10-23", "2022-10-16", "2022-10-09", "2022-10-02", 
#     "2022-09-25", "2022-09-18", "2022-09-11", "2022-09-04", 
#     "2022-08-28", "2022-08-21", "2022-08-14", "2022-08-07", 
#     "2022-07-31", "2022-07-24", "2022-07-17", "2022-07-10", "2022-07-03", 
#     "2022-06-26", "2022-06-19", "2022-06-12", "2022-06-05", 
#     "2022-05-29", "2022-05-22", "2022-05-15", "2022-05-08", "2022-05-01", 
#     "2022-04-22", "2022-04-17", "2022-04-10", "2022-04-03", 
#     "2022-03-27", "2022-03-20", "2022-03-13", "2022-03-06", 
#     "2022-02-27", "2022-02-20", "2022-02-13", "2022-02-06", 
#     "2022-01-30", "2022-01-23", "2022-01-16", "2022-01-09", "2022-01-02", 
#     "2021-12-26", "2021-12-19", "2021-12-12", "2021-12-05", 
#     "2021-11-28", "2021-11-21", "2021-11-14", "2021-11-07", 
#     "2021-10-31", "2021-10-24", "2021-10-17", "2021-10-10", "2021-10-03", 
#     "2021-09-26", "2021-09-19", "2021-09-12", "2021-09-05", 
#     "2021-08-29", "2021-08-22", "2021-08-15", "2021-08-08", "2021-08-01", 
#     "2021-07-25", "2021-07-18", "2021-07-11", "2021-07-04", 
# ]
weeks = ["2024-11-10"]


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
    os.makedirs(folder_path, exist_ok=True)  # 폴더 경로가 없으면 생성

    # 주간별로 데이터 수집
    for week in weeks:
        # 주간 날짜를 파일 이름에 사용
        pages = [
            {
                "url": f"https://www.netflix.com/tudum/top10/{country_code}?week={week}",
                "file_name": f"{folder_path}/{country_name}FilmsTop10_{week}.json"
            },
            {
                "url": f"https://www.netflix.com/tudum/top10/{country_code}/tv?week={week}",
                "file_name": f"{folder_path}/{country_name}TvTop10_{week}.json"
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
