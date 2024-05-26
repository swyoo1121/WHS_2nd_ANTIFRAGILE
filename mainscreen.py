"""
from tkinter import *

# 1. 루트화면 (root window) 생성
tk = Tk() 
# 2. 텍스트 표시
label = Label(tk,text='Hello World!') 
# 3. 레이블 배치 실행
label.pack()
# 4. 메인루프 실행
tk.mainloop()
"""

import sys, os
import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

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
        
    def closeEvent(self, QCloseEvent):
        re = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes|QMessageBox.No)
        
        if re == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
            
    def newFile(self):
        print("hello")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = MyWindow()
    ex.show()

    sys.exit(app.exec_())
