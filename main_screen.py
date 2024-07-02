### library, global variables start
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QSplitter, QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from show_result_screen import show_result_screen
from file_open_screen import file_open_screen
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

        # 파일 메뉴 설정
        file_menu = menubar.addMenu('&File')

        open_menu = QMenu('&Open', self)
        new_file_action = QAction(QIcon("images/newfile_icon.png"), '&New', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.new_file)
        recent_file_action = QAction('&Recent', self)
        open_menu.addAction(new_file_action)
        open_menu.addAction(recent_file_action)

        exit_action = QAction(QIcon("images/exit_icon.png"), '&Exit', self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.triggered.connect(self.confirm_exit)

        file_menu.addMenu(open_menu)
        file_menu.addAction(exit_action)

        # 도구 메뉴 설정
        tool_menu = menubar.addMenu('&Tools')
        
        analyze_menu = QMenu('&Analyze', self)
        analyze_wiping_action = QAction('&Analyze Wiping', self)
        analyze_falsification_action = QAction('&Analyze Falsification', self)
        analyze_deletion_action = QAction('&Analyze Deletion', self)
        analyze_menu.addAction(analyze_wiping_action)
        analyze_menu.addAction(analyze_falsification_action)
        analyze_menu.addAction(analyze_deletion_action)
        search_action = QAction(QIcon("images/analyze_icon.png"), '&Search', self)
        
        tool_menu.addMenu(analyze_menu)
        tool_menu.addAction(search_action)

        # 도움말 메뉴 설정
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction('&About us')

    # 화면 분할 구현. 왼쪽(파일 열기) + 오른쪽(출력 화면 = show_result_screen)으로 구성.
    def screen_split(self):
        splitter = QSplitter(Qt.Horizontal)

        self.open_screen_widget = file_open_screen()  # 파일 열기 화면 위젯 
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

    def confirm_exit(self):  # 파일-종료 버튼을 클릭했을 때의 이벤트
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def closeEvent(self, event):  # closeEvent 재정의 (Code Convention)
        self.confirm_exit()
        event.ignore()

    def new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open evidence item", "", "All Files (*)")
        if file_path:
            self.open_screen_widget.load_file(file_path)  # 파일 열기 화면에서 파일 로드 
            self.result_screen_widget.analyze_file(file_path)

    def display_deletion_records(self):
        self.result_screen_widget.display_single_delete_records()

    def load_records(self):
        self.result_screen_widget.load_records()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
