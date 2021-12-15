import re

from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog

from src.ui.add_update_event import Ui_DlgAddEditEvent
from src.style import style_line_edit_error
from src.message_boxes.format_msg import message_box_critical


class DlgAddEditEvent(QDialog, Ui_DlgAddEditEvent):
    """Dialog window for adding and editing events"""
    def __init__(self, id=None):
        super(DlgAddEditEvent, self).__init__()
        self.setupUi(self)
        self.dteDate_event.setDate(QDate.currentDate())
        self.mrn = id

        self.populate_event_list()

        # Event handler for push buttons
        self.btnNewEvent.clicked.connect(self.evt_btn_new_event_clicked)
        self.btnAddEvent.clicked.connect(self.evt_btn_add_event_clicked)
        self.btnRemoveEvent.clicked.connect(self.evt_btn_remove_event_clicked)
        self.btnCancel_event.clicked.connect(self.close)

    def evt_btn_new_event_clicked(self):
        """Add new event to database"""
        self.new_event_name = self.ledNewEvent.text().lower().strip()
        error_message = self.validate_event_name()

        if error_message:
            message_box_critical(error_message)
            self.ledNewEvent.setStyleSheet(style_line_edit_error())
        else:
            query = QSqlQuery()
            query.prepare("INSERT INTO event ('event_name') VALUES :event")
            query.bindValue(":event", self.new_event_name)
            bOk = query.exec()
            if bOk:
                message_box_critical("Event added to the database.")

        self.populate_event_list()
        self.lstCurrentEvent.sortItems()
        self.ledNewEvent.setText("")

    def evt_btn_add_event_clicked(self):
        """Move list widget item to the patient-set event list widget"""
        selected_row = self.lstCurrentEvent.row(self.lstCurrentEvent.currentItem())
        selected_item = self.lstCurrentEvent.takeItem(selected_row)
        self.lstPatientEvent.addItem(selected_item)
        self.lstPatientEvent.sortItems()

    def evt_btn_remove_event_clicked(self):
        """Move list item widget to non-patient event list widget"""
        selected_row = self.lstPatientEvent.row(self.lstPatientEvent.currentItem())
        selected_item = self.lstPatientEvent.takeItem(selected_row)
        self.lstCurrentEvent.addItem(selected_item)
        self.lstCurrentEvent.sortItems()

    def evt_btn_ok_event_clicked(self):
        """Add event to database"""
        # Create a list of event_ids for the patient
        patient_event_names = []
        count = self.lstPatientEvent.count()
        for i in range(count):
            patient_event_names.append(self.lstPatientEvent.item(i).text())

        query = QSqlQuery()
        bOk = query.exec("SELECT event_id, event_name FROM event")
        if bOk:
            all_events = []
            while query.next():
                all_events.append((query.value('event_id'), query.value('event_name')))

        patient_event_ids = []
        for names in patient_event_names:
            for event in all_events:
                if event[1] == names:
                    patient_event_ids.append(event[0])

        msg = "Record added to the database."
        for ids in patient_event_ids:
            query = QSqlQuery()
            query.prepare("INSERT INTO patient_event (date, event_id, patient_id, comment) "
                          "VALUES(:date, :event_id, :patient_id, :comment)")
            query.bindValue(":date", self.dteDate_event.date().toString("yyyy-MM-dd"))
            query.bindValue(":patient_id", self.mrn)
            query.bindValue(":event_id", ids)
            query.bindValue(":comment", self.txtComment_event.toPlainText())
            bOk = query.exec()
            if not bOk:
                messasge = "Not able to add record."
        message_box_critical(msg)
        self.close()

    def populate_event_list(self):
        """Send a query to get events from the database, and populate list widget"""
        self.lstCurrentEvent.clear()

        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM event")
        if bOk:
            while query.next():
                self.lstCurrentEvent.addItem(query.value('event_name'))
            self.lstCurrentEvent.sortItems()

    def validate_event_name(self):
        """Validate user input and returns an error message. Error message is blank if input passes validation"""
        error_message = ""
        string_format = "^[\w() -]{2,}$"  # Allow words, spaces, hyphens, and parenthesis
        if not re.match(string_format, self.new_event_name):
            error_message += "Event name can only contain words, spaces, hyphens, and parenthesis; must be " \
                             "at least 2 characters in length.\n"
        else:
            query = QSqlQuery()
            bOk = query.exec("SELECT event_id, event_name FROM event")
            if bOk:
                all_events = []
                while query.next():
                    all_events.append((query.value('event_id'), query.value('event_name')))

                for event in all_events:
                    if self.new_event_name == event[1]:
                        error_message += "This event already exists.\n"
        return error_message