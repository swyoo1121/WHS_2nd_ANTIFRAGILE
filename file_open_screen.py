from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class open_screen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("This is the left widget")
        layout.addWidget(label)

        self.setLayout(layout)
