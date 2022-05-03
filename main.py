import sys
import os
from PySide6.QtWidgets import QApplication
from source_python.mainwindow import MainWindow


os.environ["QT_MAC_WANTS_LAYER"] = "1"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
