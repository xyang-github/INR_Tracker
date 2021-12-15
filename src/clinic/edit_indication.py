from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog

from src.ui.editindication import Ui_DlgEditIndication
from src.validate import validate_new_indication
from src.message_boxes.format_msg import message_box_critical


class DlgEditIndication(QDialog, Ui_DlgEditIndication):
    """Dialog window for editing/renaming an item from the indication list widget"""
    def __init__(self, original_indication):
        super(DlgEditIndication, self).__init__()
        self.setupUi(self)

        # Populate the line edit widget with the name of the selected list widget item
        self.original_indication = original_indication
        self.ledIndication.setText(self.original_indication)

        # Event handlers for push buttons
        self.btnOk.clicked.connect(self.btn_ok_clicked)
        self.btnExit.clicked.connect(self.close)

    def btn_ok_clicked(self):
        """Update the list widget item and the database"""
        new_indication = self.ledIndication.text().lower()
        error_message = validate_new_indication(new_indication)

        if error_message:
            message_box_critical(error_message)
        else:
            query = QSqlQuery()
            query.prepare("UPDATE indication SET indication_name = :new_name WHERE indication_name = :orig_name")
            query.bindValue(":new_name", new_indication)
            query.bindValue(":orig_name", self.original_indication)
            bOk = query.exec()
            if bOk:
                message_box_critical(f"The indication for {self.original_indication} has been renamed to {new_indication}.")
                self.close()