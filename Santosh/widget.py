# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loader = QUiLoader()
        file = QFile("form.ui")
        file.open(QIODevice.ReadOnly)
        self.myWidget = loader.load(file, self)
        file.close()

        self.setCentralWidget(self.myWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
