import sys
import re
from decimal import Decimal

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *
from gui.patientprofile import *
from gui.add_update_result import *


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
    """
    Dialog box for patient profile
    """

    def __init__(self, id):
        super(DlgPatientProfile, self).__init__()
        self.setupUi(self)

        # Populate patient data
        self.mrn = id
        self.populate_patient_summary(self.mrn)
        self.populate_result_table()

        # Event handlers
        self.btnAdd.clicked.connect(self.evt_btn_add_result_clicked)

    def populate_patient_summary(self, id):
        """
        Populate information in the summary tab in the patient profile
        :param id:  the medical record number for patient
        """
        query = QSqlQuery()
        bOk = query.exec(
            "SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to, indication_name FROM patient p JOIN patient_indication pi ON p.patient_id = pi.patient_id JOIN indication i ON pi.indication_id = i.indication_id WHERE p.patient_id = {}".format(
                id))
        if bOk:
            query.next()
            if query.isValid():
                self.lst_patient_summary_info = ([query.value('fname'), query.value('lname'), query.value('dob'),
                                                  query.value('status'), query.value('inr_goal_from'),
                                                  query.value('inr_goal_to'), query.value('indication_name')])

                self.ledFirstName.setText(self.lst_patient_summary_info[0])
                self.ledLastName.setText(self.lst_patient_summary_info[1])
                self.ledDOB.setText(self.lst_patient_summary_info[2])
                self.ledIndications.setText(self.lst_patient_summary_info[6])
                self.ledGoal.setText(f"{self.lst_patient_summary_info[4]} - {self.lst_patient_summary_info[5]}")
                self.lblName.setText(f"{self.lst_patient_summary_info[1]}, {self.lst_patient_summary_info[0]}")

    def populate_result_table(self):
        """
        Populates the table widget with information from the database
        """
        self.tblResult.clearContents()
        self.tblResult.setRowCount(0)

        query = QSqlQuery()
        query.prepare("SELECT date, result, (inr_goal_from || '-' || inr_goal_to) AS goal, "
                      "(dose_mon + dose_tue + dose_wed + dose_thu + dose_fri + dose_sat + dose_sun) AS total_dose, "
                      "comment FROM inr i JOIN patient p ON  p.patient_id = i.patient_id "
                      "WHERE p.patient_id = :id ORDER BY date DESC")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                row = self.tblResult.rowCount()
                self.tblResult.insertRow(row)
                for col in range(5):
                    tbl_result_col_value = QTableWidgetItem(str(query.value(col)))
                    self.tblResult.setItem(row, col, tbl_result_col_value)

    def evt_btn_add_result_clicked(self):
        dlgAddResult = DlgAddResult(self.mrn)
        dlgAddResult.show()
        dlgAddResult.exec_()
        self.populate_result_table()


class DlgAddResult(QDialog, Ui_DlgAddResult):
    """
    Dialog box for adding INR result to database
    """

    def __init__(self, id):
        super(DlgAddResult, self).__init__()
        self.setupUi(self)
        self.mrn = id  # patient MRN for use in query
        self.dteDate.setDate(QDate.currentDate())
        self.ledResult.setFocus()

        # set default values for doses
        self.set_default_values()

        # signal for text change in doses
        self.ledMonday.textEdited.connect(self.evt_text_changed)
        self.ledTuesday.textEdited.connect(self.evt_text_changed)
        self.ledWednesday.textEdited.connect(self.evt_text_changed)
        self.ledThursday.textEdited.connect(self.evt_text_changed)
        self.ledFriday.textEdited.connect(self.evt_text_changed)
        self.ledSaturday.textEdited.connect(self.evt_text_changed)
        self.ledSunday.textEdited.connect(self.evt_text_changed)

        # signal for buttons
        self.chkNoChanges.clicked.connect(self.evt_chkbox_no_changes_clicked)
        self.btnOK.clicked.connect(self.evt_btn_ok_clicked)
        self.btnCancel.clicked.connect(self.evt_btn_close_clicked)

    def evt_btn_ok_clicked(self):
        """
        Insert data into the INR table if no error message is returned
        """
        error_message = self.validate_entry()

        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            sql_command = """
            INSERT INTO inr (patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, dose_sat, 
            dose_sun, comment) VALUES (:id, :date, :result, :mon, :tue, :wed, :thu, :fri, :sat, :sun, :com)
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
            query.bindValue(":com", self.txtComment.toPlainText())
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Result added to the database.")
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Could not save results into the database.")

    def evt_btn_close_clicked(self):
        """
        Close dialog box for adding/updating results
        """
        self.close()

    def evt_chkbox_no_changes_clicked(self, chk):
        """
        If check box state is True, then will make line edit boxes read-only and populate with previous doses.
        If check box state is False, will revert read-only setting and populate line edits with "0".
        Will return a message box if no prior entries in the database.
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
            bOk = query.exec(
                f"SELECT * FROM patient JOIN inr ON patient.patient_id = inr.patient_id WHERE patient.patient_id = {self.mrn} ORDER BY date DESC LIMIT 1")
            if bOk:
                query.next()
                if query.isValid():
                    self.ledMonday.setText(query.value('dose_mon'))  # DOES NOT WORK YET
                    self.ledTuesday.setText(query.value('dose_tue'))
                    self.ledWednesday.setText(query.value('dose_wed'))
                    self.ledThursday.setText(query.value('dose_thu'))
                    self.ledFriday.setText(query.value('dose_fri'))
                    self.ledSaturday.setText(query.value('dose_sat'))
                    self.ledSunday.setText(query.value('dose_sun'))
                else:
                    QMessageBox.critical(self, "Error", "No previous doses detected on record.")
                    self.chkNoChanges.setChecked(False)
        else:
            self.ledMonday.setReadOnly(False)
            self.ledTuesday.setReadOnly(False)
            self.ledWednesday.setReadOnly(False)
            self.ledThursday.setReadOnly(False)
            self.ledFriday.setReadOnly(False)
            self.ledSaturday.setReadOnly(False)
            self.ledSunday.setReadOnly(False)
            self.set_default_values()

    def evt_text_changed(self):
        """
        Calculates the total dose of warfarin, and displays in line edit box
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

    def set_default_values(self):
        """
        Sets the line edit box texts to "0"
        """
        self.ledMonday.setText("0")
        self.ledTuesday.setText("0")
        self.ledWednesday.setText("0")
        self.ledThursday.setText("0")
        self.ledFriday.setText("0")
        self.ledSaturday.setText("0")
        self.ledSunday.setText("0")

    def validate_entry(self):
        """
        Returns an error message based on validation. Error message will be blank if no errors.
        """
        error_message = ""

        # reset style sheet for line edit boxes
        self.ledMonday.setStyleSheet("")
        self.ledTuesday.setStyleSheet("")
        self.ledWednesday.setStyleSheet("")
        self.ledThursday.setStyleSheet("")
        self.ledFriday.setStyleSheet("")
        self.ledSaturday.setStyleSheet("")
        self.ledSunday.setStyleSheet("")

        daily_dose = [("Monday", self.ledMonday.text()),
                      ("Tuesday", self.ledTuesday.text()),
                      ("Wednesday", self.ledWednesday.text()),
                      ("Thursday", self.ledThursday.text()),
                      ("Friday", self.ledFriday.text()),
                      ("Saturday", self.ledSaturday.text()),
                      ("Sunday", self.ledSunday.text())]

        format_string = "^[0-9]\d*(\.\d+)?$"  # only positive integers and decimal numbers

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
