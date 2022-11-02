import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import loadUiType

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "form.ui"))


def clickedd():
    print("Button clicked!!!!!!")


class OCR(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.image = None
        self.button.clicked.connect(lambda: clickedd())


if __name__ == "__main__":
    app = QApplication([])
    widget = OCR()
    widget.show()
    sys.exit(app.exec_())
