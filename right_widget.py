from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class RightWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("This is the right widget")
        layout.addWidget(label)

        self.setLayout(layout)
