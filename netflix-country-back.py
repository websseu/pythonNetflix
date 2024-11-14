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
base_folder_path = "country"
os.makedirs(base_folder_path, exist_ok=True)

# 나라와 주간 설정
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

# weeks = [
#     "2024-11-03", "2024-11-10",
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
weeks = ["2024-11-10", "2024-11-03"]

# URL 템플릿
url_template = {
    "films": "https://www.netflix.com/tudum/top10/{country}?week={week}",
    "tv": "https://www.netflix.com/tudum/top10/{country}/tv?week={week}"
}

# 웹드라이버 백그라운드 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 나라와 주별 데이터 수집
for country in countries:
    # 나라별 폴더 생성
    country_folder_path = os.path.join(base_folder_path, country)
    os.makedirs(country_folder_path, exist_ok=True)

    for week in weeks:
        # 결과 데이터를 저장할 딕셔너리
        data = {
            "kind": "Netflix Country",
            "date": current_date,
            "date": week,
            "films": [],
            "tv": []
        }

        # 각 URL에 대해 데이터 수집
        for category, url in url_template.items():
            url = url.format(country=country, week=week)  # 나라와 주간 정보 적용
            browser.get(url)
            
            # 페이지가 로드될 시간을 기다림
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "weekly-lists")))
                print(f"{country}의 {category} 페이지가 완전히 로드되었습니다.")
                time.sleep(3)

                # 페이지 소스 파싱
                soup = BeautifulSoup(browser.page_source, 'html.parser')

                # 이미지 및 각종 정보 추출
                banners = soup.select(".banner-title")
                table_rows = soup.select("tbody tr")

                for item, row in zip(banners, table_rows):
                    image = item.select_one("picture img").get("src") if item.select_one("picture img") else "N/A"
                    ranking = row.select_one("td:nth-child(1)").get_text(strip=True) if row.select_one("td:nth-child(1)") else "N/A"
                    title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
                    week_number = row.select_one("td:nth-child(3) .wk-number").get_text(strip=True) if row.select_one("td:nth-child(3) .wk-number") else "N/A"
                    watch_id = row.get("data-id", "N/A")

                    # 각 항목의 데이터를 저장
                    entry_data = {
                        "rank": ranking,
                        "title": title,
                        "week": week_number,
                        "image": image,
                        "watchID": watch_id
                    }

                    # data 딕셔너리의 films 또는 tv 항목에 데이터 추가
                    data[category].append(entry_data)

            except TimeoutException:
                print(f"{country}의 {category} 페이지 로드 실패")

        # 나라별 JSON 파일로 저장
        output_file_path = os.path.join(country_folder_path, f"{country}_{week}.json")
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print(f"{country}의 {week} 데이터가 {output_file_path}에 저장되었습니다.")

# 브라우저 닫기
browser.quit()
