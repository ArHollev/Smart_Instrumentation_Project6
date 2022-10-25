import sys

from PySide6.QtWidgets import *


def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 200, 300)
    window.setWindowTitle("Yoooo")

    layout = QVBoxLayout()

    label = QLabel("Press the Button")
    button = QPushButton("press me")
    textbox = QTextEdit()

    button.clicked.connect(lambda: on_clicked(textbox.toPlainText()))

    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    window.setLayout(layout)

    window.show()
    app.exec()


def on_clicked(msg):
    message = QMessageBox()
    message.setText(msg)
    message.exec()


if __name__ == '__main__':
    main()
