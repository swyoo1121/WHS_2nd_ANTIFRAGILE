import sys
import os
import math
from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QMainWindow, QAction, 
    QMessageBox, QTextEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QMenu, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

dir = os.path.dirname(os.getcwd())

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
        
        exit = QAction(QIcon("images/exit_icon.png"), '&Exit', self)
        exit.setShortcut('Ctrl+e')
        exit.triggered.connect(QApplication.aboutToQuit)
        
        open = QMenu('&Open', self)
        openSub1 = QAction(QIcon("images/newfile_icon.png"), '&New', self)
        openSub1.setShortcut('Ctrl+N')
        openSub1.triggered.connect(QApplication.aboutQt)
        openSub2 = QAction('&Recent', self) 
        open.addAction(openSub1)
        open.addAction(openSub2)
        
        fileMenu.addMenu(open)
        fileMenu.addAction(exit)
        
        editMenu = menubar.addMenu('&Edit')
        
        analyze = QAction(QIcon("images/analyze_icon.png"), '&Analyze', self)
        editMenu.addAction(analyze)
        
        viewMenu = menubar.addMenu('&View')
        
        toolMenu = menubar.addMenu('&Tools')
        
        helpMenu = menubar.addMenu('&Help')
        
        helpMenu.addAction('&About us')
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.left_layout = QVBoxLayout()
        self.file_open_area = QTextEdit("")
        self.file_open_area.setReadOnly(True)
        self.left_layout.addWidget(self.file_open_area)
        
        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("단순삭제")
        self.signature_mod_button = QPushButton("시그니처 변조")

        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.button_layout)

        self.table_layout = QVBoxLayout()
        self.wiping_table = self.create_table(2, ['경로에 파일 존재 여부', '경로'])
        self.single_delete_table = self.create_table(3, ['파일 명', '삭제 유형', '경로'])
        self.signature_mod_table = self.create_table(3, ['변조 파일 명', '변조 가능성', '경로'])
        self.right_layout.addLayout(self.table_layout)

        self.wiping_button.clicked.connect(self.display_wiping_records)
        self.single_delete_button.clicked.connect(self.display_single_delete_records)
        self.signature_mod_button.clicked.connect(self.display_signature_mod_records)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 2)

        self.central_widget.setLayout(self.main_layout)

    def create_table(self, columns, headers):
        table = QTableWidget()
        table.setRowCount(0)
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border-bottom: 1px solid black; text-align: center;}")
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
            QTableWidget::item { 
                border-bottom: 1px solid lightgrey; 
                text-align: center;
            }
            QTableWidget { 
                gridline-color: lightgrey;
            }
        """)
        return table

    def close_event(self, q_close_event):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            q_close_event.accept()
        else:
            q_close_event.ignore()
            
    def new_file(self):
        print("hello")
        
    def display_wiping_records(self):
        self.display_table(self.wiping_table)

    def display_single_delete_records(self):
        self.display_table(self.single_delete_table)
        
    def display_signature_mod_records(self):
        self.display_table(self.signature_mod_table)

    def display_table(self, table):
        self.hide_all_tables()
        self.table_layout.addWidget(table)
        table.show()

    def hide_all_tables(self):
        self.wiping_table.hide()
        self.single_delete_table.hide()
        self.signature_mod_table.hide()

    def add_wiping_record(self, path):
        self.add_table_row(self.wiping_table, [path])

    def add_single_delete_record(self, file_name, delete_type):
        self.add_table_row(self.single_delete_table, [file_name, delete_type])

    def add_signature_mod_record(self, file_name, description):
        self.add_table_row(self.signature_mod_table, [file_name, description])

    def add_table_row(self, table, data):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, i, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
