# pyinstaller --onefile --add-binary "chromedriver.exe;." ~.py

import os, sys, datetime

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet, QtStyleTools

import pandas as pd
import pyautogui as pag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class QPushBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        font = QFont('Helvetica')
        self.setFont(font)
        
class Main(QDialog, QtStyleTools):
    def __init__(self):
        super().__init__()
        
        self.debugging = False
        
        self.auto_check = False
        self.gov = 'xx'
        self.category = 'xx'
        self.cal_type = 'xx'
        self.screen_shot = False
        self.url_dict = {
                            'lh': {
                                '분양': 'https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1027',
                                '임대': 'https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026',
                                '일정': 'https://apply.lh.or.kr/lhapply/apply/sc/list.do?mi=1312',
                            },
                            # 'sh': {
                            #     '임대': 'https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do?multi_itm_seq=2',
                            #     '분양': 'https://www.i-sh.co.kr/main/lay2/program/S1T294C296/www/brd/m_244/list.do?multi_itm_seq=1',
                            # }
                        }

        self.dir = self.create_folder()
        self.setStyle()
        self.initUI()
        
    def setStyle(self):
        extra = {}
        extra['font_family'] = 'Roboto'
        extra['density_scale'] = str(0)
        theme = 'dark_teal.xml'
        invert = True
        self.apply_stylesheet(self, theme=theme, extra=extra, invert_secondary=invert)
        
    def initUI(self):
        option_frame = QFrame()
        option_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        btn_frame = QFrame()
        btn_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        
        main_layout = QHBoxLayout()
        main_option_layout = QFormLayout()
        main_btn_layout = QFormLayout()
        
        option1_layout = QFormLayout()
        btn1_layout = QVBoxLayout()
        
        self.auto_comboBox = QComboBox()
        self.auto_comboBox.addItems(['자동', '수동'])
        self.auto_comboBox.activated[str].connect(lambda:self.selected_auto_comboItem(self.auto_comboBox))
        self.gov_comboBox = QComboBox()
        self.gov_comboBox.activated[str].connect(lambda:self.selected_gov_comboItem(self.gov_comboBox))
        self.cat_comboBox = QComboBox()
        self.cat_comboBox.activated[str].connect(lambda:self.selected_cat_comboItem(self.cat_comboBox))
        self.cal_comboBox = QComboBox()
        self.cal_comboBox.activated[str].connect(lambda:self.selected_cal_comboItem(self.cal_comboBox))
        self.scs_comboBox = QComboBox()
        self.scs_comboBox.activated[str].connect(lambda:self.selected_scs_comboItem(self.scs_comboBox))
        
        self.check_btn = QPushBtn('조회')
        self.check_btn.setDisabled(True)
        self.check_btn.clicked.connect(self.btn_check_clickEvent)
        self.dir_btn = QPushBtn('파일 확인')
        self.dir_btn.clicked.connect(self.btn_dir_clickEvent)
        
        option1_layout.addRow('자동 조회', self.auto_comboBox)
        option1_layout.addRow('주관사 ', self.gov_comboBox)
        option1_layout.addRow('유형(공고)', self.cat_comboBox)
        option1_layout.addRow('유형(일정)', self.cal_comboBox)
        option1_layout.addRow('저장 방식', self.scs_comboBox)
        btn1_layout.addWidget(self.check_btn)
        btn1_layout.addWidget(self.dir_btn)
        
        main_option_layout.addRow(option1_layout)
        main_btn_layout.addRow(btn1_layout)
        
        option_frame.setLayout(main_option_layout)
        btn_frame.setLayout(main_btn_layout)
        
        main_splitter = QSplitter(Qt.Horizontal)
        option_splitter = QSplitter(Qt.Vertical)
        btn_splitter = QSplitter(Qt.Vertical)
        
        option_splitter.addWidget(option_frame)
        btn_splitter.addWidget(btn_frame)
        main_splitter.addWidget(option_splitter)
        main_splitter.addWidget(btn_splitter)
        
        main_layout.addWidget(main_splitter)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Give me the house v0.2")
        self.show()
        
    def selected_auto_comboItem(self, text):
        if text.currentText() == '자동':
            self.auto_check = True
            self.gov_comboBox.clear()
            self.gov_comboBox.setDisabled(True)
            self.cat_comboBox.clear()
            self.cat_comboBox.setDisabled(True)
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.check_btn.setDisabled(True)
        elif text.currentText() == '수동':
            self.auto_check = False
            self.gov_comboBox.clear()
            self.gov_comboBox.setDisabled(False)
            self.gov_comboBox.addItems(list(self.url_dict.keys()))
            self.check_btn.setDisabled(True)
    
    def selected_gov_comboItem(self, text):
        self.gov = text.currentText()
        print(self.gov)
        if text.currentText() == 'lh':
            self.cat_comboBox.clear()
            self.cat_comboBox.setDisabled(False)
            self.cat_comboBox.addItems(list(self.url_dict[text.currentText()].keys()))
            self.check_btn.setDisabled(True)
        else:
            print(f'[ERROR] 선택한 옵션을 다시 확인하세요: {text.currentText()}')
            
    def selected_cat_comboItem(self, text):
        self.category = text.currentText()
        print(f'{self.category}')
        if text.currentText() == '일정':
            self.cal_comboBox.addItems(['분양', '임대'])
            self.check_btn.setDisabled(True)
            self.cal_comboBox.setDisabled(False)
            self.scs_comboBox.setDisabled(False)
        elif text.currentText() == '분양':
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.check_btn.setDisabled(False)
        elif text.currentText() == '임대':
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.check_btn.setDisabled(False)
        else:
            print(f'[ERROR] 선택한 옵션을 다시 확인하세요: {text.currentText()}')
            
    def selected_cal_comboItem(self, text):
        self.cal_type = text.currentText()
        print(f'{self.cal_type}')
        self.scs_comboBox.addItems(['CSV', '스크린샷'])
        self.check_btn.setDisabled(True)
    
    def selected_scs_comboItem(self, text):
        if text.currentText() == 'CSV':
            self.screen_shot = False
        elif text.currentText() == '스크린샷':
            self.screen_shot = True
        self.check_btn.setDisabled(False)
        
    def btn_check_clickEvent(self):
        self.check_btn.setDisabled(True)
        self.dir_btn.setDisabled(True)
        
        chrome_options = Options()
        chrome_options.add_experimental_option('detach', True)
        # self.browser = webdriver.Chrome(options=chrome_options)
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        if self.category == '임대':
            print(f'%% {self.gov}의 {self.category} 목록을 조회하겠습니다.')
            self.browser.minimize_window() 
        elif self.category == '분양':
            print(f'%% {self.gov}의 {self.category} 목록을 조회하겠습니다.')
            self.browser.minimize_window() 
        elif self.category == '일정':
            print(f'%% {self.gov}의 {self.cal_type} {self.category}을 조회하겠습니다.')
            if self.screen_shot:
                self.browser.maximize_window() 
            else:
                self.browser.minimize_window()
        
        url = self.url_dict[self.gov][self.category]
        self.browser.get(url)
        self.doit(auto=self.auto_check)
        
    def doit(self, auto):
        self.check_btn.setDisabled(True)
        self.dir_btn.setDisabled(True)
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if auto:
            pass
        else:
            if self.gov == 'lh':
                if self.category == '일정':
                    lh_cal_type_element = self.browser.find_element(By.NAME, 'calSrchType')
                    lh_cal_type_select = Select(lh_cal_type_element)
                    if self.cal_type == '임대':
                        lh_cal_type_select.select_by_value('01')
                    elif self.cal_type == '분양':
                        lh_cal_type_select.select_by_value('02')
                        
                    lh_cal_region_element = self.browser.find_element(By.NAME, 'calSrchLocal')
                    lh_cal_region_select = Select(lh_cal_region_element)
                    lh_cal_region_select.select_by_value('11')
                    
                    lh_cal_search_btn = self.browser.find_element(By.ID, 'btnSah')
                    lh_cal_search_btn.click()
                    
                    if self.screen_shot:
                        screen_shot_file_name = f'{self.dir}/{self.gov}_{self.cal_type}_{self.category}_{str(now)}.jpg'
                        scroll_down_element = self.browser.find_element(By.CSS_SELECTOR, '#footer')
                        action = ActionChains(self.browser).move_to_element(scroll_down_element)
                        action.perform()
                        print(f'저장 중...')
                        pag.screenshot(screen_shot_file_name)
                    else:
                        print(f'저장 중...')
                        file_name = f'{self.dir}/{self.gov}_{self.cal_type}_{self.category}_{str(now)}.csv'
                        df = pd.read_html(self.browser.page_source)[0]
                        df.dropna(axis='index', how='all', inplace=True)
                        df.dropna(axis='columns', how='all', inplace=True)
                        if os.path.exists(file_name):
                            df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                        else:
                            df.to_csv(file_name, encoding='utf-8-sig', index=False)
                    
                else:
                    lh_region_element = self.browser.find_element(By.NAME, 'cnpCd')
                    lh_region_select = Select(lh_region_element)
                    lh_region_select.select_by_value('11')

                    search_btn = self.browser.find_element(By.ID, 'btnSah')
                    search_btn.click()

                    df = pd.read_html(self.browser.page_source)[0]
                    df.dropna(axis='index', how='all', inplace=True)
                    df.dropna(axis='columns', how='all', inplace=True)
                    df = df.drop(['번호', '지역', '첨부'], axis='columns')
                    
                    file_name = f'{self.dir}/{self.gov}_{self.category}_{str(now)}.csv'
                    print(f'%% 저장 중...')
                    if os.path.exists(file_name):
                        df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                    else:
                        df.to_csv(file_name, encoding='utf-8-sig', index=False)
        
        self.browser.quit()
        print(f'%% 저장 완료: {file_name}')
        self.check_btn.setDisabled(False)
        self.dir_btn.setDisabled(False)

    def btn_dir_clickEvent(self):
        os.startfile(self.dir.split('/')[-1])
    
    def create_folder(self):
        # path = os.path.dirname(os.path.abspath(__file__))
        # print(path)
        if self.debugging:
            dir = f'./sch_result'
        else:
            dir = f'./sch_result'
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                print(dir)
        except OSError:
            print("[Error] Failed to create the directory.")
        
        return dir
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
