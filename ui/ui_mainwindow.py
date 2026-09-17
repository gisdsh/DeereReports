# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 640)
        MainWindow.setMinimumSize(QSize(790, 481))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblFin = QLabel(self.centralwidget)
        self.lblFin.setObjectName(u"lblFin")
        self.lblFin.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblFin, 0, 4, 1, 1)

        self.lblSerie = QLabel(self.centralwidget)
        self.lblSerie.setObjectName(u"lblSerie")
        self.lblSerie.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblSerie, 0, 0, 1, 1)

        self.lblInicio = QLabel(self.centralwidget)
        self.lblInicio.setObjectName(u"lblInicio")
        self.lblInicio.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblInicio, 0, 2, 1, 1)

        self.edtSerie = QLineEdit(self.centralwidget)
        self.edtSerie.setObjectName(u"edtSerie")

        self.gridLayout.addWidget(self.edtSerie, 0, 1, 1, 1)

        self.btnExport = QPushButton(self.centralwidget)
        self.btnExport.setObjectName(u"btnExport")
        self.btnExport.setEnabled(False)

        self.gridLayout.addWidget(self.btnExport, 0, 7, 1, 1)

        self.dteInicio = QDateTimeEdit(self.centralwidget)
        self.dteInicio.setObjectName(u"dteInicio")
        self.dteInicio.setDateTime(QDateTime(QDate(2026, 8, 1), QTime(0, 0, 0)))

        self.gridLayout.addWidget(self.dteInicio, 0, 3, 1, 1)

        self.dteFin = QDateTimeEdit(self.centralwidget)
        self.dteFin.setObjectName(u"dteFin")
        self.dteFin.setDateTime(QDateTime(QDate(2026, 8, 31), QTime(23, 59, 59)))

        self.gridLayout.addWidget(self.dteFin, 0, 5, 1, 1)

        self.btnQuery = QPushButton(self.centralwidget)
        self.btnQuery.setObjectName(u"btnQuery")
        self.btnQuery.setAutoDefault(False)

        self.gridLayout.addWidget(self.btnQuery, 0, 6, 1, 1)

        self.wdg1 = QWidget(self.centralwidget)
        self.wdg1.setObjectName(u"wdg1")

        self.gridLayout.addWidget(self.wdg1, 3, 0, 1, 8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.lblFin.setBuddy(self.dteFin)
        self.lblSerie.setBuddy(self.edtSerie)
        self.lblInicio.setBuddy(self.dteInicio)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MainWindow)

        self.btnQuery.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lblFin.setText(QCoreApplication.translate("MainWindow", u"&Fin", None))
        self.lblSerie.setText(QCoreApplication.translate("MainWindow", u"&Serie", None))
        self.lblInicio.setText(QCoreApplication.translate("MainWindow", u"&Inicio", None))
        self.edtSerie.setText(QCoreApplication.translate("MainWindow", u"1BM8250RHSS000194", None))
        self.btnExport.setText(QCoreApplication.translate("MainWindow", u"&Exportar...", None))
        self.btnQuery.setText(QCoreApplication.translate("MainWindow", u"&Crear tabla", None))
    # retranslateUi

