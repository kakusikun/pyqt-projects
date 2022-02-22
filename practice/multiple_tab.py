import sys
import os
os.chdir(os.path.dirname(__file__))
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QLabel, QTabWidget, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt

from setting_layout import Ui_setting_layout


class DeviceLayout(QWidget, Ui_setting_layout):
    def __init__(self):
        super(DeviceLayout, self).__init__()
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        btn = QPushButton("hi")
        self.layout = QHBoxLayout()
        # self.layout.addWidget(self.app_tab)
        self.layout.addWidget(btn)
        self.layout.addWidget(DeviceLayout())
        self.setLayout(self.layout)
        self.show()
        

# class MainWindow(QMainWindow):

#     def __init__(self):
#         super(MainWindow, self).__init__()

#         self.setWindowTitle("My App")
#         self.ui = UILayout()
#         self.setCentralWidget(self.ui)

app = QApplication(sys.argv)
w = MainWindow()
app.exec()