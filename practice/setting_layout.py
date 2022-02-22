# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\practice\setting_layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setting_layout(object):
    def setupUi(self, setting_layout):
        setting_layout.setObjectName("setting_layout")
        setting_layout.resize(819, 480)
        self.widget = QtWidgets.QWidget(setting_layout)
        self.widget.setGeometry(QtCore.QRect(0, 0, 560, 56))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.device_layout = QtWidgets.QGridLayout()
        self.device_layout.setObjectName("device_layout")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.device_layout.addWidget(self.label_5, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.device_layout.addWidget(self.label_6, 1, 4, 1, 1)
        self.thermal_status_line = QtWidgets.QLineEdit(self.widget)
        self.thermal_status_line.setReadOnly(True)
        self.thermal_status_line.setObjectName("thermal_status_line")
        self.device_layout.addWidget(self.thermal_status_line, 1, 5, 1, 1)
        self.camera_url_line = QtWidgets.QLineEdit(self.widget)
        self.camera_url_line.setObjectName("camera_url_line")
        self.device_layout.addWidget(self.camera_url_line, 0, 1, 1, 1)
        self.camera_status_line = QtWidgets.QLineEdit(self.widget)
        self.camera_status_line.setReadOnly(True)
        self.camera_status_line.setObjectName("camera_status_line")
        self.device_layout.addWidget(self.camera_status_line, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.device_layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.thermal_url_line = QtWidgets.QLineEdit(self.widget)
        self.thermal_url_line.setObjectName("thermal_url_line")
        self.device_layout.addWidget(self.thermal_url_line, 1, 1, 1, 1)
        self.thermal_test_btn = QtWidgets.QPushButton(self.widget)
        self.thermal_test_btn.setObjectName("thermal_test_btn")
        self.device_layout.addWidget(self.thermal_test_btn, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.device_layout.addWidget(self.label, 0, 0, 1, 1)
        self.camera_test_btn = QtWidgets.QPushButton(self.widget)
        self.camera_test_btn.setObjectName("camera_test_btn")
        self.device_layout.addWidget(self.camera_test_btn, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.device_layout.addItem(spacerItem, 0, 6, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.device_layout.addItem(spacerItem1, 1, 6, 1, 1)
        self.horizontalLayout.addLayout(self.device_layout)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(setting_layout)
        QtCore.QMetaObject.connectSlotsByName(setting_layout)

    def retranslateUi(self, setting_layout):
        _translate = QtCore.QCoreApplication.translate
        setting_layout.setWindowTitle(_translate("setting_layout", "Form"))
        self.label_5.setText(_translate("setting_layout", "status"))
        self.label_6.setText(_translate("setting_layout", "status"))
        self.camera_url_line.setText(_translate("setting_layout", "0"))
        self.camera_url_line.setPlaceholderText(_translate("setting_layout", "0"))
        self.label_2.setText(_translate("setting_layout", "Thermal"))
        self.thermal_url_line.setText(_translate("setting_layout", "10.36.172.100:2"))
        self.thermal_url_line.setPlaceholderText(_translate("setting_layout", "192.168.1.64:1"))
        self.thermal_test_btn.setText(_translate("setting_layout", "test"))
        self.label.setText(_translate("setting_layout", "Camera"))
        self.camera_test_btn.setText(_translate("setting_layout", "test"))
        self.pushButton.setText(_translate("setting_layout", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    setting_layout = QtWidgets.QWidget()
    ui = Ui_setting_layout()
    ui.setupUi(setting_layout)
    setting_layout.show()
    sys.exit(app.exec_())
