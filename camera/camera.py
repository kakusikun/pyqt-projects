import sys
import os
import cv2
os.chdir(os.path.dirname(__file__))
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import QElapsedTimer, QTimer, Qt, QEvent


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('misc/thermal_mapping.ui', self)
        self.camera_scroll.setWidget(self.camera_label)
        img = cv2.imread('misc/14.jpg')
        h, w, _ = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QImage(img.data, w, h, 3 * w, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qimg))
        self.camera_label.installEventFilter(self)
        self.camera_label.setScaledContents(True)

        self._init_pos_widget()

        self.setWindowTitle('Camera')
        self.show()
        
    def _init_pos_widget(self):
        for hlayout in self.pos_vlayout.children():
            widgets = [hlayout.itemAt(i).widget() for i in range(hlayout.count())]
            for widget in widgets:
                if isinstance(widget, QtWidgets.QSpinBox):
                    widget.setMinimum(0)
                    if 'pos_x' in widget.objectName():
                        widget.setMaximum(1080)
                    else:
                        widget.setMaximum(1920)
        
    def eventFilter(self, source, event):
        if source == self.camera_label:
            if event.type() == QEvent.MouseButtonPress:
                for i, rbtn in enumerate(self.pos_radio_group.buttons()):
                    if rbtn.isChecked():
                        hlayout = self.pos_vlayout.itemAt(i)
                        widgets = [hlayout.itemAt(i).widget() for i in range(hlayout.count())]
                        for widget in widgets:
                            if isinstance(widget, QtWidgets.QSpinBox):
                                if 'pos_x' in widget.objectName():
                                    widget.setValue(event.x())
                                else:
                                    widget.setValue(event.y())
                        break
            return QtWidgets.QWidget.eventFilter(self, source, event)
        
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
