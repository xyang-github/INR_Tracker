import re
from src.ui.events import Ui_DlgEvents
from src.style import style_line_edit_error
from src.clinic.edit_indication import *
from src.message_boxes.format_msg import message_box_critical, message_box_question
from src.clinic.edit_event import *


class DlgEvents(QDialog, Ui_DlgEvents):
    """Event window for application"""
    def __init__(self):
        super(DlgEvents, self).__init__()
        self.setupUi(self)

        # Event handlers for push buttons
        self.btnAddEvent.clicked.connect(self.add_event)
        self.btnEditEvent.clicked.connect(self.edit_event_dialog)
        self.btnDeleteEvent.clicked.connect(self.delete_event)
        self.btnExit.clicked.connect(self.close)

        self.populate_event_list()

    def add_event(self):
        """Add a new event to the event list widget"""
        self.new_event = self.ledNewEvent.text().lower().strip(" ")

        # If passes validation, will insert text input into the database
        error_message = self.validate_new_event()
        if error_message:
            message_box_critical(error_message)
            self.ledNewEvent.setStyleSheet(style_line_edit_error())
        else:
            query = QSqlQuery()
            query.prepare("INSERT INTO event ('event_name') VALUES (:event)")
            query.bindValue(":event", self.new_event)
            bOk = query.exec()
            if bOk:
                message_box_critical("Event added to the database.")

            # Repopulate list widget after the database has been updated.
            # Sorts the updated list. Clears line edit widget.
            self.populate_event_list()
            self.lstEvents.sortItems()
            self.ledNewEvent.setText("")

    def edit_event_dialog(self):
        """Creates a dialog box to rename a selected event"""
        error_message = self.validate_if_selected()

        if error_message:
            message_box_critical(error_message)
        else:
            original_event = self.lstEvents.selectedItems()[0].text()
            edit_dialog = DlgEditEvent(original_event)
            edit_dialog.show()
            edit_dialog.exec_()
            self.populate_event_list()

    def delete_event(self):
        """Delete selected event from the database"""
        error_message = self.validate_if_selected()

        if error_message:
            message_box_critical(error_message)
        else:
            self.selected_event = self.lstEvents.selectedItems()[0].text()
            self.question = message_box_question(f"Are you sure you want to delete the event: "
                                                 f"<b>{self.selected_event}</b>? This will remove the event "
                                                 f"from all patients that have this event.")
            self.question.btnAccept.clicked.connect(self.query_delete_event)
            self.question.show()
            self.question.exec()

            self.populate_event_list()

    def populate_event_list(self):
        """Populate the event list widget with events from the database"""
        self.lstEvents.clear()  # If not cleared, will show duplicate list widget items
        self.ledNewEvent.setStyleSheet("")

        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM event")
        if bOk:
            self.all_events = []
            while query.next():
                self.all_events.append((query.value('event_id'), query.value('event_name')))
                self.lstEvents.addItem(query.value('event_name'))

        self.lstEvents.sortItems()

    def validate_new_event(self):
        """Validate input for new event"""
        string_format = "^[\w() -]{2,}$"  # Allow words, spaces, hyphens, and parenthesis
        error_message = ""

        # Validate line edit widget
        if not re.match(string_format, self.new_event):
            error_message += "Event name can only contain words, spaces, hyphens, and parenthesis; must be " \
                             "at least 2 characters in length.\n"
        else:
            query = QSqlQuery()
            bOk = query.exec("SELECT event_id, event_name FROM event")
            if bOk:
                all_events = []
                while query.next():
                    all_events.append((query.value('event_id'), query.value('event_name')))

                # Check for duplicate entries
                for event in all_events:
                    if self.new_event == event[1]:
                        error_message += "This event already exists.\n"

        return error_message

    def validate_if_selected(self):
        """
        Check if the event list widget is empty. If not empty, will check if an item has been selected.
        Returns an error message, which is blank if validation passes.
        """
        error_message = ""

        if self.lstEvents.count() == 0:
            error_message += "There is no event to edit or delete.\n"

        try:
            bOk = self.lstEvents.selectedItems()[0]
        except IndexError:
            error_message += "No item selected to rename or delete."

        return error_message

    def query_delete_event(self):
        """
        Send a query to delete an event from the database
        Must delete from both 'event' and 'patient_event' tables
        """
        query = QSqlQuery()
        query.prepare("DELETE FROM event WHERE event_name = :name")
        query.bindValue(":name", self.selected_event)
        bOk = query.exec()
        if bOk:
            for event in self.all_events:
                if self.selected_event == event[1]:
                    event_id = event[0]

            query = QSqlQuery()
            query.prepare("DELETE from patient_event WHERE event_id = :id")
            query.bindValue(":id", event_id)
            bOk = query.exec()
            if bOk:
                message_box_critical(f"The event: <b>{self.selected_event}</b> has been deleted.")
                self.question.close()