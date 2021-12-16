from src.ui.indications import Ui_DlgIndications
from src.style import style_line_edit_error
from src.clinic.edit_indication import *
from src.message_boxes.format_msg import message_box_critical, message_box_question


class DlgIndications(QDialog, Ui_DlgIndications):
    """Indication window for application"""
    def __init__(self):
        super(DlgIndications, self).__init__()
        self.setupUi(self)

        # Event handlers for push buttons
        self.btnAddIndication.clicked.connect(self.add_indication)
        self.btnEditIndication.clicked.connect(self.edit_indication_dialog)
        self.btnDeleteIndication.clicked.connect(self.delete_indication)
        self.btnExit.clicked.connect(self.close)

        self.populate_indication_list()

    def add_indication(self):
        """Add a new indication to the indication list widget"""
        self.new_indication = self.ledNewIndication.text().lower().strip(" ")

        # If passes validation, will insert text input into the database
        error_message = validate_new_indication(self.new_indication)
        if error_message:
            message_box_critical(error_message)
            self.ledNewIndication.setStyleSheet(style_line_edit_error())
        else:
            query = QSqlQuery()
            query.prepare("INSERT INTO indication ('indication_name') VALUES (:ind)")
            query.bindValue(":ind", self.new_indication)
            bOk = query.exec()
            if bOk:
                message_box_critical("Indication added to the database.")

            # Repopulate list widget after the database has been updated.
            # Sorts the updated list. Clears line edit widget.
            self.populate_indication_list()
            self.lstIndications.sortItems()
            self.ledNewIndication.setText("")

    def edit_indication_dialog(self):
        """Creates a dialog box to rename a selected indication"""
        error_message = self.validate_if_selected()

        if error_message:
            message_box_critical(error_message)
        else:
            original_indication = self.lstIndications.selectedItems()[0].text()
            edit_dialog = DlgEditIndication(original_indication)
            edit_dialog.show()
            edit_dialog.exec_()
            self.populate_indication_list()

    def delete_indication(self):
        """Delete selected list item widget from the database"""
        error_message = self.validate_if_selected()

        if error_message:
            message_box_critical(error_message)
        else:
            self.selected_indication = self.lstIndications.selectedItems()[0].text()
            self.question = message_box_question(f"Are you sure you want to delete the indication: "
                                                 f"<b>{self.selected_indication}</b>? This will remove the indication "
                                                 f"from all patients that have this indication.")
            self.question.btnAccept.clicked.connect(self.query_delete_indication)
            self.question.show()
            self.question.exec()

            self.populate_indication_list()

    def query_delete_indication(self):
        """
        Send a query to delete an indication from the database
        Must delete from both 'indication' and 'patient_indication' tables
        """
        query = QSqlQuery()
        query.prepare("DELETE FROM indication WHERE indication_name = :name")
        query.bindValue(":name", self.selected_indication)
        bOk = query.exec()
        if bOk:
            for indication in self.all_indications:
                if self.selected_indication == indication[1]:
                    indication_id = indication[0]

            query = QSqlQuery()
            query.prepare("DELETE from patient_indication WHERE indication_id = :id")
            query.bindValue(":id", indication_id)
            bOk = query.exec()
            if bOk:
                message_box_critical(f"The indication: {self.selected_indication} has been deleted.")
                self.question.close()

    def validate_if_selected(self):
        """
        Check if the indication list widget is empty. If not empty, will check if an item has been selected.
        Returns an error message, which is blank if validation passes.
        """
        error_message = ""

        if self.lstIndications.count() == 0:
            error_message += "There is no indication to edit or delete.\n"

        try:
            bOk = self.lstIndications.selectedItems()[0]
        except IndexError:
            error_message += "No item selected to rename or delete."

        return error_message

    def populate_indication_list(self):
        """Populate the indication list widget with indications from the database"""
        self.lstIndications.clear()  # If not cleared, will show duplicate list widget items

        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM indication")
        if bOk:
            self.all_indications = []
            while query.next():
                self.all_indications.append((query.value('indication_id'), query.value('indication_name')))
                self.lstIndications.addItem(query.value('indication_name'))

        self.lstIndications.sortItems()