import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QLabel, QCheckBox, QComboBox, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QLabel("Hello")
        btn = QPushButton("hi")
        btn.clicked.connect(lambda x: print(x))
        font = widget.font()
        font.setPointSize(40)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(btn)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()