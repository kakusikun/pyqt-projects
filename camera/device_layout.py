# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\camera\misc\device_layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_device_layout_widget(object):
    def setupUi(self, device_layout_widget):
        device_layout_widget.setObjectName("device_layout_widget")
        device_layout_widget.resize(640, 480)
        self.layoutWidget = QtWidgets.QWidget(device_layout_widget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 100, 831, 54))
        self.layoutWidget.setObjectName("layoutWidget")
        self.device_layout = QtWidgets.QGridLayout(self.layoutWidget)
        self.device_layout.setContentsMargins(0, 0, 0, 0)
        self.device_layout.setObjectName("device_layout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.device_layout.addWidget(self.label_5, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.device_layout.addWidget(self.label_6, 1, 4, 1, 1)
        self.thermal_status_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.thermal_status_line.setReadOnly(True)
        self.thermal_status_line.setObjectName("thermal_status_line")
        self.device_layout.addWidget(self.thermal_status_line, 1, 5, 1, 1)
        self.camera_url_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.camera_url_line.setObjectName("camera_url_line")
        self.device_layout.addWidget(self.camera_url_line, 0, 1, 1, 1)
        self.camera_status_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.camera_status_line.setReadOnly(True)
        self.camera_status_line.setObjectName("camera_status_line")
        self.device_layout.addWidget(self.camera_status_line, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.device_layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.thermal_url_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.thermal_url_line.setObjectName("thermal_url_line")
        self.device_layout.addWidget(self.thermal_url_line, 1, 1, 1, 1)
        self.thermal_test_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.thermal_test_btn.setObjectName("thermal_test_btn")
        self.device_layout.addWidget(self.thermal_test_btn, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.device_layout.addWidget(self.label, 0, 0, 1, 1)
        self.camera_test_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.camera_test_btn.setObjectName("camera_test_btn")
        self.device_layout.addWidget(self.camera_test_btn, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.device_layout.addItem(spacerItem, 0, 6, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.device_layout.addItem(spacerItem1, 1, 6, 1, 1)

        self.retranslateUi(device_layout_widget)
        QtCore.QMetaObject.connectSlotsByName(device_layout_widget)

    def retranslateUi(self, device_layout_widget):
        _translate = QtCore.QCoreApplication.translate
        device_layout_widget.setWindowTitle(_translate("device_layout_widget", "Form"))
        self.label_5.setText(_translate("device_layout_widget", "status"))
        self.label_6.setText(_translate("device_layout_widget", "status"))
        self.camera_url_line.setText(_translate("device_layout_widget", "0"))
        self.camera_url_line.setPlaceholderText(_translate("device_layout_widget", "0"))
        self.label_2.setText(_translate("device_layout_widget", "Thermal"))
        self.thermal_url_line.setText(_translate("device_layout_widget", "10.36.172.100:2"))
        self.thermal_url_line.setPlaceholderText(_translate("device_layout_widget", "192.168.1.64:1"))
        self.thermal_test_btn.setText(_translate("device_layout_widget", "test"))
        self.label.setText(_translate("device_layout_widget", "Camera"))
        self.camera_test_btn.setText(_translate("device_layout_widget", "test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    device_layout_widget = QtWidgets.QWidget()
    ui = Ui_device_layout_widget()
    ui.setupUi(device_layout_widget)
    device_layout_widget.show()
    sys.exit(app.exec_())
