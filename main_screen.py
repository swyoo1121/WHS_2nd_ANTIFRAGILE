### library, global variables start
import sys
import os
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QSplitter, QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from file_open_screen import file_open_screen
from show_result_screen import show_result_screen

dir = os.path.dirname(os.getcwd())

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antifragile")
        self.setWindowIcon(QIcon("images/main_icon.png"))
        self.setGeometry(100, 100, 2000, 1200)
        self.initUI()
        self.screen_split()

    def initUI(self):
        self.statusBar()
        menubar = self.menuBar()

        # File Menu
        fileMenu = menubar.addMenu('&File')

        exitAction = QAction(QIcon("images/exit_icon.png"), '&Exit', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.triggered.connect(self.confirm_exit)

        openMenu = QMenu('&Open', self)
        newFileAction = QAction(QIcon("images/newfile_icon.png"), '&New', self)
        newFileAction.setShortcut('Ctrl+N')
        newFileAction.triggered.connect(self.new_file)
        recentFileAction = QAction('&Recent', self)
        openMenu.addAction(newFileAction)
        openMenu.addAction(recentFileAction)

        fileMenu.addMenu(openMenu)
        fileMenu.addAction(exitAction)

        # Tool Menu
        toolMenu = menubar.addMenu('&Tools')
        analyzeAction = QAction(QIcon("images/analyze_icon.png"), '&Analyze', self)
        toolMenu.addAction(analyzeAction)

        # Help Menu
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction('&About us')
        
    # 화면 분할 구현. 왼쪽(파일 열기 = file_open_screen.py) + 오른쪽(출력 화면 = show_result_screen.py)으로 구성.
    def screen_split(self):
        splitter = QSplitter(Qt.Horizontal)

        self.open_screen_widget = file_open_screen()
        self.result_screen_widget = show_result_screen()

        splitter.addWidget(self.open_screen_widget)
        splitter.addWidget(self.result_screen_widget)
        splitter.setSizes([1600, 4000])

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        container.setLayout(layout)

        self.setCentralWidget(container)

        # 버튼 신호를 해당 슬롯에 연결
        self.result_screen_widget.single_delete_button.clicked.connect(self.display_deletion_records)
        self.load_records()

    def confirm_exit(self):  # 파일-종료 버튼을 클릭했을 때의 이벤트.
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def closeEvent(self, event):  # closeEvent 재정의
        self.confirm_exit()
        event.ignore()

    def new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open evidence item", "", "All Files (*)")
        if file_path:
            self.open_screen_widget.load_file(file_path)
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        # 삭제 기록 불러오기
        deletion_records = get_deletion_records(file_path)
        for record in deletion_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, delete_type, timestamp = map(str.strip, record.split(","))
                self.result_screen_widget.add_single_delete_record(file_name, delete_type, timestamp)

    def display_deletion_records(self):
        self.result_screen_widget.display_single_delete_records()

    def load_records(self):
        # 단순 삭제 기록 불러오기
        deletion_records = get_deletion_records("default_file_path")  # 필요 시 실제 기본 경로로 교체
        for record in deletion_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, delete_type, timestamp = map(str.strip, record.split(","))
                self.result_screen_widget.add_single_delete_record(file_name, delete_type, timestamp)

        # 와이핑 삭제 기록 불러오기
        wiping_records = get_wiping_records()
        for record in wiping_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_exists, path = map(str.strip, record.split(","))
                self.result_screen_widget.add_wiping_record(file_exists, path)

        # 데이터 변조 기록 불러오기
        signature_mod_records = get_signature_mod_records()
        for record in signature_mod_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, mod_possibility, path = map(str.strip, record.split(","))
                self.result_screen_widget.add_signature_mod_record(file_name, mod_possibility, path)

# 외부 스크립트를 실행하여 기록을 가져오는 함수
def get_deletion_records(file_path):
    result = subprocess.run([sys.executable, "print_data_del.py", file_path], capture_output=True, text=True)
    return result.stdout.splitlines()

def get_wiping_records():
    result = subprocess.run([sys.executable, "print_wiping.py"], capture_output=True, text=True)
    return result.stdout.splitlines()

def get_signature_mod_records():
    result = subprocess.run([sys.executable, "print_data_fals.py"], capture_output=True, text=True)
    return result.stdout.splitlines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())

