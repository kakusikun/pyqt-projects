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
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter, QPen
from PyQt5.QtCore import QElapsedTimer, QTimer, Qt, QEvent, QMutex


from app_widget import Ui_Form
from device_layout import Ui_device_layout_widget


INIT_HK_RC_THERMAL_XML_STR = '''
    <?xml version = "1.0" encoding = "UTF-8"?>
    <PixelToPixelParam version = "2.0" xmlns = "http://www.std-cgi.com/ver20/XMLSchema">
    <id>2</id>
    <maxFrameRate>400</maxFrameRate>
    <reflectiveEnable>false</reflectiveEnable>
    <reflectiveTemperature>20.00</reflectiveTemperature>
    <emissivity>1</emissivity>
    <distance>50</distance>
    <refreshInterval>50</refreshInterval>
    <distanceUnit>centimeter</distanceUnit>
    <temperatureDataLength>4</temperatureDataLength>
    <JpegPictureWithAppendData>
    <jpegPicEnabled>true</jpegPicEnabled>
    <visiblePicEnable>true</visiblePicEnable>
    </JpegPictureWithAppendData>
    </PixelToPixelParam>
'''


INIT_HK_TPE_MRT_THERMAL_XML_STR = '''
    <?xml version = "1.0" encoding = "UTF-8"?>
    <PixelToPixelParam version = "2.0" xmlns = "http://www.std-cgi.com/ver20/XMLSchema">
    <id>1</id>
    <maxFrameRate>400</maxFrameRate>
    <reflectiveEnable>false</reflectiveEnable>
    <reflectiveTemperature>20.00</reflectiveTemperature>
    <emissivity>1</emissivity>
    <distance>50</distance>
    <refreshInterval>50</refreshInterval>
    <distanceUnit>centimeter</distanceUnit>
    <temperatureDataLength>4</temperatureDataLength>
    <JpegPictureWithAppendData>
    <jpegPicEnabled>true</jpegPicEnabled>
    <visiblePicEnable>true</visiblePicEnable>
    </JpegPictureWithAppendData>
    </PixelToPixelParam>
'''


def generate_colour_map():
    """
    Conversion of the colour map from GetThermal to a numpy LUT:
        https://github.com/groupgets/GetThermal/blob/bb467924750a686cc3930f7e3a253818b755a2c0/src/dataformatter.cpp#L6
    """

    lut = np.zeros((256, 1, 3), dtype=np.uint8)

    colormapIronBlack = [
        255, 255, 255, 253, 253, 253, 251, 251, 251, 249, 249, 249, 247, 247,
        247, 245, 245, 245, 243, 243, 243, 241, 241, 241, 239, 239, 239, 237,
        237, 237, 235, 235, 235, 233, 233, 233, 231, 231, 231, 229, 229, 229,
        227, 227, 227, 225, 225, 225, 223, 223, 223, 221, 221, 221, 219, 219,
        219, 217, 217, 217, 215, 215, 215, 213, 213, 213, 211, 211, 211, 209,
        209, 209, 207, 207, 207, 205, 205, 205, 203, 203, 203, 201, 201, 201,
        199, 199, 199, 197, 197, 197, 195, 195, 195, 193, 193, 193, 191, 191,
        191, 189, 189, 189, 187, 187, 187, 185, 185, 185, 183, 183, 183, 181,
        181, 181, 179, 179, 179, 177, 177, 177, 175, 175, 175, 173, 173, 173,
        171, 171, 171, 169, 169, 169, 167, 167, 167, 165, 165, 165, 163, 163,
        163, 161, 161, 161, 159, 159, 159, 157, 157, 157, 155, 155, 155, 153,
        153, 153, 151, 151, 151, 149, 149, 149, 147, 147, 147, 145, 145, 145,
        143, 143, 143, 141, 141, 141, 139, 139, 139, 137, 137, 137, 135, 135,
        135, 133, 133, 133, 131, 131, 131, 129, 129, 129, 126, 126, 126, 124,
        124, 124, 122, 122, 122, 120, 120, 120, 118, 118, 118, 116, 116, 116,
        114, 114, 114, 112, 112, 112, 110, 110, 110, 108, 108, 108, 106, 106,
        106, 104, 104, 104, 102, 102, 102, 100, 100, 100, 98, 98, 98, 96, 96,
        96, 94, 94, 94, 92, 92, 92, 90, 90, 90, 88, 88, 88, 86, 86, 86, 84, 84,
        84, 82, 82, 82, 80, 80, 80, 78, 78, 78, 76, 76, 76, 74, 74, 74, 72, 72,
        72, 70, 70, 70, 68, 68, 68, 66, 66, 66, 64, 64, 64, 62, 62, 62, 60, 60,
        60, 58, 58, 58, 56, 56, 56, 54, 54, 54, 52, 52, 52, 50, 50, 50, 48, 48,
        48, 46, 46, 46, 44, 44, 44, 42, 42, 42, 40, 40, 40, 38, 38, 38, 36, 36,
        36, 34, 34, 34, 32, 32, 32, 30, 30, 30, 28, 28, 28, 26, 26, 26, 24, 24,
        24, 22, 22, 22, 20, 20, 20, 18, 18, 18, 16, 16, 16, 14, 14, 14, 12, 12,
        12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 2, 0, 0, 0, 0, 0, 9,
        2, 0, 16, 4, 0, 24, 6, 0, 31, 8, 0, 38, 10, 0, 45, 12, 0, 53, 14, 0,
        60, 17, 0, 67, 19, 0, 74, 21, 0, 82, 23, 0, 89, 25, 0, 96, 27, 0, 103,
        29, 0, 111, 31, 0, 118, 36, 0, 120, 41, 0, 121, 46, 0, 122, 51, 0, 123,
        56, 0, 124, 61, 0, 125, 66, 0, 126, 71, 0, 127, 76, 1, 128, 81, 1, 129,
        86, 1, 130, 91, 1, 131, 96, 1, 132, 101, 1, 133, 106, 1, 134, 111, 1,
        135, 116, 1, 136, 121, 1, 136, 125, 2, 137, 130, 2, 137, 135, 3, 137,
        139, 3, 138, 144, 3, 138, 149, 4, 138, 153, 4, 139, 158, 5, 139, 163,
        5, 139, 167, 5, 140, 172, 6, 140, 177, 6, 140, 181, 7, 141, 186, 7,
        141, 189, 10, 137, 191, 13, 132, 194, 16, 127, 196, 19, 121, 198, 22,
        116, 200, 25, 111, 203, 28, 106, 205, 31, 101, 207, 34, 95, 209, 37,
        90, 212, 40, 85, 214, 43, 80, 216, 46, 75, 218, 49, 69, 221, 52, 64,
        223, 55, 59, 224, 57, 49, 225, 60, 47, 226, 64, 44, 227, 67, 42, 228,
        71, 39, 229, 74, 37, 230, 78, 34, 231, 81, 32, 231, 85, 29, 232, 88,
        27, 233, 92, 24, 234, 95, 22, 235, 99, 19, 236, 102, 17, 237, 106, 14,
        238, 109, 12, 239, 112, 12, 240, 116, 12, 240, 119, 12, 241, 123, 12,
        241, 127, 12, 242, 130, 12, 242, 134, 12, 243, 138, 12, 243, 141, 13,
        244, 145, 13, 244, 149, 13, 245, 152, 13, 245, 156, 13, 246, 160, 13,
        246, 163, 13, 247, 167, 13, 247, 171, 13, 248, 175, 14, 248, 178, 15,
        249, 182, 16, 249, 185, 18, 250, 189, 19, 250, 192, 20, 251, 196, 21,
        251, 199, 22, 252, 203, 23, 252, 206, 24, 253, 210, 25, 253, 213, 27,
        254, 217, 28, 254, 220, 29, 255, 224, 30, 255, 227, 39, 255, 229, 53,
        255, 231, 67, 255, 233, 81, 255, 234, 95, 255, 236, 109, 255, 238, 123,
        255, 240, 137, 255, 242, 151, 255, 244, 165, 255, 246, 179, 255, 248,
        193, 255, 249, 207, 255, 251, 221, 255, 253, 235, 255, 255, 24]

    def colormapChunk(ulist, step):
        return map(lambda i: ulist[i: i + step], range(0, len(ulist), step))

    chunks = colormapChunk(colormapIronBlack, 3)

    red = []
    green = []
    blue = []

    for chunk in chunks:
        red.append(chunk[0])
        green.append(chunk[1])
        blue.append(chunk[2])

    lut[:, 0, 0] = blue
    lut[:, 0, 1] = green
    lut[:, 0, 2] = red

    return lut


# Generate color map - used for colorizing the video frame.
colorMap = generate_colour_map()
clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))


def enhance_thermal_contrast(thermal, colorized=False):
    normed = cv2.normalize(thermal, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(normed)
    nor = cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR)
    if colorized:
        nor = cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR)
        colorized_img = cv2.LUT(nor, colorMap)
        return colorized_img
    return nor


def resize_to_width(img, width, angle=0):
    if angle == 90:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == -90:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif angle == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif angle != 0:
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
        img = cv2.warpAffine(img, M, (w, h))
    h, w = img.shape[:2]
    r = width / w
    nh = h * r
    img = cv2.resize(img, (width, int(nh)))
    return img


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP)
    request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(
        command, stdout=subprocess.PIPE) == 0
    
    
def init_hk_thermal_camera(ip: str):
    err = None
    try:
        ip, channel = ip.split(':')
        if not ping(ip):
            raise ConnectionError('could not find thermal')
        r = requests.put(
            f'http://{ip}:80/ISAPI/Thermal'
            + f'/channels/{channel}/thermometry/PixelToPixelParam',
            data=INIT_HK_RC_THERMAL_XML_STR if channel == 2 else INIT_HK_TPE_MRT_THERMAL_XML_STR,
            headers={'Content-Type': 'application/xml'},
            auth=HTTPDigestAuth('admin', 'hk888888'),
            timeout=3.0)
        if r.status_code != 200:
            err = f'unexpected result ({r.status_code})'
    except Exception as e:
        err = str(e)
    return err

def get_hk_thermal_array(ip: str, vis: bool = False) -> np.ndarray:
    ip, channel = ip.split(':')
    thermal_result = np.empty(0)
    err = None
    try:
        r = requests.get(
            f'http://{ip}:80/ISAPI/Thermal'
            + f'/channels/{channel}/thermometry/jpegPicWithAppendData?format=json',
            auth=HTTPDigestAuth('admin', 'hk888888'))
        multipart_data = decoder.MultipartDecoder.from_response(r)
        info = json.loads(multipart_data.parts[0].content)
        w_thermal = info['JpegPictureWithAppendData']['jpegPicWidth']
        h_thermal = info['JpegPictureWithAppendData']['jpegPicHeight']
        thermal_result = np.frombuffer(
            multipart_data.parts[2].content, np.float32).reshape(h_thermal,
                                                                 w_thermal)
    except Exception as e:
        err = str(e)
    else:
        if vis and thermal_result.size > 0:
            thermal_result = (thermal_result - thermal_result.min())
            thermal_result /= thermal_result.max()
            thermal_result *= 255
            thermal_result = thermal_result.copy().astype(np.uint8)
            thermal_result = np.repeat(
                thermal_result[..., np.newaxis], 3, axis=2)
            # visual_thermal_show = cv2.normalize(
            #     visual_thermal,
            #     None,
            #     alpha=0,
            #     beta=255,
            #     norm_type=cv2.NORM_MINMAX,
            #     dtype=cv2.CV_8U)
            # color = cv2.applyColorMap(visual_thermal_show, cv2.COLORMAP_JET)
            # color = thermal_result
            # cv2.imwrite(filename, color)
    return thermal_result, err

# rtsp://admin:hk888888@10.36.172.100:554/Streaming/Channels/001



class DeviceLayout(QWidget, Ui_device_layout_widget):
    def __init__(self):
        super(DeviceLayout, self).__init__()
        self.setupUi(self)
        self.setLayout(self.device_layout)
        
        # self.mutex = QMutex()
        # self.camera = None
        # self.thermal = None
        
class Ui(QWidget, Ui_Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        
        camera_widget = QWidget()
        camera_widget.setLayout(self.horizontalLayout_16)
        thermal_widget = QWidget()
        thermal_widget.setLayout(self.horizontalLayout_17)
        device_widget = QWidget()
        device_widget.setLayout(self.device_layout)
        
        self.app_tab.addTab(device_widget, 'Device')
        self.app_tab.addTab(camera_widget, 'Camera')
        self.app_tab.addTab(thermal_widget, 'Thermal')
        self.setLayout(self.horizontalLayout_15)
        
        self.mutex = QMutex()
        
        self.camera = None
        self.thermal = None
        
        
        self.camera_img = cv2.imread('misc/14.jpg')
        self.camera_resize_img = self.camera_img.copy()
        
        self.thermal_img = cv2.imread('misc/7.jpg')
        self.thermal_resize_img = self.thermal_img.copy()

        self.installEventFilter(self)

        self._init_device()
        self._init_labels()
        self._init_pos_widget()
        self._init_ratio_spin()

        self.setWindowTitle('Camera')
        self.show()
    
    def _open_camera(self):
        self.mutex.lock()
        try:
            if self.camera is None:
                url = self.camera_url_line.text()
                self.camera = cv2.VideoCapture(int(url))
                if not self.camera.isOpened():
                    self.camera.release()
                    self.camera = None
                    self.camera_status_line.setText('could not open camera')
                else:
                    self.camera_status_line.setText('success')
            elif isinstance(self.camera, cv2.VideoCapture) and not self.camera.isOpened():
                self.camera.release()
                url = self.camera_url_line.text()
                self.camera = cv2.VideoCapture(url)
                if not self.camera.isOpened():
                    self.camera.release()
                    self.camera = None
                    self.camera_status_line.setText('could not open camera')
                else:
                    self.camera_status_line.setText('success')
            else:
                self.camera_status_line.setText('connected')
        except Exception as e:
            self.camera_status_line.setText(str(e))
        finally:
            self.mutex.unlock()
    
    def _open_thermal(self):
        self.mutex.lock()
        try:
            if self.thermal is None:
                url = self.thermal_url_line.text()
                # err = init_hk_thermal_camera(url)
                # if err is not None:
                #     raise Exception(err)
                
                self.thermal = partial(get_hk_thermal_array, url)
                thermal_result, err = self.thermal()
                if err is not None:
                    raise Exception(err)
                if thermal_result.size == 0:
                    self.thermal = None
                    self.thermal_status_line.setText('could not open thermal')
                else:
                    self.thermal_status_line.setText('success')
            elif callable(self.thermal):
                thermal_result, err = self.thermal()
                if err is not None:
                    raise Exception(err)
                if thermal_result.size == 0:
                    self.thermal = None
                    self.thermal_status_line.setText('could not open thermal')
                else:
                    self.thermal_status_line.setText('success')
            else:
                self.thermal_status_line.setText('connected')
        except Exception as e:
            self.thermal_status_line.setText(str(e))
        finally:
            self.mutex.unlock()
    
    def _snapshot(self):
        if self.camera is not None and isinstance(self.camera, cv2.VideoCapture) and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                frame = resize_to_width(frame, 540, 90)
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
    
    def _init_device(self):
        self.camera_test_btn.clicked.connect(self._open_camera)
        self.thermal_test_btn.clicked.connect(self._open_thermal)
        self.snapshot.clicked.connect(self._snapshot)
        
    def _init_labels(self):
        self.is_camera_zoomable = False
        self.is_thermal_zoomable = False
        
        h, w, _ = self.camera_img.shape
        qimg = QImage(self.camera_img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
        self.camera_label.setPixmap(QPixmap(qimg))
        self.camera_label.installEventFilter(self)
        self.camera_scroll.setWidget(self.camera_label)
        self.camera_scroll.installEventFilter(self)
        self.zoom_camera_label.setScaledContents(True)
        self.zoom_camera_scroll.setWidget(self.zoom_camera_label)
        
        h, w, _ = self.thermal_img.shape
        qimg = QImage(self.thermal_img.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
        self.thermal_label.setPixmap(QPixmap(qimg))
        self.thermal_label.installEventFilter(self)
        self.thermal_scroll.setWidget(self.thermal_label)
        self.thermal_scroll.installEventFilter(self)
        self.zoom_thermal_label.setScaledContents(True)
        self.zoom_thermal_scroll.setWidget(self.zoom_thermal_label)
        
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
    
    def eventFilter(self, source, event):
        if source == self.camera_label:
            self.handle_plot_event(
                event,
                'camera',
                self.zoom_camera_label,
                self.pos_camera_vlayout,
                self.pos_camera_radio_group,
                self.zoom_camera_ratio_spin,
                self.is_camera_zoomable)
        if source == self.thermal_label:
            self.handle_plot_event(
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
        
        points = np.array(points)
        

    def handle_plot_event(self, event, itype, label, vlayout, btn_group, zoom_ratio_spin, is_zoomable):
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
                pixmap = QPixmap(qimg).scaled(300, 300, Qt.KeepAspectRatio)
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
        else:
            img = self.thermal_img
        
        ratio = zoom_ratio_spin.value()
        resize = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
        h, w, _ = resize.shape
        qimg = QImage(resize.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap(qimg))
        
        if itype == 'camera':
            self.camera_resize_img = resize
        else:
            self.thermal_resize_img = resize
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    # app.installEventFilter(window)
    app.exec_()
