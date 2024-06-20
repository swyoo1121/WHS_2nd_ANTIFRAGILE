### library, global variables start

import sys
import os
import subprocess  # Add this line to import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from file_open_screen import file_open_screen
from show_result_screen import show_result_screen

dir = os.path.dirname(os.getcwd())

### library, global variables end

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
        
        # Filemenu                
        fileMenu = menubar.addMenu('&File')
        
        exit = QAction(QIcon("images/exit_icon.png"), '&Exit', self)
        exit.setShortcut('Ctrl+E')
        exit.triggered.connect(self.confirm_exit)
        
        open = QMenu('&Open', self)
        openSub1 = QAction(QIcon("images/newfile_icon.png"), '&New', self)
        openSub1.setShortcut('Ctrl+N')
        openSub1.triggered.connect(self.new_file)
        openSub2 = QAction('&Recent', self) 
        open.addAction(openSub1)
        open.addAction(openSub2)
        
        fileMenu.addMenu(open)
        fileMenu.addAction(exit)
        
        toolMenu = menubar.addMenu('&Tools')
         
        analyze = QAction(QIcon("images/analyze_icon.png"), '&Analyze', self)
        toolMenu.addAction(analyze)
        
        helpMenu = menubar.addMenu('&Help')
        
        helpMenu.addAction('&About us')
 
# 화면 분할 구현. 왼쪽(파일 열기 = file_open_screen.py) + 오른쪽(출력 화면 = show_result_screen.py)으로 구성.    
    def screen_split(self):
        splitter = QSplitter(Qt.Horizontal)
        
        open_screen_widget = file_open_screen()
        self.result_screen_widget = show_result_screen()

        splitter.addWidget(open_screen_widget)
        splitter.addWidget(self.result_screen_widget)
        splitter.setSizes([1600,4000])
        
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        container.setLayout(layout)
        
        self.setCentralWidget(container)

        # Connect the button click signal to the slot that displays the deletion records
        self.result_screen_widget.single_delete_button.clicked.connect(self.display_deletion_records)
        
        # Get the deletion records from the first script
        self.deletion_records = get_deletion_records()

        # Process and add the deletion records to the GUI
        for record in self.deletion_records:
            if record.strip():  # Skip empty lines
                file_name, delete_type, timestamp = map(str.strip, record.split(","))
                self.result_screen_widget.add_single_delete_record(file_name, delete_type, timestamp)
        
    def confirm_exit(self): # Event when click the File-Exit button.
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def closeEvent(self, event): # Ignoring refer to code convention
        self.confirm_exit()
        event.ignore()
            
    def new_file(self):
        print("hello")

    def display_deletion_records(self):
        self.result_screen_widget.display_single_delete_records()

def get_deletion_records():
    result = subprocess.run([sys.executable, "print_data_del.py"], capture_output=True, text=True)
    return result.stdout.splitlines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = MyWindow()
    ex.show()

    sys.exit(app.exec_())
