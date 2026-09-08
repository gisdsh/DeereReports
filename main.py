import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.ui import MainWindow
from logic.logic import get_tokens, get_organizations, get_machines

ORGANIZATIONS = []
MACHINES = []

class MainController:
    def __init__(self):
        self.ui = MainWindow()


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
