from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
import sys
import subprocess

class show_result_screen(QWidget):
    def __init__(self):
        super().__init__()

        # 버튼 레이아웃 생성
        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("단순삭제")
        self.signature_mod_button = QPushButton("데이터 변조")

        # 버튼 레이아웃에 버튼 추가
        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        # 메인 레이아웃 생성 및 버튼 레이아웃 추가
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # 플레이스홀더 생성
        self.placeholder = QWidget()
        self.placeholder.setStyleSheet("background-color: white;")

        # 테이블 생성
        self.wiping_table = self.create_table(2, ['경로에 파일 존재 여부', '경로'])
        self.single_delete_table = self.create_table(3, ['파일 명', '삭제 유형', '시간'])
        self.signature_mod_table = self.create_table(3, ['파일 명', '변조 가능성', '복구 경로'])

        # 메인 레이아웃에 플레이스홀더 및 테이블 추가
        self.main_layout.addWidget(self.placeholder)
        self.main_layout.addWidget(self.wiping_table)
        self.main_layout.addWidget(self.single_delete_table)
        self.main_layout.addWidget(self.signature_mod_table)

        self.setLayout(self.main_layout)  # 위젯에 레이아웃 설정

        # 버튼 클릭 시 해당 테이블 표시
        self.wiping_button.clicked.connect(self.display_wiping_records)
        self.single_delete_button.clicked.connect(self.display_single_delete_records)
        self.signature_mod_button.clicked.connect(self.display_signature_mod_records)

        self.show_placeholder()  # 초기에는 플레이스홀더를 표시

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
                color: black;  /* 선택된 셀의 글자색을 변경하지 않도록 설정 */
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
        
# 와이핑 기록 및 테이블 행 추가
    def add_wiping_record(self, file_exists, path):  
        self.add_table_row(self.wiping_table, [file_exists, path])  
# 단순 삭제 기록 및 테이블 행 추가
    def add_single_delete_record(self, file_name, delete_type, timestamp):
        self.add_table_row(self.single_delete_table, [file_name, delete_type, timestamp])  
# 데이터 변조 기록 및 테이블 행 추가
    def add_signature_mod_record(self, file_name, mod_possibility, path):  
        self.add_table_row(self.signature_mod_table, [file_name, mod_possibility, path])  

    def add_table_row(self, table, data):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, i, item)
            
# 단순 삭제 기록 가져오는 부분
def get_deletion_records():
    result = subprocess.run([sys.executable, "print_data_del.py"], capture_output=True, text=True)
    return result.stdout.splitlines()
# 와이핑 기록 가져오는 부분
def get_wiping_records():  
    result = subprocess.run([sys.executable, "print_wiping.py"], capture_output=True, text=True)
    return result.stdout.splitlines()
# 데이터 변조 기록 가져오는 부분
def get_signature_mod_records():  
    result = subprocess.run([sys.executable, "detecting_data_falsification.py"], capture_output=True, text=True)
    return result.stdout.splitlines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = show_result_screen()
    main_window.show()

    # 첫 번째 스크립트에서 삭제 기록 가져오기
    deletion_records = get_deletion_records()

    # 단순 삭제 기록을 처리하고 GUI에 추가
    for record in deletion_records:
        if record.strip():  # 빈 줄 건너뛰기
            file_name, delete_type, timestamp = map(str.strip, record.split(","))
            main_window.add_single_delete_record(file_name, delete_type, timestamp)

    
    # 스크립트에서 와이핑 기록 가져오기
    wiping_records = get_wiping_records()

    # 와이핑 기록을 처리하고 GUI에 추가
    for record in wiping_records:
        if record.strip():  # 빈 줄 건너뛰기
            file_exists, path = map(str.strip, record.split(","))
            main_window.add_wiping_record(file_exists, path)

    
    # 스크립트에서 데이터 변조 기록 가져오기
    signature_mod_records = get_signature_mod_records()

    # 데이터 변조 기록 처리 및 GUI에 추가
    for record in signature_mod_records:
        if record.strip():  # 빈 줄 건너뛰기
            file_name, mod_possibility, path = map(str.strip, record.split(","))
            main_window.add_signature_mod_record(file_name, mod_possibility, path)

    sys.exit(app.exec_())
