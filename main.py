from ShoutWindow import ShoutWindow
from ShoutController import ShoutController
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication()
    window = ShoutWindow()
    controller = ShoutController(window)

    window.show()
    app.exec()