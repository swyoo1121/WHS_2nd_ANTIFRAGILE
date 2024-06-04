from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QAction, 
    QMessageBox, QTextEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class result_screen(QWidget):
    def __init__(self):
        super().__init__()
        
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
