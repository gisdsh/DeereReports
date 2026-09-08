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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDateTimeEdit, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(790, 481)
        MainWindow.setMinimumSize(QSize(790, 481))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnQuery = QPushButton(self.centralwidget)
        self.btnQuery.setObjectName(u"btnQuery")

        self.gridLayout.addWidget(self.btnQuery, 0, 7, 1, 1)

        self.dteFin = QDateTimeEdit(self.centralwidget)
        self.dteFin.setObjectName(u"dteFin")

        self.gridLayout.addWidget(self.dteFin, 0, 5, 1, 1)

        self.lblSerie = QLabel(self.centralwidget)
        self.lblSerie.setObjectName(u"lblSerie")
        self.lblSerie.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblSerie, 0, 0, 1, 1)

        self.table_hours = QTableWidget(self.centralwidget)
        if (self.table_hours.columnCount() < 15):
            self.table_hours.setColumnCount(15)
        if (self.table_hours.rowCount() < 13):
            self.table_hours.setRowCount(13)
        self.table_hours.setObjectName(u"table_hours")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_hours.sizePolicy().hasHeightForWidth())
        self.table_hours.setSizePolicy(sizePolicy)
        self.table_hours.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_hours.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_hours.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.table_hours.setRowCount(13)
        self.table_hours.setColumnCount(15)
        self.table_hours.horizontalHeader().setVisible(True)
        self.table_hours.horizontalHeader().setCascadingSectionResizes(False)
        self.table_hours.horizontalHeader().setDefaultSectionSize(50)
        self.table_hours.horizontalHeader().setHighlightSections(True)
        self.table_hours.verticalHeader().setHighlightSections(True)

        self.gridLayout.addWidget(self.table_hours, 1, 0, 1, 9)

        self.edtSerie = QLineEdit(self.centralwidget)
        self.edtSerie.setObjectName(u"edtSerie")

        self.gridLayout.addWidget(self.edtSerie, 0, 1, 1, 1)

        self.dteInicio = QDateTimeEdit(self.centralwidget)
        self.dteInicio.setObjectName(u"dteInicio")

        self.gridLayout.addWidget(self.dteInicio, 0, 3, 1, 1)

        self.lblInicio = QLabel(self.centralwidget)
        self.lblInicio.setObjectName(u"lblInicio")
        self.lblInicio.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblInicio, 0, 2, 1, 1)

        self.lblFin = QLabel(self.centralwidget)
        self.lblFin.setObjectName(u"lblFin")
        self.lblFin.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblFin, 0, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 790, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.lblSerie.setBuddy(self.edtSerie)
        self.lblInicio.setBuddy(self.dteInicio)
        self.lblFin.setBuddy(self.dteFin)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btnQuery.setText(QCoreApplication.translate("MainWindow", u"&Generar", None))
        self.lblSerie.setText(QCoreApplication.translate("MainWindow", u"&Serie", None))
        self.lblInicio.setText(QCoreApplication.translate("MainWindow", u"&Inicio", None))
        self.lblFin.setText(QCoreApplication.translate("MainWindow", u"&Fin", None))
    # retranslateUi

