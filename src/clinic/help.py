from PyQt5.QtWidgets import QDialog
from src.ui.help import Ui_DlgHelp


class DlgHelp(QDialog, Ui_DlgHelp):
    """Dialog window for the help document"""
    def __init__(self):
        super(DlgHelp, self).__init__()
        self.setupUi(self)

        # Event handler for push button
        self.btnExit.clicked.connect(self.close)