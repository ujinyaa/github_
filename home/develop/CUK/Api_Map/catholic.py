import json
import time
import os
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROMEDRIVER_PATH = r'개인의 크롬드라이버 경로를 넣어주세요'
KEYWORD = '부천 가톨릭대학교 근처 맛집'
SAVE_PATH = 'Catholic/food_data.json'

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get('https://map.kakao.com/')

def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

def food_list_print():
    time.sleep(0.2)
    food_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

    for index in range(len(food_list)):
        try:
            item = food_list[index]

            name = item.find_element(By.CSS_SELECTOR, '.head_item .link_name').text
            type_ = item.find_element(By.CSS_SELECTOR, '.head_item .subcategory').text

            addr_items = item.find_elements(By.CSS_SELECTOR, '.info_item.addr p')
            addr1 = addr_items[0].text if len(addr_items) > 0 else ''
            addr2 = addr_items[1].text[5:] if len(addr_items) > 1 else ''

            # 평점
            try:
                rating_elem = item.find_element(By.CSS_SELECTOR, 'em[data-id="scoreNum"]')
                rating_text = rating_elem.text.strip()
                rating = float(rating_text) if rating_text else None
            except:
                rating = None

            try:
                review_elem = item.find_element(By.CSS_SELECTOR, '.rating .review')
                review_text = review_elem.text
                review_num = re.findall(r'\d+', review_text)
                review_count = int(review_num[-1]) if review_num else 0
            except:
                review_count = 0

            food_data = {
                'name': name,
                'type': type_,
                'address1': addr1,
                'address2': addr2,
                'rating': rating,
                'review_count': review_count
            }

            food_dict['음식점정보'].append(food_data)
            print(f'{name} ...완료')

        except Exception as e:
            print(f"❌ 항목 {index} 처리 중 오류 발생:", e)


time_wait(10, 'div.box_searchbar > input.query')
search = driver.find_element(By.CSS_SELECTOR, 'div.box_searchbar > input.query')
search.send_keys(KEYWORD)
search.send_keys(Keys.ENTER)

sleep(1)
place_tab = driver.find_element(By.CSS_SELECTOR, r'#info\.main\.options > li.option1 > a')
place_tab.send_keys(Keys.ENTER)
sleep(1)

food_dict = {'음식점정보': []}
start = time.time()
print('[크롤링 시작...]')

page = 1
page2 = 0
error_cnt = 0

while True:
    try:
        page2 += 1
        print("**", page, "**")
        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)
        food_list_print()

        food_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')
        if len(food_list) < 15:
            break
        if not driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
            break
        if page2 % 5 == 0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            page2 = 0
        page += 1

    except Exception as e:
        error_cnt += 1
        print(e)
        print('ERROR!' * 3)
        if error_cnt > 5:
            break

elapsed_time = round(time.time() - start, 2)
total_collected = len(food_dict['음식점정보'])

print('[데이터 수집 완료]')
print(f'소요 시간 : {elapsed_time}초')
print(f'총 {total_collected}개 장소 수집 완료 ✅')

driver.quit()

os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

with open(SAVE_PATH, 'w', encoding='utf-8') as f:
    json.dump(food_dict, f, indent=4, ensure_ascii=False)
print(f'[JSON 저장 완료] → {SAVE_PATH}')
