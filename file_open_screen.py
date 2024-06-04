from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QAction, 
    QMessageBox, QTextEdit, QPushButton, QVBoxLayout, 
    QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class file_open_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.left_layout = QVBoxLayout()
        self.file_open_area = QTextEdit("")
        self.file_open_area.setReadOnly(True)
        self.left_layout.addWidget(self.file_open_area)

        self.setLayout(self.left_layout)  # Set layout for this widget

