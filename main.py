import sys
import os
from PySide2.QtWidgets import QApplication
from mainwindow import MainWindow


os.environ["QT_MAC_WANTS_LAYER"] = "1"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
