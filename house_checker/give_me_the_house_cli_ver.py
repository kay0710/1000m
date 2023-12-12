import os, time
import pandas as pd
import pyautogui as pag
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

screen_shot = False
url_dict = {
    'lh': {
        '임대': 'https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026',
        '분양': 'https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1027',
        '일정': 'https://apply.lh.or.kr/lhapply/apply/sc/list.do?mi=1312',
    },
    # 'sh': {
    #     '임대': 'https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do?multi_itm_seq=2',
    #     '분양': 'https://www.i-sh.co.kr/main/lay2/program/S1T294C296/www/brd/m_244/list.do?multi_itm_seq=1',
    # }
}

# for i in range(3):
#     print(f'기관명: {url_dict.keys()}')
#     gov = input('기관 선택하세요: ')
    
#     if gov == 'lh':
#         break
#     # elif gov == 'sh':
#     #     break
#     else:
#         if i < 2:
#             print('다시 확인해주세요.')
#         else:
#             print('오류 3번으로 종료합니다.')
#             exit()
gov = 'lh'
category = 'xx'
cal_type = 'xx'

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

print('************ Give Me the house v0.1 *************')

for i in range(3):
    print(f'조회 목록: {url_dict[gov].keys()}')
    category = input('조회 목록을 보고 원하는 옵션을 입력하세요: ')
    
    if category == '임대':
        print(f'%% {gov}의 {category} 목록을 조회하겠습니다.')
        browser = webdriver.Chrome(options=chrome_options)
        browser.minimize_window() 
        break
    elif category == '분양':
        print(f'%% {gov}의 {category} 목록을 조회하겠습니다.')
        browser = webdriver.Chrome(options=chrome_options)
        browser.minimize_window() 
        break
    elif category == '일정':
        cal_type = input('["임대", "분양"] 중 선택해서 입력하세요: ')
        print(f'%% {gov}의 {cal_type} {category}을 조회하겠습니다.')
        browser = webdriver.Chrome(options=chrome_options)
        if screen_shot:
            browser.maximize_window() 
        else:
            browser.minimize_window()
        break
    else:
        if i < 2:
            print('다시 확인해주세요.')
        else:
            print('오류 3번으로 종료합니다.')
            exit()           
            
url = url_dict[gov][category]
# browser = webdriver.Chrome(options=chrome_options)
# browser.minimize_window()
browser.get(url)

now = datetime.now().strftime('%Y%m%d_%H%M%S')

if gov == 'lh':
    if category == '일정':
        lh_cal_type_element = browser.find_element(By.NAME, 'calSrchType')
        lh_cal_type_select = Select(lh_cal_type_element)
        if cal_type == '임대':
            lh_cal_type_select.select_by_value('01')
        elif cal_type == '분양':
            lh_cal_type_select.select_by_value('02')
            
        lh_cal_region_element = browser.find_element(By.NAME, 'calSrchLocal')
        lh_cal_region_select = Select(lh_cal_region_element)
        lh_cal_region_select.select_by_value('11')
        
        lh_cal_search_btn = browser.find_element(By.ID, 'btnSah')
        lh_cal_search_btn.click()
        
        if screen_shot:
            screen_shot_file_name = f'./pytoy/house_checker/result/{gov}_{cal_type}_{category}_{str(now)}.jpg'
            scroll_down_element = browser.find_element(By.CSS_SELECTOR, '#footer')
            action = ActionChains(browser).move_to_element(scroll_down_element)
            action.perform()
            print(f'저장 중...')
            
            pag.screenshot(screen_shot_file_name)
        else:
            print(f'저장 중...')
            file_name = f'./pytoy/house_checker/result/{gov}_{cal_type}_{category}_{str(now)}.csv'
            df = pd.read_html(browser.page_source)[0]
            df.dropna(axis='index', how='all', inplace=True)
            df.dropna(axis='columns', how='all', inplace=True)
            if os.path.exists(file_name):
                df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
            else:
                df.to_csv(file_name, encoding='utf-8-sig', index=False)
        
    else:
        lh_region_element = browser.find_element(By.NAME, 'cnpCd')
        lh_region_select = Select(lh_region_element)
        lh_region_select.select_by_value('11')

        search_btn = browser.find_element(By.ID, 'btnSah')
        search_btn.click()

        df = pd.read_html(browser.page_source)[0]
        df.dropna(axis='index', how='all', inplace=True)
        df.dropna(axis='columns', how='all', inplace=True)
        df = df.drop(['번호', '지역', '첨부'], axis='columns')
        
        file_name = f'./pytoy/house_checker/result/{gov}_{category}_{str(now)}.csv'
        print(f'%% 저장 중...')
        if os.path.exists(file_name):
            df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
        else:
            df.to_csv(file_name, encoding='utf-8-sig', index=False)
# elif gov == 'sh':
#     type_btn = browser.find_element(By.CLASS_NAME, 'bg-chk')
            
#     search_btn = browser.find_element(By.CLASS_NAME, 'btn btnGreen')
#     search_btn.click()
    
#     df = pd.read_html(browser.page_source)[0]
#     df.dropna(axis='index', how='all', inplace=True)
#     df.dropna(axis='columns', how='all', inplace=True)
#     df = df.drop(['번호', '담당부서'], axis='columns')

browser.quit()
print(f'%% 저장 완료')
exit()
