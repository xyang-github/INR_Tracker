import re
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog
from src.ui.editevent import Ui_DlgEditEvent
from src.message_boxes.format_msg import message_box_critical


class DlgEditEvent(QDialog, Ui_DlgEditEvent):
    """Dialog window for editing/renaming an item from the event list widget"""
    def __init__(self, original_event):
        super(DlgEditEvent, self).__init__()
        self.setupUi(self)

        # Populate the line edit widget with the name of the selected list widget item
        self.original_event = original_event
        self.ledEvent.setText(self.original_event)

        # Event handlers for push buttons
        self.btnOk.clicked.connect(self.change_event)
        self.btnExit.clicked.connect(self.close)

    def change_event(self):
        """Update the list widget item and the database"""
        self.new_event = self.ledEvent.text().lower()
        error_message = self.validate_new_event()

        if error_message:
            message_box_critical(error_message)
        else:
            query = QSqlQuery()
            query.prepare("UPDATE event SET event_name = :new_name WHERE event_name = :orig_name")
            query.bindValue(":new_name", self.new_event)
            query.bindValue(":orig_name", self.original_event)
            bOk = query.exec()
            if bOk:
                message_box_critical(f"The event for <b>{self.original_event}</b> "
                                     f"has been renamed to <b>{self.new_event}</b>.")
                self.close()

    def validate_new_event(self):
        """Validate input for new event and return an error_message"""
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
