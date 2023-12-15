# pyinstaller --onefile --add-binary "chromedriver.exe;." ~.py
__author__  = "kay <reddevil8407@gmail.com>"
__status__  = "production"
__version__ = "1.0.0"
__date__    = "15 Dec 2023"

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

class MainGUI(QDialog, QtStyleTools):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setStyle(self):
        theme = 'dark_blue.xml'
        self.apply_stylesheet(self, theme=theme, invert_secondary=False)
        
    def initUI(self):
        option_frame = QFrame()
        option_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        btn_frame = QFrame()
        btn_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        keyword_frame = QFrame()
        keyword_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        
        main_layout = QHBoxLayout()
        main_option_layout = QFormLayout()
        main_btn_layout = QFormLayout()
        main_keyword_layout = QFormLayout()
        
        option1_layout = QFormLayout()
        btn1_layout = QVBoxLayout()
        keyword_layout = QVBoxLayout()
                
        self.auto_comboBox = QComboBox()
        
        self.gov_comboBox = QComboBox()
        self.cat_comboBox = QComboBox()
        self.cal_comboBox = QComboBox()
        self.scs_comboBox = QComboBox()
        # self.auto_comboBox.setStyleSheet('color:white')
        # self.gov_comboBox.setStyleSheet('color:white')
        # self.cat_comboBox.setStyleSheet('color:white')
        # self.cal_comboBox.setStyleSheet('color:white')
        # self.scs_comboBox.setStyleSheet('color:white')
        
        self.search_btn = QPushBtn('조회')
        self.dir_btn = QPushBtn('파일 확인')
        
        keyword_label = QLabel('키워드 설정')
        keyword_label.setAlignment(Qt.AlignCenter)
        self.keyword1_line = QLineEdit()
        self.keyword2_line = QLineEdit()
        self.keyword3_line = QLineEdit()
        self.keyword_save_btn = QPushBtn('저장')
        
        # self.keyword1_line.setStyleSheet('color:white')
        # self.keyword2_line.setStyleSheet('color:white')
        # self.keyword3_line.setStyleSheet('color:white')
        
        option1_layout.addRow('자동 조회', self.auto_comboBox)
        option1_layout.addRow('주관사 ', self.gov_comboBox)
        option1_layout.addRow('유형(공고)', self.cat_comboBox)
        option1_layout.addRow('유형(일정)', self.cal_comboBox)
        option1_layout.addRow('저장 방식', self.scs_comboBox)
        btn1_layout.addWidget(self.search_btn)
        btn1_layout.addWidget(self.dir_btn)
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword1_line)
        keyword_layout.addWidget(self.keyword2_line)
        keyword_layout.addWidget(self.keyword3_line)
        keyword_layout.addWidget(self.keyword_save_btn)
        
        main_option_layout.addRow(option1_layout)
        main_btn_layout.addRow(btn1_layout)
        main_keyword_layout.addRow(keyword_layout)
        
        option_frame.setLayout(main_option_layout)
        btn_frame.setLayout(main_btn_layout)
        keyword_frame.setLayout(main_keyword_layout)
        
        main_splitter = QSplitter(Qt.Horizontal)
        option_splitter = QSplitter(Qt.Vertical)
        btn_splitter = QSplitter(Qt.Vertical)
        keyword_splitter = QSplitter(Qt.Vertical)
        
        option_splitter.addWidget(option_frame)
        btn_splitter.addWidget(btn_frame)
        keyword_splitter.addWidget(keyword_frame)
        main_splitter.addWidget(option_splitter)
        main_splitter.addWidget(keyword_splitter)
        main_splitter.addWidget(btn_splitter)
        
        main_layout.addWidget(main_splitter)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Give me the house v0.2")    
            
class DirThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.debuggingD = True
        self.dir = ''
        
    def run(self):
        if self.debuggingD:
            if not os.path.exists(self.dir):
                self.create_folder()
                os.startfile(self.dir.split('/')[-1])
            else:
                os.startfile(self.dir.split('/')[-1])
        else:
            os.startfile(self.dir.split('/')[-1])

class KeywordSaveThread(QThread):
    keyword = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyword1 = ''
        self.keyword2 = ''
        self.keyword3 = ''
        self.spath = ''
        
    def run(self):
        f = open(self.spath, 'w')
        f.write(f'keyword1:{self.keyword1}\n')
        f.write(f'keyword2:{self.keyword2}\n')
        f.write(f'keyword3:{self.keyword3}\n')
        f.close()
        ksthread_working = f'{self.keyword1}, {self.keyword2}, {self.keyword3}'
        self.keyword.emit(ksthread_working)
        
class SearchThread(QThread):
    # 조회 & 키워드 확인
    sworking_info = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.auto = ''
        self.dir = ''
        self.gov = ''
        self.category = ''
        self.cal_type = ''
        self.url = ''
        self.url_dict = {}
        self.screen_shot = False
        self.keyword1 = ''
        self.keyword2 = ''
        self.keyword3 = ''
        self.keyword_present = False
        
    def run(self):
        ##### 조회 > 체크 > 저장 > 결과(emit) ######
        chrome_options = Options()
        chrome_options.add_experimental_option('detach', True)
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        if self.category == '일정':
            print(f'%% {self.gov}의 {self.cal_type} {self.category}을 조회하겠습니다.')
            if self.screen_shot:
                self.browser.maximize_window() 
            else:
                self.browser.minimize_window()
        else:
            print(f'%% {self.gov}의 {self.category} 목록을 조회하겠습니다.')
            self.browser.minimize_window()
            
        self.search_doit(auto=self.auto)
        
        self.sworking = False
        self.sworking_info.emit(self.keyword_present)
        
    def search_doit(self, auto):
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if auto:
            for key, val in self.url_dict[self.gov].items():
                self.category = key
                url = val
                self.browser.get(url)
                
                if self.category == '일정':
                    # 임대, 분양 일정 - 스샷 + SCV
                    for i in range(2):
                        lh_cal_type_element = self.browser.find_element(By.NAME, 'calSrchType')
                        lh_cal_type_select = Select(lh_cal_type_element)
                        if i == 0 :
                            lh_cal_type_select.select_by_value('01')
                            self.cal_type = '임대'
                        elif i == 1:
                            lh_cal_type_select.select_by_value('02')
                            self.cal_type = '분양'
                        lh_cal_region_element = self.browser.find_element(By.NAME, 'calSrchLocal')
                        lh_cal_region_select = Select(lh_cal_region_element)
                        lh_cal_region_select.select_by_value('11')
                        lh_cal_search_btn = self.browser.find_element(By.ID, 'btnSah')
                        lh_cal_search_btn.click()
                        # 스샷
                        screen_shot_file_name = f'{self.dir}/{self.gov}_{self.cal_type}_{self.category}_{str(now)}.jpg'
                        scroll_down_element = self.browser.find_element(By.CSS_SELECTOR, '#footer')
                        action = ActionChains(self.browser).move_to_element(scroll_down_element)
                        action.perform()
                        self.browser.maximize_window()
                        print(f'%% {self.gov}_{self.cal_type}_{self.category} 스크린샷 저장 중...')
                        pag.screenshot(screen_shot_file_name)
                        print(f'%% 저장 완료: {file_name}')
                        # CSV
                        print(f'%% {self.gov}_{self.cal_type}_{self.category} CSV 저장 중...')
                        file_name = f'{self.dir}/{self.gov}_{self.cal_type}_{self.category}_{str(now)}.csv'
                        df = pd.read_html(self.browser.page_source)[0]
                        df.dropna(axis='index', how='all', inplace=True)
                        df.dropna(axis='columns', how='all', inplace=True)
                        df = df.drop(['일', '토'], axis='columns')
                        df.fillna('0')
                        self.keyword_check(df)
                        if os.path.exists(file_name):
                            df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                        else:
                            df.to_csv(file_name, encoding='utf-8-sig', index=False)
                        print(f'%% 저장 완료: {file_name}')
                else:
                    #분양, 임대 - 공고
                    lh_region_element = self.browser.find_element(By.NAME, 'cnpCd')
                    lh_region_select = Select(lh_region_element)
                    lh_region_select.select_by_value('11')

                    search_btn = self.browser.find_element(By.ID, 'btnSah')
                    search_btn.click()

                    df = pd.read_html(self.browser.page_source)[0]
                    df.dropna(axis='index', how='all', inplace=True)
                    df.dropna(axis='columns', how='all', inplace=True)
                    df = df.drop(['번호', '지역', '첨부'], axis='columns')
                    df.fillna('0')
                    self.keyword_check(df)
                    
                    file_name = f'{self.dir}/{self.gov}_{self.category}_{str(now)}.csv'
                    print(f'%% {self.gov}_{self.category} 공고 저장 중...')
                    if os.path.exists(file_name):
                        df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                    else:
                        df.to_csv(file_name, encoding='utf-8-sig', index=False)
                    print(f'%% 저장 완료: {file_name}')
        else:
            url = self.url_dict[self.gov][self.category]
            self.browser.get(url)
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
                        print(f'%% {self.gov}_{self.cal_type}_{self.category} 스크린샷 저장 중...')
                        pag.screenshot(screen_shot_file_name)
                        print(f'%% 저장 완료: {screen_shot_file_name}')
                    else:
                        print(f'%% {self.gov}_{self.cal_type}_{self.category} CSV 저장 중...')
                        file_name = f'{self.dir}/{self.gov}_{self.cal_type}_{self.category}_{str(now)}.csv'
                        df = pd.read_html(self.browser.page_source)[0]
                        df.dropna(axis='index', how='all', inplace=True)
                        df.dropna(axis='columns', how='all', inplace=True)
                        df = df.drop(['일', '토'], axis='columns')
                        df.fillna('0')
                        self.keyword_check(df)
                        if os.path.exists(file_name):
                            df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                        else:
                            df.to_csv(file_name, encoding='utf-8-sig', index=False)
                        print(f'%% 저장 완료: {file_name}')
                else:
                    lh_region_element = self.browser.find_element(By.NAME, 'cnpCd')
                    lh_region_select = Select(lh_region_element)
                    lh_region_select.select_by_value('11')

                    search_btn = self.browser.find_element(By.ID, 'btnSah')
                    search_btn.click()

                    print(f'%% {self.gov}_{self.category} 공고 저장 중...')
                    file_name = f'{self.dir}/{self.gov}_{self.category}_{str(now)}.csv'
                    df = pd.read_html(self.browser.page_source)[0]
                    df.dropna(axis='index', how='all', inplace=True)
                    df.dropna(axis='columns', how='all', inplace=True)
                    df = df.drop(['번호', '지역', '첨부'], axis='columns')
                    df.fillna('0')
                    self.keyword_check(df)
                    if os.path.exists(file_name):
                        df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
                    else:
                        df.to_csv(file_name, encoding='utf-8-sig', index=False)
                    print(f'%% 저장 완료: {file_name}')
        
        self.browser.quit()
        
    def keyword_check(self, df):
        if self.category == '일정':
            df = df.astype('str')
            df_keyword1 = df[df['월'].notnull() & df['월'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword2 = df[df['화'].notnull() & df['화'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword3 = df[df['수'].notnull() & df['수'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword4 = df[df['목'].notnull() & df['목'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword5 = df[df['금'].notnull() & df['금'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
        else:
            df_keyword1 = df[df['유형'].notnull() & df['유형'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword2 = df[df['공고명'].notnull() & df['공고명'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword3 = df[df['상태'].notnull() & df['상태'].str.contains(self.keyword1 or self.keyword2 or self.keyword3)]
            df_keyword4 = df_keyword5 = []
            
        if len(df_keyword1) + len(df_keyword2) + len(df_keyword3) + len(df_keyword4) + len(df_keyword5) != 0:
            self.keyword_present = True
        else:
            self.keyword_present = False

class Main(MainGUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.debugging = True
        
        self.setStyle()
        self.initUI()
        
        self.setDefault()
        self.create_folder()
        self.initSetting()

        self.show()
    
    def setDefault(self):
        self.auto_check = False
        self.gov = 'xx'
        self.category = 'xx'
        self.cal_type = 'xx'
        # self.keyword1 = ''
        # self.keyword2 = ''
        # self.keyword3 = ''
        self.keyword_alarm = False
        self.screen_shot = False
        self.ksthread_end = True
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
        self.spath = './settings.txt'
        
    def initSetting(self):
        settings = open(self.spath).read().splitlines()
        self.keyword1 = settings[0].split(':')[-1]
        self.keyword2 = settings[1].split(':')[-1]
        self.keyword3 = settings[2].split(':')[-1]
        
        self.keyword1_line.setText(self.keyword1)
        self.keyword2_line.setText(self.keyword2)
        self.keyword3_line.setText(self.keyword3)
        
        self.auto_comboBox.addItems(['자동', '수동'])
        self.auto_comboBox.activated[str].connect(lambda:self.selected_auto_comboItem(self.auto_comboBox))
        self.gov_comboBox.activated[str].connect(lambda:self.selected_gov_comboItem(self.gov_comboBox))
        self.cat_comboBox.activated[str].connect(lambda:self.selected_cat_comboItem(self.cat_comboBox))
        self.cal_comboBox.activated[str].connect(lambda:self.selected_cal_comboItem(self.cal_comboBox))
        self.scs_comboBox.activated[str].connect(lambda:self.selected_scs_comboItem(self.scs_comboBox))
        
        self.dthread = DirThread(self)
        self.sthread = SearchThread(self)
        self.sthread.sworking_info.connect(self.info_sthread_working)
        self.ksthread = KeywordSaveThread(self)
        self.ksthread.keyword.connect(self.info_ksthread_working)
        
        self.search_btn.setDisabled(True)
        self.search_btn.clicked.connect(self.btn_search_clickEvent)
        self.dir_btn.clicked.connect(self.btn_dir_clickEvent)
        self.keyword_save_btn.clicked.connect(self.warn_keyword_save_event)

    def create_folder(self):
        if self.debugging:
            self.dir = f'./pytoy/house_checker/sch_result' # set your directory for debugging
        else:
            self.dir = f'./sch_result'
        try:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            os.chdir(self.dir.split('/')[1] + '/house_checker')
            self.dir = f'./sch_result'
        except OSError:
            QMessageBox.warning(self, '옵션 경고', '폴더 생성 실패')
        
    def selected_auto_comboItem(self, text):
        if text.currentText() == '자동':
            self.auto_check = True
            self.gov_comboBox.clear()
            self.gov_comboBox.setDisabled(False)
            self.gov_comboBox.addItems(list(self.url_dict.keys()))
            self.cat_comboBox.clear()
            self.cat_comboBox.setDisabled(True)
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.search_btn.setDisabled(True)
        elif text.currentText() == '수동':
            self.auto_check = False
            self.gov_comboBox.clear()
            self.gov_comboBox.setDisabled(False)
            self.gov_comboBox.addItems(list(self.url_dict.keys()))
            self.search_btn.setDisabled(True)
    
    def selected_gov_comboItem(self, text):
        self.gov = text.currentText()
        print(self.gov)
        if self.auto_check:
            if text.currentText() == 'lh':
                self.search_btn.setDisabled(False)
            else:
                QMessageBox.warning(self, '옵션 경고', f'선택한 옵션을 다시 확인하세요: {text.currentText()}')
        else:
            if text.currentText() == 'lh':
                self.cat_comboBox.clear()
                self.cat_comboBox.setDisabled(False)
                self.cat_comboBox.addItems(list(self.url_dict[text.currentText()].keys()))
                self.search_btn.setDisabled(True)
            else:
                QMessageBox.warning(self, '옵션 경고', f'선택한 옵션을 다시 확인하세요: {text.currentText()}')
                
    def selected_cat_comboItem(self, text):
        self.category = text.currentText()
        print(f'{self.category}')
        if text.currentText() == '일정':
            self.cal_comboBox.addItems(['분양', '임대'])
            self.search_btn.setDisabled(True)
            self.cal_comboBox.setDisabled(False)
            self.scs_comboBox.setDisabled(False)
        elif text.currentText() == '분양':
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.search_btn.setDisabled(False)
        elif text.currentText() == '임대':
            self.cal_comboBox.clear()
            self.cal_comboBox.setDisabled(True)
            self.scs_comboBox.clear()
            self.scs_comboBox.setDisabled(True)
            self.search_btn.setDisabled(False)
        else:
            QMessageBox(self, '옵션 경고', f'선택한 옵션을 다시 확인하세요: {text.currentText()}')
            
    def selected_cal_comboItem(self, text):
        self.cal_type = text.currentText()
        print(f'{self.cal_type}')
        self.scs_comboBox.addItems(['CSV', '스크린샷'])
        self.search_btn.setDisabled(True)
    
    def selected_scs_comboItem(self, text):
        if text.currentText() == 'CSV':
            self.screen_shot = False
        elif text.currentText() == '스크린샷':
            self.screen_shot = True
        self.search_btn.setDisabled(False)
        
    def btn_search_clickEvent(self):
        self.search_btn.setDisabled(True)
        self.dir_btn.setDisabled(True)
        
        if self.category == '일정':
            s_option = f'{self.gov}, {self.cal_type}, {self.category}'
        else:
            s_option = f'{self.gov}, {self.category}'
        
        reply = QMessageBox.information(self, '조회 시작', f'조회를 시작합니다.\n{s_option}',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sthread.start()
            self.sthread.auto = self.auto_check
            self.sthread.dir = self.dir
            self.sthread.gov = self.gov
            self.sthread.category = self.category
            self.sthread.cal_type = self.cal_type
            self.sthread.url_dict = self.url_dict
            self.sthread.screen_shot = self.screen_shot
            self.sthread.keyword1 = self.keyword1
            self.sthread.keyword2 = self.keyword2
            self.sthread.keyword3 = self.keyword3
            self.sthread.keyword_present = False

    @pyqtSlot(bool)
    def info_sthread_working(self, key_present):
        self.search_btn.setDisabled(False)
        self.dir_btn.setDisabled(False)
        if key_present:
            key_present_str = f'키워드와 일치한 정보를 발견했습니다.\n파일을 확인하시겠습니까?'
        else:
            key_present_str = f'키워드와 일치한 정보가 없습니다.\n파일을 확인하시겠습니까?'
        reply = QMessageBox.information(self, '조회 완료', key_present_str,
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.btn_dir_clickEvent()
        else: 
            pass

    def btn_dir_clickEvent(self):
        self.dthread.start()
        self.dthread.debuggingD = self.debugging
        self.dthread.dir = self.dir
    
    def warn_keyword_save_event(self, event):
        self.keyword1 = self.keyword1_line.text()
        self.keyword2 = self.keyword2_line.text()
        self.keyword3 = self.keyword3_line.text()
        
        if (self.keyword1 == '') or (self.keyword2 == '' and self.keyword3 != ''):
            QMessageBox.warning(self, 'Warnning', '순서대로 입력해주세요.')
        else:
            self.btn_keyword_save_clickEvent()

    def btn_keyword_save_clickEvent(self):
        reply = QMessageBox.question(self, 'Save Check', '키워드를 저장하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ksthread.start()
            self.ksthread.keyword1 = self.keyword1
            self.ksthread.keyword2 = self.keyword2
            self.ksthread.keyword3 = self.keyword3
            self.ksthread.spath = self.spath
        else:
            pass

    @pyqtSlot(str)
    def info_ksthread_working(self, ks_working):
        QMessageBox.information(self, '키워드 저장 완료', f'키워드 저장이 완료되었습니다.\n{ks_working}')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())