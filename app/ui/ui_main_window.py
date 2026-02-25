# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTabWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from app.views.components.file_selector import FileSelector
from app.views.components.summary_table_widget import SummaryTableWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 360)
        MainWindow.setDocumentMode(True)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.fileSelector = FileSelector(self.centralwidget)
        self.fileSelector.setObjectName(u"fileSelector")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileSelector.sizePolicy().hasHeightForWidth())
        self.fileSelector.setSizePolicy(sizePolicy)
        self.fileSelector.setMaximumSize(QSize(16777215, 40))

        self.centralLayout.addWidget(self.fileSelector)

        self.levelTabWidget = QTabWidget(self.centralwidget)
        self.levelTabWidget.setObjectName(u"levelTabWidget")
        self.levelTabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.levelTabWidget.setTabShape(QTabWidget.TabShape.Triangular)
        self.levelTabWidget.setDocumentMode(True)
        self.level1Tab = QWidget()
        self.level1Tab.setObjectName(u"level1Tab")
        self.level1TabLayout = QVBoxLayout(self.level1Tab)
        self.level1TabLayout.setObjectName(u"level1TabLayout")
        self.level1TabLayout.setContentsMargins(0, 0, 0, 0)
        self.level1TableWidget = SummaryTableWidget(self.level1Tab)
        self.level1TableWidget.setObjectName(u"level1TableWidget")
        self.level1TableWidget.setStyleSheet(u"QTableWidget::item:selected { background: #316AC5; }")
        self.level1TableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.level1TabLayout.addWidget(self.level1TableWidget)

        self.levelTabWidget.addTab(self.level1Tab, "")
        self.level2Tab = QWidget()
        self.level2Tab.setObjectName(u"level2Tab")
        self.level2TabLayout = QVBoxLayout(self.level2Tab)
        self.level2TabLayout.setObjectName(u"level2TabLayout")
        self.level2TabLayout.setContentsMargins(0, 0, 0, 0)
        self.level2TableWidget = SummaryTableWidget(self.level2Tab)
        self.level2TableWidget.setObjectName(u"level2TableWidget")
        self.level2TableWidget.setStyleSheet(u"QTableWidget::item:selected { background: #316AC5; }")
        self.level2TableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.level2TabLayout.addWidget(self.level2TableWidget)

        self.levelTabWidget.addTab(self.level2Tab, "")
        self.level3Tab = QWidget()
        self.level3Tab.setObjectName(u"level3Tab")
        self.level3TabLayout = QVBoxLayout(self.level3Tab)
        self.level3TabLayout.setObjectName(u"level3TabLayout")
        self.level3TabLayout.setContentsMargins(0, 0, 0, 0)
        self.level3TableWidget = SummaryTableWidget(self.level3Tab)
        self.level3TableWidget.setObjectName(u"level3TableWidget")
        self.level3TableWidget.setStyleSheet(u"QTableWidget::item:selected { background: #316AC5; }")
        self.level3TableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.level3TabLayout.addWidget(self.level3TableWidget)

        self.levelTabWidget.addTab(self.level3Tab, "")
        self.level4Tab = QWidget()
        self.level4Tab.setObjectName(u"level4Tab")
        self.level4TabLayout = QVBoxLayout(self.level4Tab)
        self.level4TabLayout.setObjectName(u"level4TabLayout")
        self.level4TabLayout.setContentsMargins(0, 0, 0, 0)
        self.level4TableWidget = SummaryTableWidget(self.level4Tab)
        self.level4TableWidget.setObjectName(u"level4TableWidget")
        self.level4TableWidget.setStyleSheet(u"QTableWidget::item:selected { background: #316AC5; }")
        self.level4TableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.level4TabLayout.addWidget(self.level4TableWidget)

        self.levelTabWidget.addTab(self.level4Tab, "")

        self.centralLayout.addWidget(self.levelTabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionSaveAs)
        self.fileMenu.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.levelTabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"\u958b\u304f...", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58...", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\u7d42\u4e86", None))
        self.levelTabWidget.setTabText(self.levelTabWidget.indexOf(self.level1Tab), QCoreApplication.translate("MainWindow", u"#1\u30ec\u30d9\u30eb", None))
        self.levelTabWidget.setTabText(self.levelTabWidget.indexOf(self.level2Tab), QCoreApplication.translate("MainWindow", u"#2\u30ec\u30d9\u30eb", None))
        self.levelTabWidget.setTabText(self.levelTabWidget.indexOf(self.level3Tab), QCoreApplication.translate("MainWindow", u"#3\u30ec\u30d9\u30eb", None))
        self.levelTabWidget.setTabText(self.levelTabWidget.indexOf(self.level4Tab), QCoreApplication.translate("MainWindow", u"#4\u30ec\u30d9\u30eb", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u30d5\u30a1\u30a4\u30eb", None))
    # retranslateUi

