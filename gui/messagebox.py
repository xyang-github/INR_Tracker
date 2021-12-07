import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QMessageBox


class Message(QMessageBox):
    def __init__(self, msg):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        label = QLabel(msg)
        label.setStyleSheet(f"color: black;"
                             "padding: 0px;")

        self.layout.addWidget(label)
        self.setStyleSheet(
            """
            background-color: white;
            width: 200px;
            border: 2px solid purple;
            border-radius: 20px;
            """
        )

        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Message("Hello World")
    w.resize(400, 200)
    w.show()
    sys.exit(app.exec_())
