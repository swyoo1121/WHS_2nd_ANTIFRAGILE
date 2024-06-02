### library, global variables start

import sys, os
import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

dir = os.path.dirname(os.getcwd())

### library, global variables end

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

    def confirm_exit(self): # Event when click the File-Exit button.
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def closeEvent(self, event): # Ignoring refer to code convention
        self.confirm_exit()
        event.ignore()
            
    def new_file(self):
        print("hello")

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = MyWindow()
    ex.show()

    sys.exit(app.exec_())
