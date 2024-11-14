from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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

# URL 템플릿
url_template = {
    "films": "https://www.netflix.com/tudum/top10/{country}?week={current_date}",
    "tv": "https://www.netflix.com/tudum/top10/{country}/tv?week={current_date}"
}

# 웹드라이버 백그라운드 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 나라별 데이터 수집
for country in countries:
    # 나라별 폴더 생성
    country_folder_path = os.path.join(base_folder_path, country)
    os.makedirs(country_folder_path, exist_ok=True)

    # 결과 데이터를 저장할 딕셔너리
    data = {
        "kind": "Netflix Country",
        "date": current_date,
        "films": [],
        "tv": []
    }

    # 각 URL에 대해 데이터 수집
    for category, url in url_template.items():
        url = url.format(country=country, current_date=current_date)  # 나라와 주간 정보 적용
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
    output_file_path = os.path.join(country_folder_path, f"{country}_{current_date}.json")
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"{country}의 데이터가 {output_file_path}에 저장되었습니다.")

# 브라우저 닫기
browser.quit()
