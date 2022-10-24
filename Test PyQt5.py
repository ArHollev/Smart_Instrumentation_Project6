import PyQt5 as pq
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout

"""
# Every GUI app must have exactly one instance of QApplication. Many parts of Qt don't work until you have executed the above line.
app = QApplication([])
# The brackets [] in the above line represent the command line arguments passed to the application. Because our app doesn't use any parameters, we leave the brackets empty.

app.setStyle('Fusion')

# create a window
# use the most basic type QWidget for it because it merely acts as a container and we don't want it to have any special behavior
window = QWidget()
layout = QVBoxLayout()

layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))

# tell the window to use this layout (and thus its contents)
window.setLayout(layout)
window.show()
"""

"""
label = QLabel('Hello World!')
label.show()
"""

from PyQt5.QtWidgets import *
app = QApplication([])
button = QPushButton('Click')
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()

# button.clicked is a signal, .connect(...) lets us install a so-called slot on it. This is simply a function that gets called when the signal occurs.
# In the above example, our slot shows a message box.
button.clicked.connect(on_button_clicked)
button.show()

# Hand control over to Qt and ask it to "run the application until the user closes it".
app.exec()