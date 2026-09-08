from PySide6.QtWidgets import QMainWindow, QHeaderView
from ui.ui_mainwindow import Ui_MainWindow
from logic.logic import query_load_profile

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.table_hours.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_hours.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.centralwidget.setVisible(False)
        self.btnQuery.clicked.connect(query_load_profile)
