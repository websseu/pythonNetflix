from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import os
import json
import time

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 최상위 releasing 폴더 생성
base_folder_path = "releasing"
os.makedirs(base_folder_path, exist_ok=True)

# 웹드라이버 설정(로컬)
browser = webdriver.Chrome()
browser.get("https://media.netflix.com/ko/")

# 페이지가 완전히 로드될 때까지 대기
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "AppContainer"))
    )
    print("페이지가 완전히 로드되었습니다.")
    
    # 스크롤을 끝까지 내리며 이미지 로드 대기
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        for i in range(0, last_height, 500):
            browser.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.5)  # 천천히 스크롤
        
        time.sleep(2)  # 페이지 로드 대기
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(10)

    # 페이지 소스 파싱
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 정보를 저장할 리스트
    releasing_data = []

    # 리스트 선택
    lists = soup.select(".item-enter-done")

    for idx, list in enumerate(lists, start=1):
        data_testid = list.get("data-testid")
        if data_testid and "NetflixOriginal:" in data_testid:
            data_testid = data_testid.split(":")[-1]  # 숫자 부분만 가져오기
        
        image_div = list.select_one(".boxshot > div")
        date_elem = list.select_one(".Hawkins-Text-default")
        title_elem = list.select_one("a[title]")
        
        image_url = None
        if image_div and 'style' in image_div.attrs:
            style = image_div.attrs['style']
            start_idx = style.find('url("') + len('url("') 
            end_idx = style.find('")', start_idx)         
            if start_idx != -1 and end_idx != -1:
                image_url = style[start_idx:end_idx]
        
        release_date = date_elem.text.strip() if date_elem else None
        title = title_elem['title'].strip() if title_elem else None

        # 수집된 정보를 딕셔너리에 저장
        releasing_data.append({
            "num": idx,
            "id": data_testid,
            "title": title,
            "image_url": image_url,
            "release_date": release_date,
        })

    # 결과를 JSON 파일로 저장
    output_file_path = os.path.join(base_folder_path, f"releasing_{current_date}.json")
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(releasing_data, json_file, ensure_ascii=False, indent=4)

    print(f"데이터가 {output_file_path}에 저장되었습니다.")

except TimeoutException:
    print("페이지 로드 실패")

finally:
    # 브라우저 닫기
    browser.quit()
