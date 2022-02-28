import sys
import cv2
import numpy as np
from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2.QtCore import Qt


class AppWidget(qtw.QWidget):
    def __init__(self):
        super(AppWidget, self).__init__()
        layout = qtw.QVBoxLayout()
        self.label = qtw.QLabel('hello')
        btn = qtw.QPushButton("hi")
        btn.clicked.connect(self._snapshot)
        btn.setStyleSheet("background-color: red;"
                "border-style: inset;"
                "border-width: 2px;"
                "border-radius: 10px;"
                "border-color: beige;"
                "font: bold 14px;"
                "min-width: 10em;"
                "padding: 6px;")
        layout.addWidget(self.label)
        layout.addWidget(btn)
        self.setLayout(layout)
        # self.cap = cv2.VideoCapture(0)
        self.np_img = np.zeros((480, 640, 3), dtype=np.uint8)
        # self.cap.read(self.np_img)
        self.qimg = qtg.QImage(self.np_img.data, 640, 480, 3 * 640, qtg.QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(qtg.QPixmap(self.qimg))
        
    def _snapshot(self):
        # self.cap.read(self.np_img)
        self.qimg = qtg.QImage(self.np_img.data, 640, 480, 3 * 640, qtg.QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(qtg.QPixmap(self.qimg))
        


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.app_widget = AppWidget()
        # label = qtw.QLabel('hello')
        self.setCentralWidget(self.app_widget)
        self.show()


app = qtw.QApplication(sys.argv)
w = MainWindow()
app.exec_()