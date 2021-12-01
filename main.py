import sys
import re
from decimal import Decimal
import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *
from gui.patientprofile import *
from gui.add_update_result import *
from gui.newpatient import *


class DlgMain(QMainWindow, Ui_dlgMain):
    """
    Main window for application
    """

    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # event handlers
        self.actionExit.triggered.connect(self.evt_action_exit_triggered)
        self.btnSearch.clicked.connect(self.evt_btn_search_clicked)

    def evt_btn_search_clicked(self):
        """
        Creates database connection when the search button is clicked
        """
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("database.db")
        if self.database.open():
            self.search_patient()
        else:
            QMessageBox.critical(self, "Database Error", "Could not connect with the database.")

    def search_patient(self):
        """
        Find a match in the database with the provided MRN. Will show message boxes for errors.
        """
        self.mrn = self.ledMRN.text()
        if self.ledMRN.text() == "":
            QMessageBox.critical(self, "No MRN Entered", "Please enter a medical record number.")
        else:
            query = QSqlQuery()
            query.prepare("SELECT patient_id FROM patient WHERE patient_id = (:id)")
            query.bindValue(":id", self.mrn)
            query.exec_()
            query.next()

            if query.isValid():
                dlgPatientProfile = DlgPatientProfile(self.mrn)
                dlgPatientProfile.show()
                dlgPatientProfile.exec_()

            else:
                QMessageBox.critical(self, "No Match Found", "The medical record number entered into the search "
                                                             "box does not match an existing record in the database.")

        self.ledMRN.clear()  # clear text box after searching

    def evt_action_exit_triggered(self):
        """
        Exit the program when user clicks on File > Exit
        """
        sys.exit(app.exec_())


class DlgPatientProfile(QDialog, Ui_DlgProfile):
    """Dialog box for patient profile"""
    def __init__(self, id):
        super(DlgPatientProfile, self).__init__()
        self.setupUi(self)

        # Result table formatting
        self.tblResult.setAlternatingRowColors(True)
        self.tblResult.setColumnWidth(2, 50)
        self.tblResult.setColumnWidth(3, 60)
        self.tblResult.setColumnWidth(4, 80)
        self.tblResult.horizontalHeader().setStretchLastSection(True)
        self.tblResult.setSortingEnabled(True)
        self.tblResult.setSelectionBehavior(QtWidgets.QTableWidget.SelectItems)
        self.tblResult.setSelectionMode(1)  # single selection mode
        self.tblResult.selectionModel().selectionChanged.connect(self.display_comment_column)

        # Populate patient data
        self.mrn = id
        self.populate_patient_summary(self.mrn)
        self.populate_result_table()

        # Event handlers
        self.tblResult.itemDoubleClicked.connect(self.evt_btn_edit_result_clicked)
        self.btnAdd.clicked.connect(self.evt_btn_add_result_clicked)
        self.btnEdit.clicked.connect(self.evt_btn_edit_result_clicked)
        self.btnDelete.clicked.connect(self.evt_btn_delete_result_clicked)
        self.btnEditPatient.clicked.connect(self.evt_btn_edit_patient_clicked)

    def populate_patient_summary(self, id):
        """
        Populate information in the summary tab in the patient profile
        :param id:  the medical record number for patient
        """
        self.list_patient_indications = []
        bOk, query = self.query_get_patient_summary_info(id)
        if bOk:
            while query.next():
                if query.isValid():
                    self.list_patient_summary_info = ([query.value('fname'), query.value('lname'), query.value('dob'),
                                                       query.value('status'), query.value('inr_goal_from'),
                                                       query.value('inr_goal_to'), query.value('indication_name'),
                                                       query.value('status')])
                    self.list_patient_indications.append(self.list_patient_summary_info[6])  # create a list if multiple indications

            self.ledFirstName.setText(self.list_patient_summary_info[0])
            self.ledLastName.setText(self.list_patient_summary_info[1])
            self.ledDOB.setText(self.list_patient_summary_info[2])
            self.ledIndications.setText(', '.join(self.list_patient_indications))
            self.ledGoal.setText(f"{self.list_patient_summary_info[4]} - {self.list_patient_summary_info[5]}")
            self.lblName.setText(f"{self.list_patient_summary_info[1]}, {self.list_patient_summary_info[0]}")
            if self.list_patient_summary_info[7] == "A":
                self.ledStatus.setText("Active")
            else:
                self.ledStatus.setText("Inactive")

    def query_get_patient_summary_info(self, id):
        """
        Prepares and executes a query search for patient information joining of multiple tables
        :param id: patient_id from patient database
        :return bOk, query: True or False if the query executed correctly, and the query itself
        """
        query = QSqlQuery()
        query.prepare("SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to, indication_name FROM patient p "
                      "JOIN patient_indication pi ON p.patient_id = pi.patient_id "
                      "JOIN indication i ON pi.indication_id = i.indication_id WHERE p.patient_id = :id")
        query.bindValue(":id", id)
        bOk = query.exec()
        return bOk, query

    def populate_result_table(self):
        """Populates the result table widget with information from the database"""
        self.tblResult.clearContents()  # clears the table content of old information before populating with newer data
        self.tblResult.setRowCount(0)  # resets row count

        query = QSqlQuery()
        query.prepare("SELECT inr_id, date, result, (i.inr_goal_from || '-' || i.inr_goal_to) AS goal, "
                      "(dose_mon + dose_tue + dose_wed + dose_thu + dose_fri + dose_sat + dose_sun) AS total_dose, "
                      "comment FROM inr i JOIN patient p ON  p.patient_id = i.patient_id "
                      "WHERE p.patient_id = :id ORDER BY date DESC")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                row = self.tblResult.rowCount()
                self.tblResult.insertRow(row)
                for col in range(6):
                    tbl_row_value = QTableWidgetItem(str(query.value(col)))
                    self.tblResult.setItem(row, col, tbl_row_value)

                    if col == 2:
                        tbl_result_col_value = QTableWidgetItem(str(query.value(col)))

                    if col == 3:
                        tbl_goal_col_value = QTableWidgetItem(str(query.value(col))).text()
                        inr_low = tbl_goal_col_value.split("-")[0].strip(" ")
                        inr_high = tbl_goal_col_value.split("-")[1].strip(" ")

                self.format_weekly_dose_col(inr_high, inr_low, row, tbl_result_col_value)

        self.tblResult.setColumnHidden(0, True)  # hide inr_id column from view
        self.tblResult.setCurrentCell(0, 1)  # set default selection

    def format_weekly_dose_col(self, inr_high, inr_low, row, tbl_result_col_value):
        """
        Will provide formatting of the table widget item's background color based on the result: red for
        supratherapeutic, yellow for subtherapeutic and green for therapeutic
        :param inr_high: the upper limit of INR goal
        :param inr_low: the lower limit of INR goal
        :param row: current row count
        :param tbl_result_col_value: the result value
        """
        if tbl_result_col_value.text() > inr_high:
            self.tblResult.item(row, 2).setBackground(QColor("#ff3300"))
        elif tbl_result_col_value.text() < inr_low:
            self.tblResult.item(row, 2).setBackground(QColor("#ffff00"))
        else:
            self.tblResult.item(row, 2).setBackground(QColor("#00ff80"))

    def evt_btn_add_result_clicked(self):
        """Creates a dialog box to add results to the database, and refreshes the result table"""
        dlgAddResult = DlgAddResult(self.mrn)
        dlgAddResult.btnOK.clicked.connect(dlgAddResult.evt_btn_ok_clicked)
        dlgAddResult.show()
        dlgAddResult.exec_()
        self.populate_result_table()

    def evt_btn_edit_result_clicked(self):
        """Creates a dialog box to update results to the database."""
        try:
            self.get_current_row_and_inr_id()
        except AttributeError:
            QMessageBox.critical(self, "Error", "No entries to edit.")
            return

        dlgEditResult = DlgAddResult(self.mrn, self.current_selection_inr_id)
        dlgEditResult.setWindowTitle("Edit Result")
        dlgEditResult.btnOK.setText("Update")

        # Retrieves query for the selected row
        query = self.return_selected_result_row()
        query.next()

        # Gets the QDate object for the original date
        original_date = query.value('date').split("-")
        original_year = int(original_date[0])
        original_month = int(original_date[1])
        original_day = int(original_date[2])
        original_date_object = QDate(original_year, original_month, original_day)

        # Gets the INR goals specified for the patient, and for the specific INR result
        inr_goal_from = query.value('inr_goal_from')
        inr_goal_to = query.value('inr_goal_to')
        patient_inr_goal_from, patient_inr_goal_to = dlgEditResult.query_get_patient_inr_goal()

        # Toggles INR goal radio buttons based on the INR goal retrieved
        if patient_inr_goal_from != query.value('inr_goal_from') and patient_inr_goal_to != query.value('inr_goal_to'):
            dlgEditResult.rbtnGoal_New.setChecked(True)
            dlgEditResult.evt_rbtn_new_goal_clicked()
            dlgEditResult.ledNewGoalFrom.setText(inr_goal_from)
            dlgEditResult.ledNewGoalTo.setText(inr_goal_to)

        # Sets line edit box to the values of the selected row
        dlgEditResult.dteDate.setDate(original_date_object)
        dlgEditResult.ledResult.setText(query.value('result'))
        dlgEditResult.ledMonday.setText(query.value('dose_mon'))
        dlgEditResult.ledTuesday.setText(query.value('dose_tue'))
        dlgEditResult.ledWednesday.setText(query.value('dose_wed'))
        dlgEditResult.ledThursday.setText(query.value('dose_thu'))
        dlgEditResult.ledFriday.setText(query.value('dose_fri'))
        dlgEditResult.ledSaturday.setText(query.value('dose_sat'))
        dlgEditResult.ledSunday.setText(query.value('dose_sun'))
        dlgEditResult.calculate_weekly_dose()
        dlgEditResult.txtComment.setPlainText(query.value('comment'))

        # Event handler
        dlgEditResult.btnOK.clicked.connect(dlgEditResult.evt_btn_update_result_clicked)

        dlgEditResult.show()
        dlgEditResult.exec_()
        self.populate_result_table()

    def get_current_row_and_inr_id(self):
        """Stores the current row index and the inr_id of the current selection"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_inr_id = self.tblResult.item(self.current_selection_row, 0).text()

    def evt_btn_delete_result_clicked(self):
        """Delete record from the table and database"""
        try:
            self.get_current_row_and_inr_id()
        except AttributeError:
            QMessageBox.critical(self, "Error", "No entries to delete.")
            return

        double_check_msg = QMessageBox.question(self, "Delete Result",
                             f"You have selected row {self.current_selection_row + 1} to be deleted.")
        if double_check_msg == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM inr WHERE inr_id = :id")
            query.bindValue(":id", self.current_selection_inr_id)
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Record deleted")
        self.populate_result_table()

    def evt_btn_edit_patient_clicked(self):
        """Opens a dialog box to edit patient information"""

        # Updates list of indications to pass to edit patient dialog box
        self.list_patient_indications = []
        query = QSqlQuery()
        query.prepare("SELECT indication_name FROM patient p JOIN patient_indication pi "
                      "ON p.patient_id = pi.patient_id JOIN indication i ON pi.indication_id = i.indication_id "
                      "WHERE p.patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                self.list_patient_indications.append(query.value('indication_name'))

        dlgEditPatient = DlgNewPatient(self.mrn, self.list_patient_indications)
        dlgEditPatient.setWindowTitle("Edit Patient Information")
        dlgEditPatient.lblHeader.setText("Update Information")
        dlgEditPatient.populate_indication_list()
        bOk, query = self.query_get_patient_summary_info(self.mrn)
        if bOk:
            while query.next():
                if query.isValid():
                    self.list_patient_summary_info = ([query.value('fname'), query.value('lname'), query.value('dob'),
                                                       query.value('status'), query.value('inr_goal_from'),
                                                       query.value('inr_goal_to'), query.value('indication_name'),
                                                       query.value('status')])

                    dlgEditPatient.ledMRN.setText(self.mrn)
                    dlgEditPatient.ledFirstName.setText(self.list_patient_summary_info[0])
                    dlgEditPatient.ledLastName.setText(self.list_patient_summary_info[1])
                    dlgEditPatient.ledDOB.setText(self.list_patient_summary_info[2])
                    dlgEditPatient.ledGoalFrom.setText(str(self.list_patient_summary_info[4]))
                    dlgEditPatient.ledGoalTo.setText(str(self.list_patient_summary_info[5]))

        dlgEditPatient.show()
        dlgEditPatient.exec_()
        self.populate_patient_summary(self.mrn)

    def return_selected_result_row(self):
        """Returns the database query for the selected table"""
        query = QSqlQuery()
        query.prepare("SELECT inr_id, patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, "
                      "dose_sat, dose_sun, comment, inr_goal_from, inr_goal_to from inr WHERE inr_id = :id")
        query.bindValue(":id", self.current_selection_inr_id)
        bOk = query.exec()
        if bOk:
            return query

    def display_comment_column(self, selected):
        """Display a message box containing any filled comment column selected"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_comment = self.tblResult.item(self.current_selection_row, 5).text()

        for i in selected.indexes():
            if i.column() == 5 and self.current_selection_comment:
                QMessageBox.information(self, "Comment", self.current_selection_comment)

    def weekly_dose_change_format(self):
        """Bold the weekly dose column when there are changes from the previous row"""
        self.total_rows = self.tblResult.rowCount()
        for row in range(self.total_rows - 1):
            self.current_weekly_dose = self.tblResult.item(row, 4)
            self.next_weekly_dose = self.tblResult.item(row+1, 4)

            if self.current_weekly_dose.text() != self.next_weekly_dose.text():
                font = QtGui.QFont()
                font.setBold(True)
                self.current_weekly_dose.setFont(font)
                self.current_weekly_dose.setForeground(QBrush(QColor("blue")))


class DlgAddResult(QDialog, Ui_DlgAddResult):
    """Dialog box for adding INR result to database"""
    def __init__(self, patient_id, inr_id=None):
        """
        :param patient_id: patient_id of current patient
        :param inr_id: inr_id of currently selected row
        """
        super(DlgAddResult, self).__init__()
        self.setupUi(self)
        self.mrn = patient_id  # patient MRN for use in query
        self.inr_id = inr_id  # inr_id for the selected result
        self.dteDate.setDate(QDate.currentDate())
        self.ledResult.setFocus()
        self.gbxNewGoal.setHidden(True)

        self.patient_inr_goal_from, self.patient_inr_goal_to = self.query_get_patient_inr_goal()
        self.rbtn_Goal_Default.setText(f"Default: {self.patient_inr_goal_from} - {self.patient_inr_goal_to}")

        # set default values for line edit boxes
        self.set_default_values()

        # signal for text change in doses
        self.ledMonday.textEdited.connect(self.calculate_weekly_dose)
        self.ledTuesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledWednesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledThursday.textEdited.connect(self.calculate_weekly_dose)
        self.ledFriday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSaturday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSunday.textEdited.connect(self.calculate_weekly_dose)

        # signal for buttons
        self.chkNoChanges.clicked.connect(self.evt_chkbox_no_changes_clicked)
        self.btnCancel.clicked.connect(self.close)
        self.rbtnGoal_New.clicked.connect(self.evt_rbtn_new_goal_clicked)
        self.rbtn_Goal_Default.clicked.connect(self.evt_rbtn_default_goal_clicked)

    def evt_btn_ok_clicked(self):
        """Insert data into the INR table if no error message is returned"""
        error_message = self.validate_entry_format()

        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            sql_command = """
            INSERT INTO inr (patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, dose_sat, 
            dose_sun, comment, inr_goal_from, inr_goal_to) 
            VALUES (:id, :date, :result, :mon, :tue, :wed, :thu, :fri, :sat, :sun, :com, :goal_from, :goal_to)
            """
            query = self.inr_table_prepare_bind_query(sql_command)
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Result added to the database.")
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Could not save results into the database.")

    def evt_btn_update_result_clicked(self):
        """Update result entry based on the selected table row"""
        error_message = self.validate_entry_format()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            sql_command = """
            UPDATE inr SET patient_id = :id, date = :date, result = :result, dose_mon = :mon, dose_tue = :tue, 
            dose_wed = :wed, dose_thu = :thu, dose_fri = :fri, dose_sat = :sat, dose_sun = :sun, comment = :com,
            inr_goal_from = :goal_from, inr_goal_to = :goal_to WHERE inr_id = :inr_id
            """
            query = self.inr_table_prepare_bind_query(sql_command)
            query.bindValue(":inr_id", int(self.inr_id))
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Record updated.")
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Not able to update record.")

    def evt_chkbox_no_changes_clicked(self, chk):
        """
        If check box state is True, then will make line edit boxes read-only and populate with previous doses.
        If check box state is False, will revert read-only setting and populate line edits with "0".
        Will return a message box if no prior entries in the database.
        :param chk: True or False if the checkbox for "No Changes" is selected or not
        """
        if chk:
            # set line edit boxes for daily doses to read only
            self.ledMonday.setReadOnly(True)
            self.ledTuesday.setReadOnly(True)
            self.ledWednesday.setReadOnly(True)
            self.ledThursday.setReadOnly(True)
            self.ledFriday.setReadOnly(True)
            self.ledSaturday.setReadOnly(True)
            self.ledSunday.setReadOnly(True)

            # populate line edit boxes for daily doses
            query = QSqlQuery()
            query.prepare("SELECT * FROM inr WHERE patient_id = :id ORDER BY date, inr_id DESC LIMIT 1")
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
                    QMessageBox.critical(self, "Error", "No previous doses detected on record.")
                    self.chkNoChanges.setChecked(False)
                    self.set_read_only_false()
        else:
            self.set_read_only_false()
            self.set_default_values()

    def set_read_only_false(self):
        """Set line edit boxes for daily doses to editable"""
        self.ledMonday.setReadOnly(False)
        self.ledTuesday.setReadOnly(False)
        self.ledWednesday.setReadOnly(False)
        self.ledThursday.setReadOnly(False)
        self.ledFriday.setReadOnly(False)
        self.ledSaturday.setReadOnly(False)
        self.ledSunday.setReadOnly(False)

    def calculate_weekly_dose(self):
        """Calculates the total dose of warfarin, and displays in line edit box"""
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

    def set_default_values(self):
        """Sets the line edit box texts to '0'"""
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

    def validate_entry_format(self):
        """Returns an error message based on validation. Error message will be blank if no errors."""
        error_message = ""

        # reset style sheet for line edit boxes
        self.ledMonday.setStyleSheet("")
        self.ledTuesday.setStyleSheet("")
        self.ledWednesday.setStyleSheet("")
        self.ledThursday.setStyleSheet("")
        self.ledFriday.setStyleSheet("")
        self.ledSaturday.setStyleSheet("")
        self.ledSunday.setStyleSheet("")
        self.ledNewGoalFrom.setStyleSheet("")
        self.ledNewGoalTo.setStyleSheet("")

        daily_dose = [("Monday", self.ledMonday.text()),
                      ("Tuesday", self.ledTuesday.text()),
                      ("Wednesday", self.ledWednesday.text()),
                      ("Thursday", self.ledThursday.text()),
                      ("Friday", self.ledFriday.text()),
                      ("Saturday", self.ledSaturday.text()),
                      ("Sunday", self.ledSunday.text())]

        format_string ="^[0-9]\d*(\.\d+)?$"  # only positive integers and decimal numbers

        if self.ledResult.text() == "":
            error_message += "INR result cannot be blank.\n"
            self.ledResult.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string, self.ledResult.text()):
            error_message += "Invalid format for INR result. Please enter a result that is a positive integer " \
                             "or decimal number.\n"
            self.ledResult.setStyleSheet(style_line_edit_error())

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

        if self.rbtnGoal_New.isChecked():
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

                if self.new_inr_goal_from == str(patient_inr_goal_from) and self.new_inr_goal_to == str(patient_inr_goal_to):
                    error_message += "The new INR goal matches the current INR goal for the patient.\n"
                    self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())
                    self.ledNewGoalFrom.setStyleSheet(style_line_edit_error())

        return error_message

    def query_get_patient_inr_goal(self):
        """Return the patient's inr goal from the patient table"""
        query = QSqlQuery()
        query.prepare("SELECT inr_goal_from, inr_goal_to FROM patient WHERE patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            query.next()
            patient_inr_goal_from = query.value('inr_goal_from')
            patient_inr_goal_to = query.value('inr_goal_to')
        return patient_inr_goal_from, patient_inr_goal_to

    def inr_table_prepare_bind_query(self, sql_command):
        """
        Returns the executed query to insert data into the inr table
        :param sql_command: sql statement to be executed
        :return: the executed query
        """
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

        if self.rbtnGoal_New.isChecked():
            query.bindValue(":goal_from", self.new_inr_goal_from)
            query.bindValue(":goal_to", self.new_inr_goal_to)
        if self.rbtn_Goal_Default.isChecked():
            query.bindValue(":goal_from", self.patient_inr_goal_from)
            query.bindValue(":goal_to", self.patient_inr_goal_to)

        query.bindValue(":com", self.txtComment.toPlainText())
        return query

    def evt_rbtn_new_goal_clicked(self):
        """Reveals the groupbox for new INR goal entry when the 'new goal' radio button is clicked"""
        self.gbxNewGoal.setHidden(False)

    def evt_rbtn_default_goal_clicked(self):
        """Hides the groupbox for new INR goal entry when the 'default' radio button is clicked"""
        self.gbxNewGoal.setHidden(True)


class DlgNewPatient(QDialog, Ui_DlgNewPatient):
    """Dialog box for adding new patients"""
    def __init__(self, id, patient_indications):  # each new instance, the indication list reverts back to the original
        super(DlgNewPatient, self).__init__()
        self.setupUi(self)
        self.mrn = id
        self.indications = patient_indications
        self.ledMRN.setReadOnly(True)
        self.populate_indication_list()

        # Signals
        self.btnAddIndication.clicked.connect(self.evt_btn_add_patient_indication_clicked)
        self.btnRemoveIndication.clicked.connect(self.evt_btn_remove_patient_indication_clicked)
        self.btnNewIndication.clicked.connect(self.evt_btn_new_indication_clicked)
        self.buttonBox.accepted.connect(self.evt_btn_ok_clicked)
        self.buttonBox.rejected.connect(self.close)

    def populate_indication_list(self):
        """Populate list widgets for patient indications and database indications"""

        self.lstPatientIndications.clear()
        self.lstExistingIndications.clear()

        # Populate the patient indication list box from patient table
        self.lstPatientIndications.addItems(self.indications)

        self.lstPatientIndications.sortItems()
        # Populate the indication list box from the indication table
        bOk, query = self.query_get_all_indications()
        if bOk:
            while query.next():
                if query.value('indication_name') not in self.indications:
                    self.lstExistingIndications.addItem(query.value('indication_name'))
        self.lstExistingIndications.sortItems()

    def query_get_all_indications(self):
        """Retrieves all indication ids and names from the indication table"""
        query = QSqlQuery()
        bOk = query.exec("SELECT indication_id, indication_name FROM indication")
        return bOk, query

    def evt_btn_add_patient_indication_clicked(self):
        """Move list item from indication list widget to patient indication list widget"""
        selected_row = self.lstExistingIndications.row(self.lstExistingIndications.currentItem())
        selected_item = self.lstExistingIndications.takeItem(selected_row)
        self.lstPatientIndications.addItem(selected_item)
        self.lstPatientIndications.sortItems()

    def evt_btn_remove_patient_indication_clicked(self):
        """Move list item from patient indication list widget to indication list widget"""
        selected_row = self.lstPatientIndications.row(self.lstPatientIndications.currentItem())
        selected_item = self.lstPatientIndications.takeItem(selected_row)
        self.lstExistingIndications.addItem(selected_item)
        self.lstExistingIndications.sortItems()

    def evt_btn_new_indication_clicked(self):
        """Add new indication to database"""
        self.new_indication = self.ledNewIndication.text()
        error_message = self.validate_new_indication()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
            self.ledNewIndication.setStyleSheet(style_line_edit_error())
        else:
            query = QSqlQuery()
            query.prepare("INSERT INTO indication ('indication_name') VALUES (:ind)")
            query.bindValue(":ind", self.new_indication.lower().strip(" "))
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Indication added to the database.")
            self.populate_indication_list()
            self.ledNewIndication.setText("")

    def evt_btn_ok_clicked(self):
        """Update patient and patient_indication tables"""
        error_message = self.validate_patient_information()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            query = QSqlQuery()
            query.prepare("UPDATE patient SET fname = :fname, lname = :lname, status = :status, "
                          "inr_goal_from = :inr_goal_from, inr_goal_to = :inr_goal_to, dob = :dob "
                          "WHERE patient_id = :id")

            query.bindValue(":fname", self.ledFirstName.text().title())
            query.bindValue(":lname", self.ledLastName.text().title())
            query.bindValue(":dob", self.ledDOB.text())
            if self.rbtnStatusActive.isChecked():
                query.bindValue(":status", "A")
            else:
                query.bindValue(":status", "I")
            query.bindValue(":inr_goal_from", self.ledGoalFrom.text())
            query.bindValue(":inr_goal_to", self.ledGoalTo.text())
            query.bindValue(":id", self.mrn)
            query.exec()

            # List of patient indication names
            num_of_patient_indications = self.lstPatientIndications.count()

            self.indications = []
            for row in range(num_of_patient_indications):
                list_widget_item = self.lstPatientIndications.item(row)
                self.indications.append(list_widget_item.text())

            # List of patient indication ids
            patient_indication_id = []
            bOk, query = self.query_get_all_indications()
            if bOk:
                while query.next():
                    if query.value('indication_name') in self.indications:
                        patient_indication_id.append(query.value('indication_id'))

            # Clear all rows from patient_indication corresponding to patient_id
            query = QSqlQuery()
            query.prepare("DELETE FROM patient_indication WHERE patient_id = :id")
            query.bindValue(":id", self.mrn)
            query.exec()

            for id in patient_indication_id:
                query = QSqlQuery()
                query.prepare("INSERT INTO patient_indication (indication_id, patient_id) "
                              "VALUES (:indication_id, :patient_id)")
                query.bindValue(":indication_id", id)
                query.bindValue(":patient_id", self.mrn)
                query.exec()

            QMessageBox.information(self, "Success", "Patient profile has been updated.")
            self.close()

    def validate_patient_information(self):
        error_message = ""
        format_string_name = "[\w+\-]+$"
        format_string_birthdate = "\d{4}-\d{2}-\d{2}"
        format_string_inr_goal = "^[0-9]\d*(\.\d+)?$"

        self.ledFirstName.setStyleSheet("")
        self.ledLastName.setStyleSheet("")
        self.ledDOB.setStyleSheet("")
        self.ledGoalFrom.setStyleSheet("")
        self.ledGoalTo.setStyleSheet("")

        # Test first name
        if self.ledFirstName.text() == "":
            error_message += "First name cannot be blank.\n"
            self.ledFirstName.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_name, self.ledFirstName.text()):
            error_message += "First name can only contain letters and hyphens.\n"
            self.ledFirstName.setStyleSheet(style_line_edit_error())

        # Test last name
        if self.ledLastName.text() == "":
            error_message += "Last name cannot be blank.\n"
            self.ledLastName.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_name, self.ledLastName.text()):
            error_message += "Last name can only contain letters and hyphens.\n"
            self.ledLastName.setStyleSheet(style_line_edit_error())

        # Test date of birth
        if self.ledDOB.text() == "":
            error_message += "Date of birth cannot be blank.\n"
            self.ledDOB.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_birthdate, self.ledDOB.text()):
            error_message += "Date of birth must be in the format of YYYY-MM-DD.\n"
            self.ledDOB.setStyleSheet(style_line_edit_error())
        else:
            birthdate = list(map(int, self.ledDOB.text().split("-")))
            try:
                test_birthdate = datetime.datetime(birthdate[0], birthdate[1], birthdate[2])
            except ValueError:
                error_message += "Invalid birthdate.\n"
                self.ledDOB.setStyleSheet(style_line_edit_error())

        # Test indication
        if self.lstPatientIndications.count() == 0:
            error_message += "Patient must have at least one indication.\n"

        # Test INR goal
        if self.ledGoalFrom.text() == "" or self.ledGoalFrom.text() == "0":
            error_message += "INR goal cannot be blank or 0.\n"
            self.ledGoalFrom.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_inr_goal, self.ledGoalFrom.text()):
            error_message += "Invalid format for INR goal. Please enter a result that is a positive integer " \
                             "or decimal number.\n"
            self.ledGoalFrom.setStyleSheet(style_line_edit_error())

        if self.ledGoalTo.text() == "" or self.ledGoalTo.text() == "0":
            error_message += "New INR goal cannot be blank or 0.\n"
            self.ledGoalTo.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_inr_goal, self.ledGoalTo.text()):
            error_message += "Invalid format for INR goal. Please enter a result that is a positive integer " \
                             "or decimal number.\n"
            self.ledGoalTo.setStyleSheet(style_line_edit_error())
        else:
            if Decimal(self.ledGoalFrom.text()) >= Decimal(self.ledGoalTo.text()):
                error_message += "The INR range is not valid.\n"
                self.ledGoalFrom.setStyleSheet(style_line_edit_error())
                self.ledGoalTo.setStyleSheet(style_line_edit_error())

        return error_message

    def validate_new_indication(self):
        """Validates line edit box for new indication"""
        string_format = "^[\w() -]{2,}$"  # only allow words, spaces, hyphens, and parenthesis
        error_message = ""

        if not re.match(string_format, self.new_indication):
            error_message += "Indication name can only contain words, spaces, hyphens, and parenthesis.\n"

        if len(self.new_indication) <= 2:
            error_message += "Indication name must contain more than two characters.\n"

        # Create a list of tuples of indication ids and names from the indication table
        bOk, query = self.query_get_all_indications()
        if bOk:
            all_indications = []
            while query.next():
                all_indications.append((query.value('indication_id'), query.value('indication_name')))

            for indication in all_indications:
                if self.new_indication == indication[1]:
                    error_message += "This indication already exists.\n"

        return error_message


def style_line_edit_error():
    """
    A style sheet used to show line edit boxes with invalid entries
    :return: style sheet for a line edit box with a red border
    """
    sStyle = """
        QLineEdit {
            border: 1px solid red;
        }
    """

    return sStyle


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
