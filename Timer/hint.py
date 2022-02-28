# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hint.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_hint(object):
    def setupUi(self, hint):
        if not hint.objectName():
            hint.setObjectName(u"hint")
        hint.resize(200, 151)
        self.layoutWidget = QWidget(hint)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 181, 131))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hint_label = QLabel(self.layoutWidget)
        self.hint_label.setObjectName(u"hint_label")
        font = QFont()
        font.setFamily(u"\u5fae\u8edf\u6b63\u9ed1\u9ad4")
        font.setPointSize(28)
        self.hint_label.setFont(font)

        self.verticalLayout.addWidget(self.hint_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.retranslateUi(hint)

        QMetaObject.connectSlotsByName(hint)
    # setupUi

    def retranslateUi(self, hint):
        hint.setWindowTitle(QCoreApplication.translate("hint", u"Form", None))
        self.hint_label.setText(QCoreApplication.translate("hint", u"hint", None))
    # retranslateUi

