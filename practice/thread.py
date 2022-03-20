import time
from typing import *

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc

def test():
    time.sleep(1.0)

class Counter(qtc.QThread):
    def __init__(self, btn: qtw.QPushButton):
        super().__init__()
        self.btn = btn
        self.count = 0
        
    def run(self):
        while True:
            # self.sleep(1.0)
            time.sleep(1.0)
            self.btn.setText(str(self.count))
            self.count += 1
        
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.btn = qtw.QPushButton('start')
        self.btn.setCheckable(True)
        self.counter = None
        self.btn.clicked.connect(self.start_count)
        self.setCentralWidget(self.btn)
        self.show()
        
    def start_count(self, checked):
        print(checked)
        if checked:
            self.counter = Counter(self.btn)
            self.counter.start()
        else:
            if self.counter is not None:
                self.counter.terminate()
        
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    w = MainWindow()
    app.exec_()