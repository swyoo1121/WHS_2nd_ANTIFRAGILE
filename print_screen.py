import sys
from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QMainWindow, QAction, 
    QMessageBox, QTextEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QMenu, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antifragile")
        self.setWindowIcon(QIcon("images/main_icon.png"))
        self.setGeometry(100, 100, 2000, 1200)
        self.initUI()

    def initUI(self):
        self.statusBar()
        menubar = self.menuBar()
                
        fileMenu = menubar.addMenu('&File')
        
        exit_action = QAction(QIcon("images/exit_icon.png"), '&Exit', self)
        exit_action.setShortcut('Ctrl+e')
        exit_action.triggered.connect(QApplication.quit)
        
        open = QMenu('&Open', self)
        openSub1 = QAction(QIcon("images/newfile_icon.png"), '&New', self)
        openSub1.setShortcut('Ctrl+N')
        openSub1.triggered.connect(self.newFile)
        openSub2 = QAction('&Recent', self) 
        open.addAction(openSub1)
        open.addAction(openSub2)
        
        fileMenu.addMenu(open)
        fileMenu.addAction(exit_action)
        
        editMenu = menubar.addMenu('&Edit')
        
        analyze = QAction(QIcon("images/analyze_icon.png"), '&Analyze', self)
        editMenu.addAction(analyze)
        
        viewMenu = menubar.addMenu('&View')
        
        toolMenu = menubar.addMenu('&Tools')
        
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction('&About us')
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 왼쪽 영역에 텍스트 편집기 배치
        self.left_layout = QVBoxLayout()
        self.file_open_area = QTextEdit("")
        self.file_open_area.setReadOnly(True)
        self.left_layout.addWidget(self.file_open_area)
        
        # 오른쪽 위 영역에 버튼 레이아웃 설정
        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("단순삭제")
        self.signature_mod_button = QPushButton("시그니처 변조")

        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        # 오른쪽 위 영역에 버튼 레이아웃 추가
        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.button_layout)

        # 오른쪽 영역에 표 초기화
        self.table_layout = QVBoxLayout()
        self.wiping_table = QTableWidget()
        self.wiping_table.setRowCount(0)
        self.wiping_table.setColumnCount(2)
        self.wiping_table.setHorizontalHeaderLabels(['경로에 파일 존재 여부','경로'])
        self.wiping_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.wiping_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.wiping_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border-bottom: 1px solid black; text-align: center;}")
        self.wiping_table.verticalHeader().setVisible(False)
        self.wiping_table.setStyleSheet("""
            QTableWidget::item { 
                border-bottom: 1px solid lightgrey; 
                text-align: center;
            }
            QTableWidget { 
                gridline-color: lightgrey;
            }
        """)

        self.single_delete_table = QTableWidget()
        self.single_delete_table.setRowCount(0)
        self.single_delete_table.setColumnCount(3)
        self.single_delete_table.setHorizontalHeaderLabels(['파일 명', '삭제 유형','경로'])
        self.single_delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.single_delete_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.single_delete_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border-bottom: 1px solid black; text-align: center;}")
        self.single_delete_table.verticalHeader().setVisible(False)
        self.single_delete_table.setStyleSheet("""
            QTableWidget::item { 
                border-bottom: 1px solid lightgrey; 
                text-align: center;
            }
            QTableWidget { 
                gridline-color: lightgrey;
            }
        """)

        self.signature_mod_table = QTableWidget()
        self.signature_mod_table.setRowCount(0)
        self.signature_mod_table.setColumnCount(3)
        self.signature_mod_table.setHorizontalHeaderLabels(['변조 파일 명', '변조 가능성','경로'])
        self.signature_mod_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.signature_mod_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.signature_mod_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border-bottom: 1px solid black; text-align: center;}")
        self.signature_mod_table.verticalHeader().setVisible(False)
        self.signature_mod_table.setStyleSheet("""
            QTableWidget::item { 
                border-bottom: 1px solid lightgrey; 
                text-align: center;
            }
            QTableWidget { 
                gridline-color: lightgrey;
            }
        """)

        # 표를 오른쪽 레이아웃에 추가하지 않음, 버튼 아래에 동적으로 추가 예정
        self.right_layout.addLayout(self.table_layout)

        # 버튼 클릭 이벤트 연결
        self.wiping_button.clicked.connect(self.display_wiping_records)
        self.single_delete_button.clicked.connect(self.display_single_delete_records)
        self.signature_mod_button.clicked.connect(self.display_signature_mod_records)

        # 메인 레이아웃 설정
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 2)

        self.central_widget.setLayout(self.main_layout)

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
            
    def newFile(self):
        print("New file action triggered")
        
    def display_wiping_records(self):
        # 와이핑 표만 보이도록
        self.hide_all_tables()
        self.table_layout.addWidget(self.wiping_table)
        self.wiping_table.show()

    def display_single_delete_records(self):
        # 단순삭제 표만 보이도록
        self.hide_all_tables()
        self.table_layout.addWidget(self.single_delete_table)
        self.single_delete_table.show()
        
    def display_signature_mod_records(self):
        # 시그니처 변조 표만 보이도록
        self.hide_all_tables()
        self.table_layout.addWidget(self.signature_mod_table)
        self.signature_mod_table.show()

    def hide_all_tables(self):
        # 모든 표 숨기기
        self.wiping_table.hide()
        self.single_delete_table.hide()
        self.signature_mod_table.hide()

    def center_align_headers(self, table):
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.horizontalHeader().setStyleSheet("QHeaderView::section { border-bottom: 1px solid black; text-align: center; }")
        
    def add_wiping_record(self, path):
        row_position = self.wiping_table.rowCount()
        self.wiping_table.insertRow(row_position)
        item = QTableWidgetItem(path)
        item.setTextAlignment(Qt.AlignCenter)
        self.wiping_table.setItem(row_position, 0, item)

    def add_single_delete_record(self, file_name, delete_type):
        row_position = self.single_delete_table.rowCount()
        self.single_delete_table.insertRow(row_position)
        item_file_name = QTableWidgetItem(file_name)
        item_file_name.setTextAlignment(Qt.AlignCenter)
        item_delete_type = QTableWidgetItem(delete_type)
        item_delete_type.setTextAlignment(Qt.AlignCenter)
        self.single_delete_table.setItem(row_position, 0, item_file_name)
        self.single_delete_table.setItem(row_position, 1, item_delete_type)

    def add_signature_mod_record(self, file_name, description):
        row_position = self.signature_mod_table.rowCount()
        self.signature_mod_table.insertRow(row_position)
        item_file_name = QTableWidgetItem(file_name)
        item_file_name.setTextAlignment(Qt.AlignCenter)
        item_description = QTableWidgetItem(description)
        item_description.setTextAlignment(Qt.AlignCenter)
        self.signature_mod_table.setItem(row_position, 0, item_file_name)
        self.signature_mod_table.setItem(row_position, 1, item_description)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    
    sys.exit(app.exec_())
