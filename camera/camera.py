from functools import partial
import sys
import os
import cv2
import numpy as np
import json
import platform
import subprocess
import requests
from requests.auth import HTTPDigestAuth
from requests_toolbelt.multipart import decoder

os.chdir(os.path.dirname(__file__))
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter, QPen
from PyQt5.QtCore import QElapsedTimer, QTimer, Qt, QEvent, QMutex


from app_widget import Ui_app_widget
from utils import *

# rtsp://admin:hk888888@10.36.172.100:554/Streaming/Channels/001

        
class Ui(QWidget, Ui_app_widget):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        
        
        self.mutex = QMutex()
        
        self.camera = None
        self.thermal = None
        self.vis_img = None
        self.ratios = []
        self.angle_diffs = []
        self.offsets = []
        
        self.camera_img = None
        self.camera_resize_img = None
        self.thermal_img = None
        self.thermal_resize_img = None
        
        
        # self.camera_img = cv2.imread('misc/14.jpg')
        # self.camera_resize_img = self.camera_img.copy()
        
        # self.thermal_img = cv2.imread('misc/7.jpg')
        # self.thermal_resize_img = self.thermal_img.copy()
        

        self.installEventFilter(self)

        self._init_tab()
        self._init_toolbar()
        self._init_device()
        self._init_labels()
        self._init_pos_widget()
        self._init_ratio_spin()

        self.setWindowTitle('Thermal Mapping')
        self.show()
    
    def _open_camera(self):
        self.mutex.lock()
        try:
            if isinstance(self.camera, cv2.VideoCapture):
                self.camera.release()
            
            url = self.camera_url_line.text()
            try:
                url = int(url)
            except:
                self.camera = cv2.VideoCapture(url)
            else:                                        
                self.camera = cv2.VideoCapture(int(url))
                
            if not self.camera.isOpened():
                self.camera.release()
                self.camera = None
                self.camera_status_line.setText('could not open camera')
            else:
                self.camera_status_line.setText('success')
        except Exception as e:
            self.camera_status_line.setText(str(e))
        finally:
            self.mutex.unlock()
    
    def _open_thermal(self):
        self.mutex.lock()
        try:
            url = self.thermal_url_line.text()
            self.thermal = partial(get_hk_thermal_array, url)
            thermal_result, err = self.thermal()
            if err is not None:
                raise Exception(err)
            if thermal_result.size == 0:
                self.thermal_status_line.setText('could not open thermal')
            else:
                self.thermal_status_line.setText('success')
        except Exception as e:
            self.thermal_status_line.setText(str(e))
        finally:
            self.mutex.unlock()
    
    def _snapshot(self):
        if self.camera is not None and isinstance(self.camera, cv2.VideoCapture) and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                frame = resize_to_width(frame, 1080, 90)
                self.camera_img = frame
                self.zoom_by_radio('camera', self.camera_label, self.camera_ratio_spin)
            else:
                self.camera_status_line.setText('could not open camera')
        
        if self.thermal is not None:
            thermal_result, err = self.thermal()
            if err is not None or thermal_result.size == 0:
                self.thermal_status_line.setText('could not open thermal')
            else:
                thermal_result = thermal_result.copy()
                # thermal_result[thermal_result < 30] = 0
                thermal_result = enhance_thermal_contrast(thermal_result, True)
                thermal_result = resize_to_width(thermal_result, 120, 90)
                self.thermal_img = thermal_result
                self.zoom_by_radio('thermal', self.thermal_label, self.thermal_ratio_spin)
    
    def _visualize(self):
        if len(self.ratios) > 0 and self.camera_img is not None and self.thermal_img is not None:
            self.vis_img = vis(self.camera_img.copy(), self.thermal_img.copy(), self.ratios[-1], self.offsets[-1])
            h, w, _ = self.vis_img.shape
            qimg = QImage(self.vis_img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
            self.vis_label.setPixmap(QPixmap(qimg))
    
    def _mapping(self):
        if self.camera_img is not None and self.thermal_img is not None:
            cpts = self.get_points(self.pos_camera_vlayout) / self.camera_ratio_spin.value()
            tpts = self.get_points(self.pos_thermal_vlayout) / self.thermal_ratio_spin.value()
            ratio, angle_diff, offset = get_stats(cpts, tpts)
            self.ratios.append(ratio)
            self.angle_diffs.append(angle_diff)
            self.offsets.append(offset)

            h, w, _ = self.camera_img.shape
            th, tw, _ = self.thermal_img.shape
            x1, y1 = offset
            x2, y2 = offset + np.array([tw, th]) * ratio
            text = ('倍率:{:.1f} 左右誤差:{:d} 上下誤差:{:d}  旋轉誤差:{:.2f}'.format(
                ratio, int(w-x1-x2), int(h-y1-y2), angle_diff))
                        
            stat_widget = QWidget()        
            stat_layout = QHBoxLayout()
            del_btn = QPushButton('delete')
            del_btn.clicked.connect(partial(self.delete_stat_widget, stat_widget))
            stat_layout.addWidget(del_btn)
            stat_line = QLineEdit()
            stat_line.setText(text)
            stat_line.setReadOnly(True)
            stat_layout.addWidget(stat_line)
            stat_widget.setLayout(stat_layout)
            self.stats_layout.insertWidget(0, stat_widget)
            
    def _calculate(self):
        if self.camera_img is not None and self.thermal_img is not None:
            ratios = np.array(self.ratios)
            angle_diffs = np.array(self.angle_diffs)
            offsets = np.array(self.offsets)
            
            ratio = ratios.mean()
            angle_diff = angle_diffs.mean()
            offset = offsets.mean(axis=0)
            
            h, w, _ = self.camera_img.shape
            th, tw, _ = self.thermal_img.shape
            x1, y1 = offset
            x2, y2 = offset + np.array([tw, th]) * ratio
            text = ('倍率:{:.1f} 左右誤差:{:d} 上下誤差:{:d}  旋轉誤差:{:.2f}'.format(
                ratio, int(w-x1-x2), int(h-y1-y2), angle_diff))
            self.result_line.setText(text)
            self.result_line.setReadOnly(True)

        
    def _init_tab(self):
        
        device_widget = QWidget()
        device_widget.setLayout(self.device_layout)
        camera_widget = QWidget()
        camera_widget.setLayout(self.camera_layout)
        thermal_widget = QWidget()
        thermal_widget.setLayout(self.thermal_layout)
        result_widget = QWidget()
        result_widget.setLayout(self.result_layout)
        
        self.app_tab.addTab(device_widget, 'Device')
        self.app_tab.addTab(camera_widget, 'Camera')
        self.app_tab.addTab(thermal_widget, 'Thermal')
        self.app_tab.addTab(result_widget, 'Result')
        self.setLayout(self.app_layout)
        
        
    def _init_device(self):
        self.camera_test_btn.clicked.connect(self._open_camera)
        self.thermal_test_btn.clicked.connect(self._open_thermal)
        
    def _init_toolbar(self):
        self.snapshot_btn.clicked.connect(self._snapshot)
        self.mapping_btn.clicked.connect(self._mapping)
        self.visualize_btn.clicked.connect(self._visualize)
        self.calculate_btn.clicked.connect(self._calculate)
        
    def _init_labels(self):
        self.is_camera_zoomable = False
        self.is_thermal_zoomable = False
        
        # h, w, _ = self.camera_img.shape
        # qimg = QImage(self.camera_img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
        # self.camera_label.setPixmap(QPixmap(qimg))
        self.camera_label.installEventFilter(self)
        self.camera_scroll.setWidget(self.camera_label)
        self.camera_scroll.installEventFilter(self)
        # self.zoom_camera_label.setScaledContents(True)
        self.zoom_camera_scroll.setWidget(self.zoom_camera_label)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.zoom_camera_label.setAlignment(Qt.AlignCenter)
        
        # h, w, _ = self.thermal_img.shape
        # qimg = QImage(self.thermal_img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
        # self.thermal_label.setPixmap(QPixmap(qimg))
        self.thermal_label.installEventFilter(self)
        self.thermal_scroll.setWidget(self.thermal_label)
        self.thermal_scroll.installEventFilter(self)
        # self.zoom_thermal_label.setScaledContents(True)
        self.zoom_thermal_scroll.setWidget(self.zoom_thermal_label)
        self.thermal_label.setAlignment(Qt.AlignCenter)
        self.zoom_thermal_label.setAlignment(Qt.AlignCenter)
        
        self.vis_label.setAlignment(Qt.AlignCenter)
        self.vis_scroll.setWidget(self.vis_label)
        
    def _init_pos_widget(self):
        for hlayout in self.pos_camera_vlayout.children():
            widgets = [hlayout.itemAt(i).widget() for i in range(hlayout.count())]
            for widget in widgets:
                if isinstance(widget, QtWidgets.QSpinBox):
                    widget.setMinimum(0)
                    if 'pos_x' in widget.objectName():
                        widget.setMaximum(1080)
                    else:
                        widget.setMaximum(1920)
                    widget.valueChanged.connect(partial(self.zoom_by_pos_radio, 'camera', self.zoom_camera_label, self.pos_camera_vlayout, self.pos_camera_radio_group, self.zoom_camera_ratio_spin))
                if isinstance(widget, QtWidgets.QRadioButton):
                    widget.clicked.connect(partial(self.zoom_by_pos_radio, 'camera', self.zoom_camera_label, self.pos_camera_vlayout, self.pos_camera_radio_group, self.zoom_camera_ratio_spin))
                    
        for hlayout in self.pos_thermal_vlayout.children():
            widgets = [hlayout.itemAt(i).widget() for i in range(hlayout.count())]
            for widget in widgets:
                if isinstance(widget, QtWidgets.QSpinBox):
                    widget.setMinimum(0)
                    if 'pos_x' in widget.objectName():
                        widget.setMaximum(1080)
                    else:
                        widget.setMaximum(1920)
                    widget.valueChanged.connect(partial(self.zoom_by_pos_radio, 'thermal', self.zoom_thermal_label, self.pos_thermal_vlayout, self.pos_thermal_radio_group, self.zoom_thermal_ratio_spin))
                if isinstance(widget, QtWidgets.QRadioButton):
                    widget.clicked.connect(partial(self.zoom_by_pos_radio, 'thermal', self.zoom_thermal_label, self.pos_thermal_vlayout, self.pos_thermal_radio_group, self.zoom_thermal_ratio_spin))
    
    def _init_ratio_spin(self):
        self.camera_ratio_spin.valueChanged.connect(partial(self.zoom_by_radio, 'camera', self.camera_label, self.camera_ratio_spin))
        self.zoom_camera_ratio_spin.valueChanged.connect(partial(self.zoom_by_pos_radio, 'camera', self.zoom_camera_label, self.pos_camera_vlayout, self.pos_camera_radio_group, self.zoom_camera_ratio_spin))
        self.thermal_ratio_spin.valueChanged.connect(partial(self.zoom_by_radio, 'thermal', self.thermal_label, self.thermal_ratio_spin))
        self.zoom_thermal_ratio_spin.valueChanged.connect(partial(self.zoom_by_pos_radio, 'thermal', self.zoom_thermal_label, self.pos_thermal_vlayout, self.pos_thermal_radio_group, self.zoom_thermal_ratio_spin))
        self.vis_ratio_spin.valueChanged.connect(partial(self.zoom_by_radio, 'vis', self.vis_label, self.vis_ratio_spin))
    
    def eventFilter(self, source, event):
        if source == self.camera_label:
            self.handle_zoom_event(
                event,
                'camera',
                self.zoom_camera_label,
                self.pos_camera_vlayout,
                self.pos_camera_radio_group,
                self.zoom_camera_ratio_spin,
                self.is_camera_zoomable)
        if source == self.thermal_label:
            self.handle_zoom_event(
                event,
                'thermal',
                self.zoom_thermal_label,
                self.pos_thermal_vlayout,
                self.pos_thermal_radio_group,
                self.zoom_thermal_ratio_spin,
                self.is_thermal_zoomable)

        if event.type() == QEvent.KeyPress:
            if self.app_tab.currentIndex() == 1:
                self.handle_zoom_event(
                    event,
                    'camera',
                    self.zoom_camera_label,
                    self.pos_camera_vlayout,
                    self.pos_camera_radio_group,
                    self.zoom_camera_ratio_spin,
                    self.is_camera_zoomable)
            elif self.app_tab.currentIndex() == 2:
                self.handle_zoom_event(
                    event,
                    'thermal',
                    self.zoom_thermal_label,
                    self.pos_thermal_vlayout,
                    self.pos_thermal_radio_group,
                    self.zoom_thermal_ratio_spin,
                    self.is_thermal_zoomable)

        if event.type() == QEvent.KeyPress and event.modifiers() == Qt.ControlModifier:
            self.is_camera_zoomable = True
            self.is_thermal_zoomable = True
        if event.type() == QEvent.KeyRelease and event.modifiers() == Qt.NoModifier:
            self.is_camera_zoomable = False
            self.is_thermal_zoomable = False

        return QtWidgets.QWidget.eventFilter(self, source, event)

    def get_points(self, vlayout):
        points = []
        for hlayout in vlayout.children():
            point = [0, 0]
            widgets = [hlayout.itemAt(i).widget() for i in range(hlayout.count())]
            for widget in widgets:
                if isinstance(widget, QtWidgets.QSpinBox):
                    if 'pos_x' in widget.objectName():
                        point[0] = widget.value()
                    else:
                        point[1] = widget.value()
            points.append(point)
        
        return np.array(points)
        
    def handle_zoom_event(self, event, itype, label, vlayout, btn_group, zoom_ratio_spin, is_zoomable):
        if event.type() == QEvent.MouseButtonPress:
            widgets = self.get_checked_pos_widgets(vlayout, btn_group)
            if len(widgets) > 0:
                for widget in widgets:
                    if isinstance(widget, QtWidgets.QSpinBox):
                        if 'pos_x' in widget.objectName():
                            widget.setValue(event.x())
                        else:
                            widget.setValue(event.y())
        elif event.type() == QEvent.MouseMove and is_zoomable:
            if itype == 'camera':
                self.zoom(self.camera_resize_img, label, zoom_ratio_spin, event.x(), event.y())
            else:
                self.zoom(self.thermal_resize_img, label, zoom_ratio_spin, event.x(), event.y())
        elif event.type() == QEvent.KeyPress and event.key() in [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D]:
            widgets = self.get_checked_pos_widgets(vlayout, btn_group)
            if len(widgets) > 0:
                x, y = 0, 0
                for widget in widgets:
                    if isinstance(widget, QtWidgets.QSpinBox):
                        if 'pos_x' in widget.objectName():
                            x = widget.value()
                        else:
                            y = widget.value()
                
                if event.key() == Qt.Key_W:
                    y -= 1
                if event.key() == Qt.Key_S:
                    y += 1
                if event.key() == Qt.Key_A:
                    x -= 1
                if event.key() == Qt.Key_D:
                    x += 1
                
                for widget in widgets:
                    if isinstance(widget, QtWidgets.QSpinBox):
                        if 'pos_x' in widget.objectName():
                            widget.setValue(x)
                        else:
                            widget.setValue(y)
            
                if itype == 'camera':
                    self.zoom(self.camera_resize_img, label, zoom_ratio_spin, x, y)
                else:
                    self.zoom(self.thermal_resize_img, label, zoom_ratio_spin, x, y)  

    def get_checked_pos_widgets(self, vlayout, btn_group):
        for i, rbtn in enumerate(btn_group.buttons()):
            if rbtn.isChecked():
                hlayout = vlayout.itemAt(i)
                widgets = [hlayout.itemAt(j).widget() for j in range(hlayout.count())]
                return widgets
        return []
    
    def zoom(self, img, label, zoom_ratio_spin, pos_x, pos_y):
        if pos_x >= 0 and pos_y >= 0:
            ratio = zoom_ratio_spin.value()
            h, w, _ = img.shape
            a_x = max(0, pos_x - int(20 / ratio))
            b_x = min(w, pos_x + int(20 / ratio))
            b_x += (b_x - a_x) % 2 + 1
            a_y = max(0, pos_y - int(20 / ratio))
            b_y = min(h, pos_y + int(20 / ratio))
            b_y += (b_y - a_y) % 2 + 1
            zoom_img = img[a_y:b_y, a_x:b_x, :].copy()
            zoom_h, zoom_w, _ = zoom_img.shape
            if (zoom_h >= (int(40 / ratio) - 2) 
                    and zoom_w >= (int(40 / ratio) - 2)):
                c_x, c_y = round(zoom_w / 2), round(zoom_h / 2)
                x_unit, y_unit = round(zoom_w / 4), round(zoom_h / 4)
                zoom_img = cv2.line(zoom_img, (c_x, c_y - y_unit),
                                (c_x, c_y + y_unit), (0, 0, 0), 1)
                zoom_img = cv2.line(zoom_img, (c_x - x_unit, c_y),
                                (c_x + x_unit, c_y), (0, 0, 0), 1)
                qimg = QImage(zoom_img.data.tobytes(), zoom_w, zoom_h, 3 * zoom_w, QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap(qimg).scaled(500, 500, Qt.KeepAspectRatio)
                label.setPixmap(pixmap)
                
    def zoom_by_pos_radio(self, itype, label, vlayout, btn_group, zoom_ratio_spin, *args):
        widgets = self.get_checked_pos_widgets(vlayout, btn_group)
        if len(widgets) > 0:
            pos_x = -1
            pos_y = -1
            for widget in widgets:
                if isinstance(widget, QtWidgets.QSpinBox):
                    if 'pos_x' in widget.objectName():
                        pos_x = widget.value()
                    if 'pos_y' in widget.objectName():
                        pos_y = widget.value()
            if itype == 'camera':
                self.zoom(self.camera_resize_img, label, zoom_ratio_spin, pos_x, pos_y)
            else:
                self.zoom(self.thermal_resize_img, label, zoom_ratio_spin, pos_x, pos_y)
                
    def zoom_by_radio(self, itype, label, zoom_ratio_spin, *args):
        if itype == 'camera':
            img = self.camera_img
        elif itype == 'thermal':
            img = self.thermal_img
        else:
            img = self.vis_img
        
        if img is not None:
            ratio = zoom_ratio_spin.value()
            resize = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
            h, w, _ = resize.shape
            qimg = QImage(resize.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
            label.setPixmap(QPixmap(qimg))
            
            if itype == 'camera':
                self.camera_resize_img = resize
            else:
                self.thermal_resize_img = resize

    def delete_stat_widget(self, stat_widget):
        index = self.stats_layout.indexOf(stat_widget)
        self.ratios.pop(index)
        self.angle_diffs.pop(index)
        self.offsets.pop(index)
        stat_widget.setParent(None)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    # app.installEventFilter(window)
    app.exec_()
