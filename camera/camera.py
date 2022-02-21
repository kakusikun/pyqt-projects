import sys
import os
import cv2
os.chdir(os.path.dirname(__file__))
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter, QPen
from PyQt5.QtCore import QElapsedTimer, QTimer, Qt, QEvent


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('misc/thermal_mapping.ui', self)
        self.camera_scroll.setWidget(self.camera_label)
        img = cv2.imread('misc/14.jpg')
        h, w, _ = img.shape
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QImage(self.img.data, w, h, 3 * w, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qimg))
        self.camera_label.installEventFilter(self)
        self.camera_label.setScaledContents(True)
        self.zoom_label.setScaledContents(True)

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
    
    def get_checked_pos_widgets(self):
        for i, rbtn in enumerate(self.pos_radio_group.buttons()):
            if rbtn.isChecked():
                hlayout = self.pos_vlayout.itemAt(i)
                widgets = [hlayout.itemAt(j).widget() for j in range(hlayout.count())]
                return widgets
        return []
    
    def eventFilter(self, source, event):
        if source == self.camera_label:
            if event.type() == QEvent.MouseButtonPress:
                widgets = self.get_checked_pos_widgets()
                if len(widgets) > 0:
                    for widget in widgets:
                        if isinstance(widget, QtWidgets.QSpinBox):
                            if 'pos_x' in widget.objectName():
                                widget.setValue(event.x())
                            else:
                                widget.setValue(event.y())
                    self.zoom(event.x(), event.y())
            return QtWidgets.QWidget.eventFilter(self, source, event)
        
    def zoom(self, pos_x, pos_y):
        if pos_x >= 0 and pos_y >= 0:
            ratio = self.zoom_ratio_spin.value()
            h, w, _ = self.img.shape
            a_x = max(0, pos_x - int(20 / ratio))
            b_x = min(w, pos_x + int(20 / ratio))
            a_y = max(0, pos_y - int(20 / ratio))
            b_y = min(h, pos_y + int(20 / ratio))
            zoom_img = self.img[a_y:b_y, a_x:b_x, :]
            zoom_h, zoom_w, _ = zoom_img.shape
            if (zoom_h >= (int(40 / ratio) - 2) 
                    and zoom_w >= (int(40 / ratio) - 2)):
                qimg = QImage(zoom_img.data.tobytes(), zoom_w, zoom_h, 3 * zoom_w, QImage.Format_RGB888)
                painter = QPainter()
                pen = QPen(Qt.black, 1, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
                painter.begin(qimg)
                painter.setPen(pen)
                x_unit, y_unit = int(zoom_w / 4), int(zoom_h / 4)
                painter.drawLine(2*x_unit, y_unit, 2*x_unit, 3*y_unit)
                painter.drawLine(x_unit, 2*y_unit, 3*x_unit, 2*y_unit)
                painter.end()
                self.zoom_label.setPixmap(QPixmap.fromImage(qimg))
                
    # def zoom(self):
    #     widgets = self.get_checked_pos_widgets()
    #     if len(widgets) > 0:
    #         pos_x = -1
    #         pos_y = -1
    #         for widget in widgets:
    #             if isinstance(widget, QtWidgets.QSpinBox):
    #                 if 'pos_x' in widget.objectName():
    #                     pos_x = widget.value()
    #                 if 'pos_y' in widget.objectName():
    #                     pos_y = widget.value()
    #         if pos_x >= 0 and pos_y >= 0:
    #             h, w, _ = self.img.shape
    #             a_x = max(0, pos_x - 100)
    #             b_x = min(w, pos_x + 100)
    #             a_y = max(0, pos_y - 100)
    #             b_y = min(h, pos_y + 100)
    #             qimg = QImage(self.img[a_x:b_x, a_y:b_y, :].data, (b_x - a_x), (b_y - a_y), 3 * (b_x - a_x), QImage.Format_RGB888)
    #             self.zoom_label.setPixmap(QPixmap.fromImage(qimg))

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
