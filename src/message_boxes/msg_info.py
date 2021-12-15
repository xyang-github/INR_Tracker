from src.ui.message_box_question import Ui_DlgMessageBoxQuestion


class DlgMessageBoxQuestion(Ui_DlgMessageBoxQuestion):
    """Dialog window for the clinic report"""
    def __init__(self):
        super(DlgMessageBoxQuestion, self).__init__()
        self.setupUi(self)