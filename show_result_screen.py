#### 파일 넣어서 출력한 후에 .001파일 넣어서 엔트리 확인은 안됨 -> errors='ignore' 넣어서 문제 없이 돌아감
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QHeaderView, QAbstractItemView, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import subprocess
import sys

class show_result_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("완전 삭제")
        self.signature_mod_button = QPushButton("데이터 변조")

        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.placeholder = QWidget()
        self.placeholder.setStyleSheet("background-color: white;")

        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Find : ")
        self.search_bar = QLineEdit()
        self.search_options = QComboBox()
        self.search_button = QPushButton("Search")
        self.clear_search_button = QPushButton("X")
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_options)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.clear_search_button)

        self.wiping_table = self.create_table(2, ['와이핑된 파일', '와이핑 흔적 발견'])
        self.single_delete_table = self.create_table(3, ['파일 명', '삭제 유형', '시간'])
        self.signature_mod_table = self.create_table(4, ['파일 명', '변조 가능성', '복구 경로', '시간'])

        self.main_layout.addWidget(self.wiping_table)
        self.main_layout.addWidget(self.single_delete_table)
        self.main_layout.addWidget(self.signature_mod_table)
        self.main_layout.addWidget(self.placeholder)
        self.main_layout.addLayout(self.search_layout)

        self.setLayout(self.main_layout)  # Set layout for this widget

        self.wiping_button.clicked.connect(self.display_wiping_records)
        self.single_delete_button.clicked.connect(self.display_single_delete_records)
        self.signature_mod_button.clicked.connect(self.display_signature_mod_records)
        self.search_button.clicked.connect(self.search_records)
        self.clear_search_button.clicked.connect(self.clear_search)

        self.show_placeholder()  # Show the placeholder initially

        self.search_bar.setAlignment(Qt.AlignCenter)  # Center text input

        # 테이블의 가로 스크롤바를 필요할 때만 표시하도록 설정
        self.wiping_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.single_delete_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.signature_mod_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 세로 스크롤바 설정
        self.wiping_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.single_delete_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.signature_mod_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 단순 삭제 테이블의 열을 자동으로 채우도록 설정
        self.single_delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 데이터 변조 테이블의 열을 내용에 맞게 조정
        self.signature_mod_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.wiping_results = None  # Store wiping results

    def create_table(self, columns, headers):
        table = QTableWidget()
        table.setRowCount(0)
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {border-bottom: 1px solid black; text-align: center;}")
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        self.search_options.clear()
        self.search_options.addItems(["공통", "파일", "흔적"])
        self.center_align_combobox_text(self.search_options)
        if self.wiping_results is None:
            self.load_wiping_results()
        self.display_table(self.wiping_table)

    def display_single_delete_records(self):
        self.search_options.clear()
        self.search_options.addItems(["공통", "파일명", "삭제유형", "시간"])
        self.center_align_combobox_text(self.search_options)
        self.display_table(self.single_delete_table)

    def display_signature_mod_records(self):
        self.search_options.clear()
        self.search_options.addItems(["공통", "파일명", "변조가능성", "복구경로", "시간"])
        self.center_align_combobox_text(self.search_options)
        self.display_table(self.signature_mod_table)

    def display_table(self, table):
        self.hide_all_tables()
        table.show()
        self.adjust_table_columns(table)

    def hide_all_tables(self):
        self.wiping_table.hide()
        self.single_delete_table.hide()
        self.signature_mod_table.hide()
        self.placeholder.hide()

    def show_placeholder(self):
        self.hide_all_tables()
        self.placeholder.show()

    def add_wiping_record(self, file_name, wiping_trace):
        self.add_table_row(self.wiping_table, [file_name, wiping_trace])

    def add_single_delete_record(self, file_name, delete_type, timestamp):
        self.add_table_row(self.single_delete_table, [file_name, delete_type, timestamp])

    def add_signature_mod_record(self, file_name, falsify_type, recovery_path, formatted_timestamp):
        self.add_table_row(self.signature_mod_table, [file_name, falsify_type, recovery_path, formatted_timestamp])

    def add_table_row(self, table, data):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, i, item)
        self.adjust_table_columns(table)

    def clear_tables(self):
        self.wiping_table.setRowCount(0)
        self.single_delete_table.setRowCount(0)
        self.signature_mod_table.setRowCount(0)

    def analyze_file(self, file_path):
        self.clear_tables()

        deletion_records = self.get_deletion_records(file_path)
        for record in deletion_records:
            if record.strip():
                try:
                    file_name, delete_type, timestamp = map(str.strip, record.split(","))
                    self.add_single_delete_record(file_name, delete_type, timestamp)
                except ValueError:
                    print(f"Skipping invalid record: {record}")

        wiping_records = self.get_wiping_records(file_path)
        for record in wiping_records:
            if record.strip():
                try:
                    file_name, wiping_trace = map(str.strip, record.split(","))
                    self.add_wiping_record(file_name, wiping_trace)
                except ValueError:
                    print(f"Skipping invalid record: {record}")

        signature_mod_records = self.get_signature_mod_records(file_path)
        for record in signature_mod_records:
            if record.strip():
                fields = record.split(",")
                if len(fields) >= 4:
                    file_name = fields[0].strip()
                    falsify_type = ",".join(fields[1:-2]).strip()
                    recovery_path = fields[-2].strip()
                    formatted_timestamp = fields[-1].strip()
                    self.add_signature_mod_record(file_name, falsify_type, recovery_path, formatted_timestamp)
                else:
                    print(f"Skipping invalid record: {record}")

    def load_records(self):
        self.clear_tables()

        deletion_records = self.get_deletion_records("default_file_path")
        for record in deletion_records:
            if record.strip():
                try:
                    file_name, delete_type, timestamp = map(str.strip, record.split(","))
                    self.add_single_delete_record(file_name, delete_type, timestamp)
                except ValueError:
                    print(f"Skipping invalid record: {record}")

        wiping_records = self.get_wiping_records("default_file_path")
        for record in wiping_records:
            if record.strip():
                try:
                    file_name, wiping_trace = map(str.strip, record.split(","))
                    self.add_wiping_record(file_name, wiping_trace)
                except ValueError:
                    print(f"Skipping invalid record: {record}")

        signature_mod_records = self.get_signature_mod_records("default_file_path")
        for record in signature_mod_records:
            if record.strip():
                fields = record.split(",")
                if len(fields) >= 4:
                    file_name = fields[0].strip()
                    falsify_type = ",".join(fields[1:-2]).strip()
                    recovery_path = fields[-2].strip()
                    formatted_timestamp = fields[-1].strip()
                    self.add_signature_mod_record(file_name, falsify_type, recovery_path, formatted_timestamp)
                else:
                    print(f"Skipping invalid record: {record}")

    def get_deletion_records(self, file_path):
        result = subprocess.run([sys.executable, "simple_delete_detection.py", file_path], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stdout.splitlines()

    def get_wiping_records(self, _):
        result = subprocess.run([sys.executable, "print_wiping.py"], capture_output=True, text=True, encoding='cp949', errors='ignore')
        self.wiping_results = result.stdout.splitlines()
        return self.wiping_results

    def get_signature_mod_records(self, file_path):
        result = subprocess.run([sys.executable, "detect_data_falsify.py", file_path], capture_output=True, text=True, encoding='cp949', errors='ignore')
        return result.stdout.splitlines()

    def load_wiping_results(self):
        self.clear_tables()
        wiping_records = self.get_wiping_records("default_file_path")
        for record in wiping_records:
            if record.strip():
                try:
                    file_name, wiping_trace = map(str.strip, record.split(","))
                    self.add_wiping_record(file_name, wiping_trace)
                except ValueError:
                    print(f"Skipping invalid record: {record}")

    def search_records(self):
        search_term = self.search_bar.text()
        search_option = self.search_options.currentText()
        if self.wiping_table.isVisible():
            self.filter_table(self.wiping_table, search_term, search_option)
        elif self.single_delete_table.isVisible():
            self.filter_table(self.single_delete_table, search_term, search_option)
        elif self.signature_mod_table.isVisible():
            self.filter_table(self.signature_mod_table, search_term, search_option)

    def filter_table(self, table, search_term, search_option):
        for row in range(table.rowCount()):
            match = False
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if search_option == "공통" or \
                   (search_option == "파일" and column == 1 and self.wiping_table.isVisible()) or \
                   (search_option == "흔적" and column == 0 and self.wiping_table.isVisible()) or \
                   (search_option == "파일명" and column == 0) or \
                   (search_option == "삭제유형" and column == 1 and self.single_delete_table.isVisible()) or \
                   (search_option == "시간" and column == table.columnCount() - 1) or \
                   (search_option == "변조가능성" and column == 1 and self.signature_mod_table.isVisible()) or \
                   (search_option == "복구경로" and column == 2 and self.signature_mod_table.isVisible()):
                    if search_term.lower() in item.text().lower():
                        match = True
                        break
            table.setRowHidden(row, not match)

    def clear_search(self):
        self.search_bar.clear()
        if self.wiping_table.isVisible():
            self.reset_table_filter(self.wiping_table)
        elif self.single_delete_table.isVisible():
            self.reset_table_filter(self.single_delete_table)
        elif self.signature_mod_table.isVisible():
            self.reset_table_filter(self.signature_mod_table)

    def reset_table_filter(self, table):
        for row in range(table.rowCount()):
            for column in range(table.columnCount()):
                item = table.item(row, column)
                item.setBackground(QColor("white"))  
            table.setRowHidden(row, False)

    def adjust_table_columns(self, table):
        table.resizeColumnsToContents()
        header = table.horizontalHeader()
        if table == self.signature_mod_table:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            for column in range(table.columnCount()):
                if table.columnWidth(column) > 300:
                    header.setSectionResizeMode(column, QHeaderView.Interactive)
                    table.setColumnWidth(column, 300)
                else:
                    header.setSectionResizeMode(column, QHeaderView.Stretch)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)

    def center_align_combobox_text(self, combobox):
        for i in range(combobox.count()):
            combobox.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = show_result_screen()
    main_window.resize(800, 600)
    main_window.show()
    sys.exit(app.exec_())

