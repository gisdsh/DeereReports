import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView
from ui.ui_mainwindow import Ui_MainWindow
from logic.login import get_tokens, get_organizations, get_machines

ORGANIZATIONS = []
MACHINES = []

class MainController:
    def __init__(self):
        self.ui = MainWindow()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.table_hours.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_hours.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.centralwidget.setVisible(False)



def login():
    global ORGANIZATIONS
    global MACHINES
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Deere Reports")
    login_btn = msg_box.addButton("Ingresar", QMessageBox.ButtonRole.AcceptRole)
    cancel_btn = msg_box.addButton("Salir", QMessageBox.ButtonRole.RejectRole)
    msg_box.exec()
    if msg_box.clickedButton() == login_btn:
        window.statusbar.showMessage("Cargando . . .")
        tokens = get_tokens()
        if tokens:
            ORGANIZATIONS = get_organizations(tokens)
            MACHINES = get_machines(tokens)
            window.statusbar.showMessage(f"{str(len(ORGANIZATIONS))} organizaciones, {str(len(MACHINES))} máquinas")
        else:
            app.quit()
        window.centralwidget.setVisible(True)
        sys.exit(app.exec())
    else:
        QApplication.instance().quit()



if __name__ == "__main__":
    login()
