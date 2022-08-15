from ShoutWindow import ShoutWindow
from ShoutController import ShoutController
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication()
    controller = ShoutController()
    controller.window.show()
    app.exec()