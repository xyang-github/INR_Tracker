from PyQt5.QtCore import Qt
from src.message_boxes.msg_critical import *
from src.message_boxes.msg_info import *


def message_box_critical(msg):
    """Creates a dialog window showing a critical message"""
    msg_box = DlgMessageBoxCritical()
    msg_box.setModal(True)
    msg_box.setWindowFlag(Qt.FramelessWindowHint)
    msg_box.setAttribute(Qt.WA_TranslucentBackground)
    msg_box.tedMessage.setPlainText(msg)
    msg_box.show()
    msg_box.exec()


def message_box_question(msg):
    """Creates a dialog window asking for verification"""
    msg_box = DlgMessageBoxQuestion()
    msg_box.setWindowFlag(Qt.FramelessWindowHint)
    msg_box.setAttribute(Qt.WA_TranslucentBackground)
    msg_box.tedMsg.setText(msg)
    msg_box.btnDecline.clicked.connect(msg_box.done)
    return msg_box