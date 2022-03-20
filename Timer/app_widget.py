# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_app_widget(object):
    def setupUi(self, app_widget):
        if not app_widget.objectName():
            app_widget.setObjectName(u"app_widget")
        app_widget.resize(640, 480)
        self.layoutWidget = QWidget(app_widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 315, 349))
        self.app_layout = QVBoxLayout(self.layoutWidget)
        self.app_layout.setObjectName(u"app_layout")
        self.app_layout.setContentsMargins(20, 20, 20, 20)
        self.timer_lcd = QLCDNumber(self.layoutWidget)
        self.timer_lcd.setObjectName(u"timer_lcd")
        self.timer_lcd.setMinimumSize(QSize(271, 73))
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(36)
        self.timer_lcd.setFont(font)
        self.timer_lcd.setStyleSheet(u"QLCDNumber{\n"
"	color:rgb(255, 255, 255);\n"
"	background-color:rgb(0, 0, 0);\n"
"	border-radius: 5px;\n"
"}")
        self.timer_lcd.setDigitCount(8)
        self.timer_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.timer_lcd.setProperty("value", 12345678.000000000000000)

        self.app_layout.addWidget(self.timer_lcd)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.play_pause_btn = QPushButton(self.layoutWidget)
        self.play_pause_btn.setObjectName(u"play_pause_btn")
        icon = QIcon()
        icon.addFile(u"play-button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play_pause_btn.setIcon(icon)
        self.play_pause_btn.setCheckable(True)
        self.play_pause_btn.setChecked(False)

        self.horizontalLayout.addWidget(self.play_pause_btn)

        self.stop_btn = QPushButton(self.layoutWidget)
        self.stop_btn.setObjectName(u"stop_btn")
        icon1 = QIcon()
        icon1.addFile(u"stop-button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_btn.setIcon(icon1)
        self.stop_btn.setCheckable(False)
        self.stop_btn.setChecked(False)

        self.horizontalLayout.addWidget(self.stop_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8edf\u6b63\u9ed1\u9ad4")
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignRight)

        self.hour_combo = QComboBox(self.layoutWidget)
        self.hour_combo.setObjectName(u"hour_combo")

        self.horizontalLayout_2.addWidget(self.hour_combo, 0, Qt.AlignLeft)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2, 0, Qt.AlignRight)

        self.minute_combo = QComboBox(self.layoutWidget)
        self.minute_combo.setObjectName(u"minute_combo")
        self.minute_combo.setMaxCount(60)

        self.horizontalLayout_4.addWidget(self.minute_combo, 0, Qt.AlignLeft)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_3, 0, Qt.AlignRight)

        self.second_combo = QComboBox(self.layoutWidget)
        self.second_combo.setObjectName(u"second_combo")

        self.horizontalLayout_5.addWidget(self.second_combo, 0, Qt.AlignLeft)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.forever_radio = QRadioButton(self.layoutWidget)
        self.forever_radio.setObjectName(u"forever_radio")

        self.horizontalLayout_3.addWidget(self.forever_radio)

        self.repeat_radio = QRadioButton(self.layoutWidget)
        self.repeat_radio.setObjectName(u"repeat_radio")

        self.horizontalLayout_3.addWidget(self.repeat_radio, 0, Qt.AlignRight)

        self.repeat_combo = QComboBox(self.layoutWidget)
        self.repeat_combo.setObjectName(u"repeat_combo")
        self.repeat_combo.setEditable(False)

        self.horizontalLayout_3.addWidget(self.repeat_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.hint_line = QLineEdit(self.layoutWidget)
        self.hint_line.setObjectName(u"hint_line")
        self.hint_line.setLayoutDirection(Qt.LeftToRight)
        self.hint_line.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.verticalLayout.addWidget(self.hint_line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.hide_btn = QPushButton(self.layoutWidget)
        self.hide_btn.setObjectName(u"hide_btn")

        self.horizontalLayout_7.addWidget(self.hide_btn)

        self.exit_btn = QPushButton(self.layoutWidget)
        self.exit_btn.setObjectName(u"exit_btn")
        self.exit_btn.setStyleSheet(u"QPushButton:checked {color: white;}")

        self.horizontalLayout_7.addWidget(self.exit_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.app_layout.addLayout(self.verticalLayout)


        self.retranslateUi(app_widget)

        QMetaObject.connectSlotsByName(app_widget)
    # setupUi

    def retranslateUi(self, app_widget):
        app_widget.setWindowTitle(QCoreApplication.translate("app_widget", u"Form", None))
        self.play_pause_btn.setText("")
        self.stop_btn.setText("")
        self.label.setText(QCoreApplication.translate("app_widget", u"H", None))
        self.label_2.setText(QCoreApplication.translate("app_widget", u"M", None))
        self.label_3.setText(QCoreApplication.translate("app_widget", u"S", None))
        self.forever_radio.setText(QCoreApplication.translate("app_widget", u"forever", None))
        self.repeat_radio.setText(QCoreApplication.translate("app_widget", u"repeat", None))
        self.hint_line.setText("")
        self.hint_line.setPlaceholderText(QCoreApplication.translate("app_widget", u"hint text", None))
        self.hide_btn.setText(QCoreApplication.translate("app_widget", u"running backgroud", None))
        self.exit_btn.setText(QCoreApplication.translate("app_widget", u"close", None))
    # retranslateUi

