# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        loader = QUiLoader()
        file = QFile("form.ui")
        file.open(QFile.ReadOnly)
        self.myWidget = loader.load(file, self)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec()
