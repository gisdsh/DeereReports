import sys
import settings
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.ui import MainWindow
from logic.logic import get_tokens, get_organizations, get_machines

settings.ORGANIZATIONS = []
settings.MACHINES = []
settings.TOKENS = {}

class MainController:
    def __init__(self):
        self.ui = MainWindow()


def login():
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
        settings.TOKENS = get_tokens()
        if settings.TOKENS:
            settings.ORGANIZATIONS = get_organizations(settings.TOKENS)
            settings.MACHINES = get_machines(settings.TOKENS)
            window.statusbar.showMessage(f"{str(len(settings.ORGANIZATIONS))} organizaciones, {str(len(settings.MACHINES))} máquinas")
        else:
            app.quit()
        window.centralwidget.setVisible(True)
        window.edtSerie.setFocus()
        window.edtSerie.selectionEnd()
        sys.exit(app.exec())
    else:
        QApplication.instance().quit()


if __name__ == "__main__":
    login()
