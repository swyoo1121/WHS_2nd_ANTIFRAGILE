from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import Qt
import subprocess
import sys

class show_result_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("단순삭제")
        self.signature_mod_button = QPushButton("데이터 변조")

        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.placeholder = QWidget()
        self.placeholder.setStyleSheet("background-color: white;")

        self.wiping_table = self.create_table(2, ['경로에 파일 존재 여부', '경로'])
        self.single_delete_table = self.create_table(3, ['파일 명', '삭제 유형', '시간'])
        self.signature_mod_table = self.create_table(3, ['파일 명', '변조 가능성', '복구 경로'])

        self.main_layout.addWidget(self.placeholder)
        self.main_layout.addWidget(self.wiping_table)
        self.main_layout.addWidget(self.single_delete_table)
        self.main_layout.addWidget(self.signature_mod_table)

        self.setLayout(self.main_layout)  

        self.wiping_button.clicked.connect(self.display_wiping_records)
        self.single_delete_button.clicked.connect(self.display_single_delete_records)
        self.signature_mod_button.clicked.connect(self.display_signature_mod_records)

        self.show_placeholder()  # Show the placeholder initially

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
            QTableWidget::item:selected {
                color: black;  
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
        table.show()

    def hide_all_tables(self):
        self.wiping_table.hide()
        self.single_delete_table.hide()
        self.signature_mod_table.hide()
        self.placeholder.hide()

    def show_placeholder(self):
        self.hide_all_tables()
        self.placeholder.show()

    def add_wiping_record(self, file_exists, path):
        self.add_table_row(self.wiping_table, [file_exists, path])

    def add_single_delete_record(self, file_name, delete_type, timestamp):
        self.add_table_row(self.single_delete_table, [file_name, delete_type, timestamp])

    def add_signature_mod_record(self, file_name, mod_possibility, path):
        self.add_table_row(self.signature_mod_table, [file_name, mod_possibility, path])

    def add_table_row(self, table, data):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, i, item)

    def clear_tables(self):
        self.wiping_table.setRowCount(0)
        self.single_delete_table.setRowCount(0)
        self.signature_mod_table.setRowCount(0)

    def analyze_file(self, file_path):
        # 기존 테이블 데이터 초기화
        self.clear_tables()

        # 단순순 삭제 기록 불러오기
        deletion_records = self.get_deletion_records(file_path)
        for record in deletion_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, delete_type, timestamp = map(str.strip, record.split(","))
                self.add_single_delete_record(file_name, delete_type, timestamp)

        # 와이핑 기록 불러오기
        wiping_records = self.get_wiping_records(file_path)
        for record in wiping_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_exists, path = map(str.strip, record.split(","))
                self.add_wiping_record(file_exists, path)

        # 데이터 변조 기록 불러오기
        signature_mod_records = self.get_signature_mod_records(file_path)
        for record in signature_mod_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, mod_possibility, path = map(str.strip, record.split(","))
                self.add_signature_mod_record(file_name, mod_possibility, path)

    def load_records(self):
        # 기존 테이블 데이터 초기화
        self.clear_tables()

        # 단순 삭제 기록 불러오기
        deletion_records = self.get_deletion_records("default_file_path")  
        for record in deletion_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, delete_type, timestamp = map(str.strip, record.split(","))
                self.add_single_delete_record(file_name, delete_type, timestamp)

        # 와이핑 삭제 기록 불러오기
        wiping_records = self.get_wiping_records("default_file_path")
        for record in wiping_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_exists, path = map(str.strip, record.split(","))
                self.add_wiping_record(file_exists, path)

        # 데이터 변조 기록 불러오기
        signature_mod_records = self.get_signature_mod_records("default_file_path")
        for record in signature_mod_records:
            if record.strip():  # 빈 줄 건너뛰기
                file_name, mod_possibility, path = map(str.strip, record.split(","))
                self.add_signature_mod_record(file_name, mod_possibility, path)

    # 외부 스크립트를 실행하여 기록을 가져오는 함수
    def get_deletion_records(self, file_path):
        result = subprocess.run([sys.executable, "simple_delete_detection.py", file_path], capture_output=True, text=True)
        return result.stdout.splitlines()

    def get_wiping_records(self, file_path):
        result = subprocess.run([sys.executable, "print_wiping.py", file_path], capture_output=True, text=True)
        return result.stdout.splitlines()

    def get_signature_mod_records(self, file_path):
        result = subprocess.run([sys.executable, "detecting_data_falsification.py", file_path], capture_output=True, text=True)
        return result.stdout.splitlines()
