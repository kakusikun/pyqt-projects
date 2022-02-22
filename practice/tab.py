import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QLabel, QTabWidget, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.label = QLabel("Hello")
        self.btn = QPushButton("hi")
        self.tab = QTabWidget()
        self.layout = QVBoxLayout()
        self.tab.addTab(self.label, 't1')
        self.tab.addTab(self.btn, 't2')
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)
        self.show()

app = QApplication(sys.argv)
w = MainWindow()
app.exec()