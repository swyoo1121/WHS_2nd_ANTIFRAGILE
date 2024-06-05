import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from left_widget import LeftWidget
from right_widget import RightWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Split Window Example")
        self.setGeometry(100, 100, 800, 600)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = LeftWidget()
        right_widget = RightWidget()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 400])

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        container.setLayout(layout)

        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
