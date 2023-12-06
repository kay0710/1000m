import sys, os, io, requests, datetime
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from helpers import bg_helpers
from qt_material import apply_stylesheet, QtStyleTools

class QPushBtnIcon(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(200)
        self.setFixedWidth(200)
        self.setIconSize(QSize(192, 192))
class QPushBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        font = QFont('Helvetica')
        # font.setBold(True)
        self.setFont(font)
        
class Main(QDialog, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.dabugging = True
        
        self.setDefault(debugging=self.dabugging)
        self.setStyle()
        self.initUI()
        self.initSettings()
        
    def setStyle(self):
        extra = {}
        extra['font_family'] = 'Roboto'
        extra['density_scale'] = str(0)
        theme = 'dark_blue.xml'
        invert = True
        self.apply_stylesheet(self, theme=theme, extra=extra, invert_secondary=invert)
    
    def initUI(self):
        prompt_frame = QFrame()
        prompt_frame.setFrameShape(QFrame.StyledPanel | QFrame.Sunken)
        userinfo_frame = QFrame()
        userinfo_frame.setFrameShape(QFrame.StyledPanel | QFrame.Sunken)
        filelist_frame = QFrame()
        filelist_frame.setFrameShape(QFrame.StyledPanel | QFrame.Sunken)
        orgimg_frame = QFrame()
        orgimg_frame.setFrameShape(QFrame.StyledPanel | QFrame.Sunken)
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel | QFrame.Sunken)
        
        main_layout = QVBoxLayout()
        main_prompt_layout = QFormLayout()
        main_userinfo_layout = QFormLayout()
        main_filelist_layout = QHBoxLayout()
        
        prompt1_layout = QHBoxLayout()
        prompt2_layout = QVBoxLayout()
        fileload_btn_layout = QHBoxLayout()
        img_org_layout = QHBoxLayout()
        img_result_layout = QHBoxLayout()
        
        prompt_btn = QPushBtn('번역')
        prompt_btn.clicked.connect(self.btn_trans_clicked)
        fileload_btn = QPushBtn('불러오기')
        fileload_btn.clicked.connect(self.load_file)
        doit_btn = QPushBtn('Do it')
        doit_btn.clicked.connect(self.app_doit)
        
        self.prompt_line = QLineEdit('크리스마스 트리', parent=self)
        self.prompt_label = QLabel('', parent=self)
        self.userinfo_select_label = QLabel('', parent=self)
        self.userinfo_credit_label = QLabel('9999.9', parent=self)
        self.img_org_label = QLabel(parent=self)
        self.img_result_label = QLabel(parent=self)
        
        self.file_list = QTableWidget(self)
        self.file_list.setRowCount(5)
        self.file_list.setColumnCount(3)
        self.file_list.setColumnWidth(0, 150)
        self.file_list.setColumnWidth(1, 700)
        self.file_list.setHorizontalHeaderLabels(['image name', 'path', 'size'])
        self.file_list.cellDoubleClicked.connect(self.filelist_dclicked)
        self.file_list.cellDoubleClicked.connect(self.prev_org_image)
        
        prompt1_layout.addWidget(self.prompt_line)
        prompt1_layout.addWidget(prompt_btn)
        prompt2_layout.addWidget(self.prompt_label)
        fileload_btn_layout.addWidget(fileload_btn)
        fileload_btn_layout.addWidget(doit_btn)
        img_org_layout.addWidget(self.img_org_label)
        img_result_layout.addWidget(self.img_result_label)
        
        main_prompt_layout.addRow('배경 설명: ', prompt1_layout)
        main_prompt_layout.addRow('번역 결과: ', prompt2_layout)
        main_prompt_layout.addRow(fileload_btn_layout)
        main_userinfo_layout.addRow('선택한 파일: ', self.userinfo_select_label)
        main_userinfo_layout.addRow('남은 크레딧: ', self.userinfo_credit_label)
        main_filelist_layout.addWidget(self.file_list)
        
        prompt_frame.setLayout(main_prompt_layout)
        userinfo_frame.setLayout(main_userinfo_layout)
        filelist_frame.setLayout(main_filelist_layout)
        orgimg_frame.setLayout(img_org_layout)
        result_frame.setLayout(img_result_layout)
                
        main_splitter = QSplitter(Qt.Vertical)
        splitter1 = QSplitter(Qt.Horizontal) # 위 - prompt, info
        splitter2 = QSplitter(Qt.Horizontal) # 아래 왼쪽 - file list
        splitter3 = QSplitter(Qt.Horizontal) # 아래 오른쪽 - orgimg, result
        
        splitter3.resize(1000,520)
        
        splitter1.addWidget(prompt_frame)
        splitter1.addWidget(userinfo_frame)
        splitter2.addWidget(filelist_frame)
        splitter3.addWidget(orgimg_frame)
        splitter3.addWidget(result_frame)
        main_splitter.addWidget(splitter1)
        main_splitter.addWidget(splitter2)
        main_splitter.addWidget(splitter3)
        
        main_layout.addWidget(main_splitter)
        
        self.setLayout(main_layout)
        self.setWindowTitle('BG Editor v0.2')
        self.resize(1100, 950)
        self.center()
        self.show()
        
    def btn_trans_clicked(self):
        self.USER_PROMPT = self.prompt_line.text()
        print(f"[CHECK] User input: {self.USER_PROMPT}")
        self.INPUT_PROMPT = bg_helpers.trans_prompt(self.USER_PROMPT, 'naver')
        self.prompt_label.setText(self.INPUT_PROMPT)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def setDefault(self, debugging):
        self.clicked_path = '?'
        self.target_path = '?'
        self.IMG = ''
        self.USER_PROMPT = ''
        self.DIR_NAME = 'bg' 
        self.INPUT_PROMPT = ''
        self.MY_API = 'b70f19ea7789c256edf7d7cb31bfc26c58a01ba784b8d51c0da3fb99051ffbea80f2b816e75fe705f5acab2ce255eca8'
        self.BG_URL = 'https://clipdrop-api.co/replace-background/v1'
        self.UP_URL = 'https://clipdrop-api.co/image-upscaling/v1/upscale'
        
        if debugging:
            # debugging mode
            self.BGRESULT_PATH = './bg_editor/cd/bgedit/' 
            self.UPRESULT_PATH = './bg_editor/cd/upscaled/' 
            self.spath = './bg_editor/settings.txt'
            self.default_path = './bg_editor/data'
        else:
            # install mode
            self.BGRESULT_PATH = './cd/bgedit/'
            self.UPRESULT_PATH = './cd/upscaled/'
            self.spath = './settings.txt'
            self.default_path = './data'
        
        self.BGRESULT_DIR = bg_helpers.create_dir(self.BGRESULT_PATH, self.DIR_NAME)
        self.UPRESULT_DIR = bg_helpers.create_dir(self.UPRESULT_PATH, self.DIR_NAME)
    
    def initSettings(self):
        self.settings = open(self.spath).read().splitlines()
        self.credits = self.settings[0].split(':')[-1]
        self.default_path = self.settings[1].split(':')[-1]
        
        self.userinfo_credit_label.setText(self.credits)
    
    def app_doit(self, event):
        reply = QMessageBox.question(self, 'Message', 'Do it?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.doit()
        else:
            pass
        
    def load_file(self):
        fname = QFileDialog.getOpenFileNames(self, '', self.default_path,
                                             'JPEG(*.jpg *.jpeg *.jpe *.jfif);; PNG(*.png)')
        self.file_list.setRowCount(len(fname[0]))
 
        for i in range(len(fname[0])):
            img, fpath, fsize = bg_helpers.get_fsize(fname, i)
            self.file_list.setItem(i, 0, QTableWidgetItem(img))
            self.file_list.setItem(i, 1, QTableWidgetItem(fpath))
            self.file_list.setItem(i, 2, QTableWidgetItem(fsize))
        self.file_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def filelist_dclicked(self):
        row = self.file_list.currentIndex().row()
        if self.file_list.item(row, 1) != None:
            self.clicked_path = self.file_list.item(row, 1).text()
            self.target_path = self.file_list.item(row, 1).text()
            self.userinfo_select_label.setText(self.clicked_path)
        else:
            self.clicked_path = '?'
            print("load file first")
        
    def prev_org_image(self):
        preview = QPixmap(self.clicked_path)
        width = preview.width()
        height = preview.height()
        
        self.img_org_label.clear()
        if self.clicked_path != '?':
            if width > height:
                self.img_org_label.setPixmap(preview.scaled(500, int(500*(height/width))+50,
                                                            Qt.KeepAspectRatio))
                self.img_org_label.setAlignment(Qt.AlignCenter)
            elif width == height:
                self.img_org_label.setPixmap(preview.scaled(500, 500+50,
                                                            Qt.KeepAspectRatio))
                self.img_org_label.setAlignment(Qt.AlignCenter)
            else:
                self.img_org_label.setPixmap(preview.scaled(int(500*(width/height)), 500+50,
                                                            Qt.KeepAspectRatio))
                self.img_org_label.setAlignment(Qt.AlignCenter)
        else:
            print("load file first")
    
    def doit(self):
        print('doit!!!')
        img_name, img_resolution, img_file_obj = bg_helpers.load_img(self.target_path, 'BG')
        print("[WAIT] Wait the result, plz.")
        
        r = requests.post(self.BG_URL,
                  files = {
                      'image_file': (self.target_path, img_file_obj, 'image/jpg'),
                      },
                  data = { 
                          'prompt': self.INPUT_PROMPT 
                          },
                  headers = { 
                             'x-api-key': self.MY_API
                             }
                  )
        if (r.ok):
            result = Image.open(io.BytesIO(r.content))
            now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            bg_result_file = f"{img_name}_bgedit_{now}.jpg"
            result.save(self.BGRESULT_DIR + bg_result_file)
            
            rimg = QPixmap(self.BGRESULT_DIR+bg_result_file)
            width = rimg.width()
            height = rimg.height()
            
            self.img_result_label.clear()            
            if width > height:
                self.img_result_label.setPixmap(rimg.scaled(500, int(500*(height/width))+50,
                                                            Qt.KeepAspectRatio))
                self.img_result_label.setAlignment(Qt.AlignCenter)
            elif width == height:
                self.img_result_label.setPixmap(rimg.scaled(500, 500+50,
                                                            Qt.KeepAspectRatio))
                self.img_result_label.setAlignment(Qt.AlignCenter)
            else:
                self.img_result_label.setPixmap(rimg.scaled(int(500*(width/height)), 500+50,
                                                            Qt.KeepAspectRatio))
                self.img_result_label.setAlignment(Qt.AlignCenter)
            print(f"[RESULT] {bg_result_file} is saved.")
            
            self.credits = str(r.headers['x-remaining-credits'])
            f = open(self.spath, 'w')
            f.write('credits:'+self.credits+'\n')
            f.write(f'default_path:{self.default_path}')
            f.close()
            
            self.userinfo_credit_label.setText(f"{r.headers['x-remaining-credits']}")
            print(f"[CHECK] {float(r.headers['x-remaining-credits'])} credits are remained")
            
            if float(r.headers['x-remaining-credits']) < 5:        
                print("[WARNING] The credit has almost been used up.")
        else:    
            print(r)
            r.raise_for_status()
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())