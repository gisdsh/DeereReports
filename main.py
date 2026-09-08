import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ui_mainwindow import Ui_MainWindow
from logic.login import get_tokens


class MainController:
    def __init__(self):
        self.ui = MainWindow()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.btnLogin.clicked.connect(login)


def login():
    tokens = get_tokens()
    if not tokens:
        app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Deere Reports")
    login_btn = msg_box.addButton("Ingresar", QMessageBox.ButtonRole.AcceptRole)
    cancel_btn = msg_box.addButton("Salir", QMessageBox.ButtonRole.RejectRole)
    msg_box.exec()
    if msg_box.clickedButton() == login_btn:
        login()
        sys.exit(app.exec())
    else:
        QApplication.instance().quit()