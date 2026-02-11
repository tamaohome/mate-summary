# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_selector.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QWidget)
class Ui_FileSelector(object):
    def setupUi(self, fileSelector):
        if not fileSelector.objectName():
            fileSelector.setObjectName(u"fileSelector")
        self.horizontalLayout = QHBoxLayout(fileSelector)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pathLineEdit = QLineEdit(fileSelector)
        self.pathLineEdit.setObjectName(u"pathLineEdit")

        self.horizontalLayout.addWidget(self.pathLineEdit)

        self.browsePushButton = QPushButton(fileSelector)
        self.browsePushButton.setObjectName(u"browsePushButton")

        self.horizontalLayout.addWidget(self.browsePushButton)


        self.retranslateUi(fileSelector)

        QMetaObject.connectSlotsByName(fileSelector)
    # setupUi

    def retranslateUi(self, fileSelector):
        self.pathLineEdit.setPlaceholderText(QCoreApplication.translate("FileSelector", u"\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044...", None))
        self.browsePushButton.setText(QCoreApplication.translate("FileSelector", u"\u53c2\u7167...", None))
        pass
    # retranslateUi

