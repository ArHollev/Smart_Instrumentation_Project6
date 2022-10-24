import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

import random
from PySide6 import QtCore, QtWidgets, QtGui

# Simpele 'Hello World!' pagina     
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     label = QLabel("Hello World", alignment=Qt.AlignCenter)
#     label.show()
#     sys.exit(app.exec_())

   
# Define a class named MyWidget, which extends QWidget and includes a QPushButton and QLabel.
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
    # The MyWidget class has the magic member function that randomly chooses an item from the hello list. 
    # When you click the button, the magic function is called.
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

# Now, add a main function where you instantiate MyWidget and show it.
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())