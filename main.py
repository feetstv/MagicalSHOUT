import sys
from pathlib import Path

from ShoutWindow import ShoutWindow
from ShoutController import ShoutController
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# if __name__ == "__main__":
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#     qml_file = Path(__file__).resolve().parent / "ShoutQMLWindow.qml"
#     engine.load(qml_file)
#     if not engine.rootObjects():
#         sys.exit(-1)
#     app.exec()

if __name__ == "__main__":
    app = QApplication()
    controller = ShoutController()
    controller.window.show()
    app.exec()