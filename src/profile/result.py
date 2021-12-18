import re
from decimal import Decimal
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog
from src.ui.add_update_result import Ui_DlgAddResult
from src.style import style_line_edit_error
from src.message_boxes.format_msg import message_box_critical


class DlgAddUpdateResult(QDialog, Ui_DlgAddResult):
    """Dialog window for adding or updating INR results"""
    def __init__(self, patient_id, inr_id=None):
        super(DlgAddUpdateResult, self).__init__()
        self.setupUi(self)

        self.mrn = patient_id  # The patient_id for use in query
        self.inr_id = inr_id  # The inr_id for use in query. For updating purposes.
        self.dteDate.setDate(QDate.currentDate())  # Set current date as the default for the date object
        self.ledResult.setFocus()
        self.gbxNewGoal.setHidden(True)

        # Set default option for radio button
        self.patient_inr_goal_from, self.patient_inr_goal_to = self.query_get_patient_inr_goal()
        self.rbtnGoalDefault.setText(f"Default: {self.patient_inr_goal_from} - {self.patient_inr_goal_to}")

        # Set the value for each daily dose's line edit widgets to 0
        self.set_daily_doses_to_zero()

        # Calculates the total dose when line edit widget text has been edited
        self.ledMonday.textEdited.connect(self.calculate_weekly_dose)
        self.ledTuesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledWednesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledThursday.textEdited.connect(self.calculate_weekly_dose)
        self.ledFriday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSaturday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSunday.textEdited.connect(self.calculate_weekly_dose)

        # Event handlers for input widgets
        self.chkNoChanges.clicked.connect(self.no_changes_to_dose)
        self.rbtnGoalNew.clicked.connect(self.set_new_goal)
        self.rbtnGoalDefault.clicked.connect(self.set_same_goal)
        self.btnOK.clicked.connect(self.add_result)
        self.btnCancel.clicked.connect(self.close)

    def add_result(self):
        """Add new result entry into the database"""
        error_message = self.validate_entry()

        if error_message:
            message_box_critical(error_message)
        else:
            sql_command = """
            INSERT INTO inr (patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, dose_sat, 
            dose_sun, comment, inr_goal_from, inr_goal_to) 
            VALUES (:id, :date, :result, :mon, :tue, :wed, :thu, :fri, :sat, :sun, :com, :goal_from, :goal_to)
            """
            query = self.query_inr_table_prepare_and_bind_query(sql_command)
            bOk = query.exec()
            if bOk:
                message_box_critical("Result added to the database.")
                self.close()
            else:
                message_box_critical("Could not save results into the database.")

    def update_result(self):
        """Update a selected result entry in the database"""
        error_message = self.validate_entry()

        if error_message:
            message_box_critical(error_message)
        else:
            sql_command = """
            UPDATE inr SET patient_id = :id, date = :date, result = :result, dose_mon = :mon, dose_tue = :tue, 
            dose_wed = :wed, dose_thu = :thu, dose_fri = :fri, dose_sat = :sat, dose_sun = :sun, comment = :com,
            inr_goal_from = :goal_from, inr_goal_to = :goal_to WHERE inr_id = :inr_id
            """
            query = self.query_inr_table_prepare_and_bind_query(sql_command)
            query.bindValue(":inr_id", int(self.inr_id))
            bOk = query.exec()
            if bOk:
                message_box_critical("Record updated.")
                self.close()
            else:
                message_box_critical("Not able to update record.")

    def no_changes_to_dose(self, chk):
        """
        Provide different effects if the checkbox is checked, or unchecked.
        If checked: change daily doses to read-only and will fill their values to match the previous entry
        If unchecked: allow for editing of daily doses and set values to a default of 0
        """
        if chk:
            # Set line edit widgets for daily doses to read-only
            self.ledMonday.setReadOnly(True)
            self.ledTuesday.setReadOnly(True)
            self.ledWednesday.setReadOnly(True)
            self.ledThursday.setReadOnly(True)
            self.ledFriday.setReadOnly(True)
            self.ledSaturday.setReadOnly(True)
            self.ledSunday.setReadOnly(True)

            # Populate the daily doses with the same values as the previous entry
            query = QSqlQuery()
            query.prepare("SELECT * FROM inr WHERE patient_id = :id ORDER BY date DESC, inr_id DESC LIMIT 1")
            query.bindValue(":id", self.mrn)
            bOk = query.exec()
            if bOk:
                query.next()
                if query.isValid():
                    self.ledMonday.setText(query.value('dose_mon'))
                    self.ledTuesday.setText(query.value('dose_tue'))
                    self.ledWednesday.setText(query.value('dose_wed'))
                    self.ledThursday.setText(query.value('dose_thu'))
                    self.ledFriday.setText(query.value('dose_fri'))
                    self.ledSaturday.setText(query.value('dose_sat'))
                    self.ledSunday.setText(query.value('dose_sun'))
                    self.calculate_weekly_dose()
                else:
                    message_box_critical("No previous doses detected on record.")
                    self.chkNoChanges.setChecked(False)
                    self.set_read_only_false()
        else:
            self.set_read_only_false()
            self.set_daily_doses_to_zero()

    def set_new_goal(self):
        """Reveal widgets for entering a new INR goal when the associated radio button is selected."""
        self.gbxNewGoal.setHidden(False)

    def set_same_goal(self):
        """Hide widgets for entering a new INR goal when the default radio button is selected"""
        self.gbxNewGoal.setHidden(True)

    def set_read_only_false(self):
        """Set the line edit widgets for the daily doses to be editable"""
        self.ledMonday.setReadOnly(False)
        self.ledTuesday.setReadOnly(False)
        self.ledWednesday.setReadOnly(False)
        self.ledThursday.setReadOnly(False)
        self.ledFriday.setReadOnly(False)
        self.ledSaturday.setReadOnly(False)
        self.ledSunday.setReadOnly(False)

    def set_daily_doses_to_zero(self):
        """Set the line edit widgets for the daily doses to be a value of 0"""
        self.ledMonday.setText("0")
        self.ledTuesday.setText("0")
        self.ledWednesday.setText("0")
        self.ledThursday.setText("0")
        self.ledFriday.setText("0")
        self.ledSaturday.setText("0")
        self.ledSunday.setText("0")
        self.ledTotal.setText("")
        self.ledNewGoalTo.setText("0")
        self.ledNewGoalFrom.setText("0")

    def calculate_weekly_dose(self):
        """
        Calculates the total dose of warfarin, and displays this value in a line edit widget.
        Uses the Decimal module to prevent floating point error during calculations.
        """
        try:
            self.ledTotal.setText(str(
                Decimal(self.ledMonday.text()) +
                Decimal(self.ledTuesday.text()) +
                Decimal(self.ledWednesday.text()) +
                Decimal(self.ledThursday.text()) +
                Decimal(self.ledFriday.text()) +
                Decimal(self.ledSaturday.text()) +
                Decimal(self.ledSunday.text())
            ))
        except:
            self.ledTotal.setText("")

    def validate_entry(self):
        """Validate user input and returns an error message. Error message is blank if all input passed validation."""
        error_message = ""
        format_string ="^[0-9]\d*(\.\d+)?$"  # Only positive integers and decimal numbers

        # Reset style sheet for line edit widgets
        self.ledMonday.setStyleSheet("")
        self.ledTuesday.setStyleSheet("")
        self.ledWednesday.setStyleSheet("")
        self.ledThursday.setStyleSheet("")
        self.ledFriday.setStyleSheet("")
        self.ledSaturday.setStyleSheet("")
        self.ledSunday.setStyleSheet("")
        self.ledNewGoalFrom.setStyleSheet("")
        self.ledNewGoalTo.setStyleSheet("")

        # Validate line edit widget for result
        if self.ledResult.text() == "":
            error_message += "INR result cannot be blank.\n"
            self.ledResult.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string, self.ledResult.text()):
            error_message += "Invalid format for INR result. Please enter a result that is a positive integer " \
                             "or decimal number.\n"
            self.ledResult.setStyleSheet(style_line_edit_error())

        # Validate line edit widgets for daily doses
        daily_dose = [("Monday", self.ledMonday.text()),
                      ("Tuesday", self.ledTuesday.text()),
                      ("Wednesday", self.ledWednesday.text()),
                      ("Thursday", self.ledThursday.text()),
                      ("Friday", self.ledFriday.text()),
                      ("Saturday", self.ledSaturday.text()),
                      ("Sunday", self.ledSunday.text())]

        for day in daily_dose:
            if day[1] == "":
                error_message += f"{day[0]}'s dose cannot be blank. Dose must be at least 0 or higher.\n"
                command = f"self.led{day[0]}.setStyleSheet(style_line_edit_error())"
                eval(command)

            elif not re.match(format_string, day[1]):
                error_message += f"{day[0]}'s dose is not a valid format. Please enter a positive integer or " \
                                 f"decimal number.\n"
                command = f"self.led{day[0]}.setStyleSheet(style_line_edit_error())"
                eval(command)

        # Validate new INR goal
        if self.rbtnGoalNew.isChecked():
            if self.ledNewGoalFrom.text() == "" or self.ledNewGoalFrom.text() == "0":
                error_message += "New INR goal cannot be blank or 0.\n"
                self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())
            elif not re.match(format_string, self.ledNewGoalFrom.text()):
                error_message += "Invalid format for INR goal. Please enter a result that is a positive integer " \
                                 "or decimal number.\n"
                self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())
            elif self.ledNewGoalTo.text() == "" or self.ledNewGoalTo.text() == "0":
                error_message += "New INR goal cannot be blank or 0.\n"
                self.ledNewGoalTo.setStyleSheet(style_line_edit_error())
            elif not re.match(format_string, self.ledNewGoalTo.text()):
                error_message += "Invalid format for INR goal. Please enter a result that is a positive integer " \
                                 "or decimal number.\n"
                self.ledNewGoalTo.setStyleSheet(style_line_edit_error())
            elif Decimal(self.ledNewGoalFrom.text()) >= Decimal(self.ledNewGoalTo.text()):
                error_message += "The INR range is not valid.\n"
            else:
                self.new_inr_goal_from = "{:.1f}".format(Decimal(self.ledNewGoalFrom.text()))
                self.new_inr_goal_to = "{:.1f}".format(Decimal(self.ledNewGoalTo.text()))

                patient_inr_goal_from, patient_inr_goal_to = self.query_get_patient_inr_goal()

                if self.new_inr_goal_from == str(patient_inr_goal_from) and \
                        self.new_inr_goal_to == str(patient_inr_goal_to):
                    error_message += "The new INR goal matches the current INR goal for the patient.\n"
                    self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())
                    self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())

        return error_message

    def query_inr_table_prepare_and_bind_query(self, sql_command):
        """Prepares and bind values to a query associated with the inr table"""
        query = QSqlQuery()
        query.prepare(sql_command)
        query.bindValue(":id", self.mrn)
        query.bindValue(":date", self.dteDate.date().toString("yyyy-MM-dd"))
        # format to 2 decimal places for formatting consistency
        query.bindValue(":result", "{:.2f}".format(Decimal(self.ledResult.text())))
        query.bindValue(":mon", "{:.2f}".format(Decimal(self.ledMonday.text())))
        query.bindValue(":tue", "{:.2f}".format(Decimal(self.ledTuesday.text())))
        query.bindValue(":wed", "{:.2f}".format(Decimal(self.ledWednesday.text())))
        query.bindValue(":thu", "{:.2f}".format(Decimal(self.ledThursday.text())))
        query.bindValue(":fri", "{:.2f}".format(Decimal(self.ledFriday.text())))
        query.bindValue(":sat", "{:.2f}".format(Decimal(self.ledSaturday.text())))
        query.bindValue(":sun", "{:.2f}".format(Decimal(self.ledSunday.text())))

        if self.rbtnGoalNew.isChecked():
            query.bindValue(":goal_from", self.new_inr_goal_from)
            query.bindValue(":goal_to", self.new_inr_goal_to)
        if self.rbtnGoalDefault.isChecked():
            query.bindValue(":goal_from", self.patient_inr_goal_from)
            query.bindValue(":goal_to", self.patient_inr_goal_to)

        query.bindValue(":com", self.txtComment.toPlainText())
        return query

    def query_get_patient_inr_goal(self):
        """Return the patient-set INR goal from the patient table"""
        query = QSqlQuery()
        query.prepare("SELECT inr_goal_from, inr_goal_to FROM patient WHERE patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            query.next()
            patient_inr_goal_from = query.value('inr_goal_from')
            patient_inr_goal_to = query.value('inr_goal_to')

        return patient_inr_goal_from, patient_inr_goal_to