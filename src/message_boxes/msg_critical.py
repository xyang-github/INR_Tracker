from src.ui.message_box_critical import Ui_DlgMessageBoxCritical


class DlgMessageBoxCritical(Ui_DlgMessageBoxCritical):
    """Dialog window for the clinic report"""
    def __init__(self):
        super(DlgMessageBoxCritical, self).__init__()
        self.setupUi(self)

        self.btnOk.setText("OK")
        self.btnOk.clicked.connect(self.close)