from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QAction, 
    QMessageBox, QTextEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class show_result_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.button_layout = QHBoxLayout()
        self.wiping_button = QPushButton("와이핑")
        self.single_delete_button = QPushButton("단순삭제")
        self.signature_mod_button = QPushButton("시그니처 변조")

        self.button_layout.addWidget(self.wiping_button)
        self.button_layout.addWidget(self.single_delete_button)
        self.button_layout.addWidget(self.signature_mod_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.placeholder = QWidget()
        self.placeholder.setStyleSheet("background-color: white;")

        self.wiping_table = self.create_table(2, ['경로에 파일 존재 여부', '경로'])
        self.single_delete_table = self.create_table(3, ['파일 명', '삭제 유형', '경로'])
        self.signature_mod_table = self.create_table(3, ['변조 파일 명', '변조 가능성', '경로'])

        self.main_layout.addWidget(self.placeholder)
        self.main_layout.addWidget(self.wiping_table)
        self.main_layout.addWidget(self.single_delete_table)
        self.main_layout.addWidget(self.signature_mod_table)

        self.setLayout(self.main_layout)  # Set layout for this widget

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
    import sys
    app = QApplication(sys.argv)
    main_window = show_result_screen()
    main_window.show()
    sys.exit(app.exec_())

