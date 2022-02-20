import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = QAction("test 1", self)
        self.action.setCheckable(True)
        self.action.setChecked(True)
        self.action.toggled.connect(self.on_action_triggered)
        
    def on_action_triggered(self, e):
        print(e)
        if e:
            self.showMaximized()
        else:
            self.showNormal()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(self.action)
        context.exec(e.globalPos())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()