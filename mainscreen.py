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

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100,100,2100,1400)
        
        layout = QVBoxLayout()

        self.setLayout(layout)
        self.setWindowTitle("Antifragile")
        self.setWindowIcon(QIcon("images/file-img.png"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = MyWindow()
    w.show()
    
    sys.exit(app.exec_())
