import sys
import re
from decimal import Decimal
import datetime
import csv

import dateutil
from dateutil.relativedelta import relativedelta
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor, QBrush, QPainter, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from gui.main_ui import *
from gui.patientprofile import *
from gui.add_update_result import *
from gui.newpatient import *
from gui.indications import *
from gui.editindication import *
from gui.report import *


class DlgMain(QMainWindow, Ui_dlgMain):
    """Main window for application"""
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # Establish a connection to the database
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("data/inr_tracker.db")
        if self.database.open():
            if "indication" not in self.database.tables():
                self.create_indication_table()
            if "inr" not in self.database.tables():
                self.create_inr_table()
            if "patient" not in self.database.tables():
                self.create_patient_table()
            if "patient_indication" not in self.database.tables():
                self.create_patient_indication_table()
        else:
            QMessageBox.critical(self, "Database Error", "Could not connect with the database.")

        # event handlers
        self.actionExit.triggered.connect(self.evt_action_exit_triggered)
        self.btnSearch.clicked.connect(self.evt_btn_search_clicked)
        self.btnNewPatient.clicked.connect(self.evt_btn_new_patient_clicked)
        self.btnIndications.clicked.connect(self.evt_btn_indications_clicked)
        self.btnReports.clicked.connect(self.evt_btn_reports_clicked)

    def evt_btn_search_clicked(self):
        """Searches for a matching patient_id in the patient table"""
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

    def evt_btn_new_patient_clicked(self):

        dlgNewPatient = DlgNewUpdatePatient()
        dlgNewPatient.rbtnStatusInactive.setEnabled(False)
        dlgNewPatient.show()
        dlgNewPatient.exec_()
        dlgNewPatient.populate_indication_list()

    def evt_btn_indications_clicked(self):
        dlgIndications = DlgIndications()
        dlgIndications.show()
        dlgIndications.exec_()

    def evt_btn_reports_clicked(self):
        """Opens a dialog box for the clinic report"""

        html = self.get_html()

        dlgReport = DlgReport()
        dlgReport.tedReport.setHtml(html)
        dlgReport.show()
        dlgReport.exec_()

    def get_html(self):
        """Create an HTML string to format the clinic report"""

        # Retrieve total number of active patients
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) AS total FROM patient WHERE status = :status")
        query.bindValue(":status", "A")
        query.exec()
        query.next()
        total_actives = query.value('total')
        # Retrieve total number of inactive patients
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) AS total FROM patient WHERE status = :status")
        query.bindValue(":status", "I")
        query.exec()
        query.next()
        total_inactives = query.value('total')
        # Retrieve total number of patients
        query = QSqlQuery()
        query.exec("SELECT COUNT(*) AS total FROM patient")
        query.next()
        total_all_patients = query.value('total')
        html = f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style = "background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">Patient Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td><strong>Total Patients:</strong></td>
                    <td>{total_all_patients}</td>
                </tr>
                <tr>
                    <td><strong>Active Patients:</strong></td>
                    <td>{total_actives}</td>
                </tr>
                <tr>
                    <td><strong>Inactive Patients:</strong></td>
                    <td>{total_inactives}</td>
                </tr>
            </table>
        </div>
        &nbsp;<br>
        """
        # Retrieve total number of indications
        query = QSqlQuery()
        query.exec("SELECT COUNT(*) AS total FROM indication")
        query.next()
        total_indications = query.value('total')
        # Retrieve breakdown of indications
        list_indications = []
        query = QSqlQuery()
        query.exec("SELECT COUNT(i.indication_id) AS total, indication_name FROM indication i "
                   "JOIN patient_indication pi ON i.indication_id = pi.indication_id GROUP BY indication_name "
                   "ORDER BY indication_name DESC")
        while query.next():
            list_indications.append((query.value('indication_name'), query.value('total')))
        list_indications.sort()
        html += f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style = "background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">Indication Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td style="width: 150px"><strong>Total Indications:</strong></td>
                    <td>{total_indications}</th>
                </tr>
        """
        for indication in list_indications:
            html += f"""
            <tr>
                <td>{indication[0]}</td>
                <td>{indication[1]}</td>
            </tr>
            """
        html += """
            </table>
        </div>
        &nbsp;<br>
        """
        # Retrieve total number of goals
        query = QSqlQuery()
        query.exec("SELECT COUNT(DISTINCT inr_goal_from || '-' || inr_goal_to) AS total from patient")
        query.next()
        total_goals = query.value('total')
        # Retrieve breakdown of INR goals
        list_goals = []
        query = QSqlQuery()
        query.exec("SELECT COUNT(inr_goal_from || '-' || inr_goal_to) AS total, (inr_goal_from || '-' || inr_goal_to) "
                   "AS goal FROM patient GROUP BY goal")
        while query.next():
            list_goals.append((query.value('goal'), query.value('total')))
        list_goals.sort()
        html += f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style="background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">Goal Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td style="width: 150px"><strong>Total Goals:</strong></th>
                    <td>{total_goals}</th>
                </tr>
        """
        for goal in list_goals:
            html += f"""
                <tr>
                    <td>{goal[0]}</td>
                    <td>{goal[1]}</td>
                </tr>
            """
        html += """
            </table>
        </div>
        """
        return html

    def create_indication_table(self):
        """Create a table named 'indication' if not already in the database"""
        command = """
            CREATE TABLE IF NOT EXISTS "indication" (
                "indication_id"	INTEGER NOT NULL,
                "indication_name"	TEXT NOT NULL,
                PRIMARY KEY("indication_id")
            )
        """
        query = QSqlQuery()
        query.exec_(command)

    def create_inr_table(self):
        """Create a table named 'inr' if not already in the database"""
        command = """
            CREATE TABLE IF NOT EXISTS "inr" (
                "inr_id"	INTEGER NOT NULL,
                "patient_id"	INTEGER NOT NULL,
                "date"	TEXT,
                "result"	TEXT,
                "dose_mon"	TEXT,
                "dose_tue"	TEXT,
                "dose_wed"	TEXT,
                "dose_thu"	TEXT,
                "dose_fri"	TEXT,
                "dose_sat"	TEXT,
                "dose_sun"	TEXT,
                "comment"	TEXT,
                "inr_goal_from"	TEXT,
                "inr_goal_to"	TEXT,
                FOREIGN KEY("patient_id") REFERENCES "patient"("patient_id") on delete cascade,
                PRIMARY KEY("inr_id" AUTOINCREMENT))
        """
        query = QSqlQuery()
        query.exec_(command)

    def create_patient_table(self):
        """Create a table named 'patient' if not already in the database"""
        command = """
            CREATE TABLE IF NOT EXISTS "patient" (
                "patient_id"	INTEGER NOT NULL,
                "fname"	TEXT NOT NULL,
                "lname"	TEXT NOT NULL,
                "dob"	TEXT NOT NULL,
                "status"	TEXT NOT NULL,
                "inr_goal_from"	TEXT NOT NULL,
                "inr_goal_to"	TEXT NOT NULL,
                PRIMARY KEY("patient_id")
            )
        """
        query = QSqlQuery()
        query.exec_(command)

    def create_patient_indication_table(self):
        """Create a table named 'patient_indication' if not already in the database"""
        command = """
            CREATE TABLE IF NOT EXISTS "patient_indication" (
                "indication_id"	INTEGER NOT NULL,
                "patient_id"	INTEGER NOT NULL,
                FOREIGN KEY("patient_id") REFERENCES "patient"("patient_id") on delete cascade
            )
        """
        query = QSqlQuery()
        query.exec_(command)


class DlgIndications(QDialog, Ui_DlgIndications):
    def __init__(self):
        super(DlgIndications, self).__init__()
        self.setupUi(self)

        # Signal for buttons
        self.btnAdd.clicked.connect(self.evt_btn_add_clicked)
        self.btnEdit.clicked.connect(self.evt_btn_edit_clicked)
        self.btnDelete.clicked.connect(self.evt_btn_delete_clicked)
        self.btnExit.clicked.connect(self.close)

        self.populate_indication_list()

    def evt_btn_add_clicked(self):
        """Add a new indication to the indication list widget"""

        # Validate text input
        self.new_indication = self.ledNewIndication.text().lower().strip(" ")
        error_message = validate_new_indication(self.new_indication)
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
            self.ledNewIndication.setStyleSheet(style_line_edit_error())
        else:
            # Add text input into the indication table
            query = QSqlQuery()
            query.prepare("INSERT INTO indication ('indication_name') VALUES (:ind)")
            query.bindValue(":ind", self.new_indication)
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Indication added to the database.")

            # Repopulate and sort list widget. Clears line edit widget text.
            self.populate_indication_list()
            self.lstIndications.sortItems()
            self.ledNewIndication.setText("")

    def evt_btn_edit_clicked(self):
        """Opens a dialog box to rename a selected indication"""

        # Validate selection
        error_message = self.validate_if_selected()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            # Dialog box to rename the selected item
            original_indication = self.lstIndications.selectedItems()[0].text()
            edit_dialog = DlgEditIndication(original_indication)
            edit_dialog.show()
            edit_dialog.exec_()
            self.populate_indication_list()

    def evt_btn_delete_clicked(self):
        """Delete indication from indication table and patient_indication linking table"""

        # Validation on selection
        error_message = self.validate_if_selected()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            # Asking user for verification of deletion
            selected_indication = self.lstIndications.selectedItems()[0].text()
            double_check_msg = QMessageBox.question(self, "Delete indication?",
                                 f"Are you sure you want to delete the indication: {selected_indication}? "
                                 f"This will remove the indication from all patients that have this indication.")
            # Delete from indication table
            if double_check_msg == QMessageBox.Yes:
                query = QSqlQuery()
                query.prepare("DELETE FROM indication WHERE indication_name = :name")
                query.bindValue(":name", selected_indication)
                bOk = query.exec()
                if bOk:
                    # Delete from patient_indication table
                    for indication in self.all_indications:
                        if selected_indication == indication[1]:
                            indication_id = indication[0]

                    query = QSqlQuery()
                    query.prepare("DELETE from patient_indication WHERE indication_id = :id")
                    query.bindValue(":id", indication_id)
                    bOk = query.exec()
                    if bOk:
                        QMessageBox.information(self, "Success",
                                                f"The indication: {selected_indication} has been deleted.")
                        # Repopulate indication list widget
                        self.populate_indication_list()

    def validate_if_selected(self):
        """Validate if an item in the list widget exists or has been selected"""
        error_message = ""
        if self.lstIndications.count() == 0:
            error_message += "There is no indication to edit or delete.\n"
        try:
            bOk = self.lstIndications.selectedItems()[0]
        except IndexError:
            error_message += "No item selected to rename or delete."
        return error_message

    def populate_indication_list(self):
        """Populate the list widget with indications from the indication table"""
        self.lstIndications.clear()
        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM indication")
        if bOk:
            self.all_indications = []
            while query.next():
                self.all_indications.append((query.value('indication_id'), query.value('indication_name')))
                self.lstIndications.addItem(query.value('indication_name'))
        self.lstIndications.sortItems()


class DlgEditIndication(QDialog, Ui_DlgEditIndication):
    """Dialog box for renaming an indication"""
    def __init__(self, original_indication):
        super(DlgEditIndication, self).__init__()
        self.setupUi(self)
        self.original_indication = original_indication
        self.ledIndication.setText(self.original_indication)

        self.btnOk.clicked.connect(self.btn_ok_clicked)
        self.btnExit.clicked.connect(self.close)

    def btn_ok_clicked(self):
        """Rename the indication and updates the indication table with the new value"""
        new_indication = self.ledIndication.text().lower()
        error_message = validate_new_indication(new_indication)
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            query = QSqlQuery()
            query.prepare("UPDATE indication SET indication_name = :new_name WHERE indication_name = :orig_name")
            query.bindValue(":new_name", new_indication)
            query.bindValue(":orig_name", self.original_indication)
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", f"The indication for {self.original_indication} has been renamed to {new_indication}.")
                self.close()


class DlgPatientProfile(QDialog, Ui_DlgProfile):
    """Dialog box for patient profile"""
    def __init__(self, id):
        super(DlgPatientProfile, self).__init__()
        self.number_of_results_in_range = 0
        self.setupUi(self)
        self.mrn = id

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
        self.populate_patient_summary()

        # Warns if no indication on record, and disables buttons associated with the result table widget
        if self.ledIndications.text() == "No Indication On Record":
            QMessageBox.warning(self, "Warning", "There is no indication on record for this patient. "
                                                 "Please add an indication in order to add, edit or delete any "
                                                 "further results.")
            self.btnAdd.setDisabled(True)
            self.btnEdit.setDisabled(True)
            self.btnDelete.setDisabled(True)
        else:
            self.btnAdd.setDisabled(False)
            self.btnEdit.setDisabled(False)
            self.btnDelete.setDisabled(False)

        self.populate_result_table()

        # Event handlers
        self.tblResult.itemDoubleClicked.connect(self.evt_btn_edit_result_clicked)
        self.btnAdd.clicked.connect(self.evt_btn_add_result_clicked)
        self.btnEdit.clicked.connect(self.evt_btn_edit_result_clicked)
        self.btnDelete.clicked.connect(self.evt_btn_delete_result_clicked)
        self.btnEditPatient.clicked.connect(self.evt_btn_edit_patient_clicked)
        self.btnExit.clicked.connect(self.close)
        self.btnAnalytics.clicked.connect(self.evt_btn_analytics_clicked)
        self.btnCSV.clicked.connect(self.evt_btn_csv_clicked)
        self.btnPDF.clicked.connect(self.evt_btn_pdf_clicked)

    def evt_btn_add_result_clicked(self):
        """Slot: creates a dialog box to add new INR results"""
        dlgAddResult = DlgAddUpdateResult(self.mrn)
        dlgAddResult.btnOK.clicked.connect(dlgAddResult.evt_btn_ok_clicked)
        dlgAddResult.show()
        dlgAddResult.exec_()
        self.populate_result_table()  # update the result table widget after adding a new value into the database

    def evt_btn_edit_result_clicked(self):
        """
        Creates a dialog box to update results to the database.
        1. Retrieve the row value and INR id of the selected row in the table widget
        2. Send a query using the row id and row value to retrieve information from patient table
        3. From the query, create a date object and patient-set INR goal
        4. Populate line edit widgets with values directly from the query, date object and patient-set INR
        """
        try:
            self.get_current_row_and_inr_id()
        except AttributeError:
            QMessageBox.critical(self, "Error", "No entries to edit.")
            return

        dlgEditResult = DlgAddUpdateResult(self.mrn, self.current_selection_inr_id)
        dlgEditResult.setWindowTitle("Edit Result")
        dlgEditResult.btnOK.setText("Update")

        query = self.query_get_inr_information()
        query.next()

        # Get the QDate object for date associated with the result
        original_date = query.value('date').split("-")
        original_year = int(original_date[0])
        original_month = int(original_date[1])
        original_day = int(original_date[2])
        original_date_object = QDate(original_year, original_month, original_day)

        # Get the patient-set INR goal and the result-set INR goal
        inr_goal_from = query.value('inr_goal_from')
        inr_goal_to = query.value('inr_goal_to')
        patient_inr_goal_from, patient_inr_goal_to = dlgEditResult.query_get_patient_inr_goal()

        # Toggles radio buttons for default or new INR goal
        if patient_inr_goal_from != query.value('inr_goal_from') and patient_inr_goal_to != query.value('inr_goal_to'):
            dlgEditResult.rbtnGoal_New.setChecked(True)
            dlgEditResult.evt_rbtn_new_goal_clicked()
            dlgEditResult.ledNewGoalFrom.setText(inr_goal_from)
            dlgEditResult.ledNewGoalTo.setText(inr_goal_to)

        # Sets the text for the line edit widgets
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

    def evt_btn_delete_result_clicked(self):
        """
        Delete record from the table and database
        1. Get row index and inr id of the selected row in the result table widget
        2. Verifies user's choice using a message box
        3. Send a query to delete all fields with the corresponding inr_id in the inr table
        4. Refresh result table widget
        """
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
        """
        Opens a dialog box to edit patient information
        1. Create/update a list of patient specific indication(s); this will be passed to the DlgNewPatient class to
            later prevent displaying of duplicate indications
        2. Create a dialog box to update patient information via the DlgNewPatient class
        3. Send a query to retrieve information from the patient table
        4. Store query information in a patient summary information list
        5. Populate update dialog box's line edit widgets with information from the patient summary information list
        6. Refresh patient summary tab with updated information
        """

        # Updates list of indications to pass to edit patient dialog box
        self.list_patient_indication_name = []
        query = QSqlQuery()
        query.prepare("SELECT indication_name FROM patient p JOIN patient_indication pi "
                      "ON p.patient_id = pi.patient_id JOIN indication i ON pi.indication_id = i.indication_id "
                      "WHERE p.patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                self.list_patient_indication_name.append(query.value('indication_name'))

        dlgEditPatient = DlgNewUpdatePatient(self.mrn, self.list_patient_indication_name)
        dlgEditPatient.setWindowTitle("Edit Patient Information")
        dlgEditPatient.lblHeader.setText("Update Information")
        dlgEditPatient.populate_indication_list()

        # Populate line edit widgets
        self.list_patient_summary_info, self.list_patient_indication_name = self.query_get_patient_summary_info()
        self.list_patient_indication_name.sort()
        dlgEditPatient.ledMRN.setText(self.mrn)
        dlgEditPatient.ledFirstName.setText(self.list_patient_summary_info[0])
        dlgEditPatient.ledLastName.setText(self.list_patient_summary_info[1])
        dlgEditPatient.ledDOB.setText(self.list_patient_summary_info[2])
        dlgEditPatient.ledGoalFrom.setText(str(self.list_patient_summary_info[4]))
        dlgEditPatient.ledGoalTo.setText(str(self.list_patient_summary_info[5]))

        dlgEditPatient.show()
        dlgEditPatient.exec_()
        self.populate_patient_summary()

    def evt_btn_analytics_clicked(self):
        """Calculates the TTR and opens a dialog box to display the results"""
        self.total_rows = self.tblResult.rowCount()
        self.total_days_in_ttr = 0
        self.total_days = 0

        for i in range(self.total_rows - 1):
            ttr = 0
            shift_in_ttr = 0
            calculate_ttr = "(shift_in_ttr / total_shift) * days_between_results"

            date1 = self.tblResult.item(i+1, 1).text().split("-")  # older date
            date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))

            date2 = self.tblResult.item(i, 1).text().split("-")  # newer date
            date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
            days_between_results = abs((date2 - date1).days)

            result1 = Decimal(self.tblResult.item(i+1, 2).text())  # older result
            result2 = Decimal(self.tblResult.item(i, 2).text())  # newer result
            total_shift = abs(result2 - result1)

            inr_goal = self.tblResult.item(i, 3).text().split("-")
            inr_goal_lower_limit = Decimal(inr_goal[0])
            inr_goal_upper_limit = Decimal(inr_goal[1])

            if result1 < inr_goal_lower_limit:
                if result2 < inr_goal_lower_limit:
                    ttr = 0
                elif result2 > inr_goal_upper_limit:
                    shift_in_ttr = (inr_goal_upper_limit - inr_goal_lower_limit)
                    ttr = eval(calculate_ttr)
                else:
                    shift_in_ttr = result2 - inr_goal_lower_limit
                    ttr = eval(calculate_ttr)
            elif result1 > inr_goal_upper_limit:
                if result2 < inr_goal_lower_limit:
                    shift_in_ttr = inr_goal_upper_limit - inr_goal_lower_limit
                    ttr = eval(calculate_ttr)
                elif result2 > inr_goal_upper_limit:
                    ttr = 0
                else:
                    shift_in_ttr = inr_goal_upper_limit - result2
                    ttr = eval(calculate_ttr)
            else:
                if result2 < inr_goal_lower_limit:
                    shift_in_ttr = result1 - inr_goal_lower_limit
                    ttr = eval(calculate_ttr)
                elif result2 > inr_goal_upper_limit:
                    shift_in_ttr = inr_goal_upper_limit - result1
                    ttr = eval(calculate_ttr)
                else:
                    ttr = days_between_results

            self.total_days_in_ttr += ttr
            self.total_days += days_between_results

        percent_ttr = self.total_days_in_ttr / self.total_days

        dlgAnalytics = DlgAnalytics(percent_ttr, self.total_days_in_ttr, self.total_days,
                                    self.total_rows, self.number_of_results_in_range)
        dlgAnalytics.show()
        dlgAnalytics.exec_()

    def evt_btn_csv_clicked(self):
        """Write data from the result table widget to a csv file"""
        column_header = []
        for col in range(1, self.tblResult.columnCount()):
            column_header.append(self.tblResult.horizontalHeaderItem(col).text())

        print(self.tblResult.horizontalHeaderItem(1).text())
        path = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        if path[0] != "":
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(column_header)
                for row in range(self.tblResult.rowCount()):
                    data = []
                    for col in range(1, self.tblResult.columnCount()):
                        item = self.tblResult.item(row, col).text()
                        data.append(item)
                    writer.writerow(data)

    def evt_btn_pdf_clicked(self):
        """Saves a summary chart in PDF format"""
        html = self.create_html()
        document = QTextDocument()
        document.setHtml(html)
        printer = QPrinter()
        document.print_(printer)

    def create_html(self):
        """Constructs an HTML string for PDF output"""
        html = f"""
        <div style="font-family: arial; text-align: center">
            <h1 style="align-self: center">Patient Anticoagulation Summary Report</h1>
            Medical Facility<br>
            Address<br>
            Phone Number | Fax Number
        </div>

        <hr>
        
        <div style="font-family: arial">
            <table style="border-style: solid; border-radius: 15px; width: 100%; padding: 10px; border-color: gray">
                <tr>
                    <td style="width: 100px"><strong>Patient Name:</strong></td>
                    <td>{self.list_patient_summary_info[1]}, {self.list_patient_summary_info[0]}</td>
                </tr>
                <tr>
                    <td><strong>Date of Birth:</strong></td>
                    <td>{self.list_patient_summary_info[2]}</td>
                </tr>
                <tr>
                    <td><strong>Indication(s):</strong></td>
                    <td>{', '.join(self.list_patient_indication_name)}</td>
                </tr>
                <tr>
                    <td><strong>INR Goal:</strong></td>
                    <td>{self.list_patient_summary_info[4]} - {self.list_patient_summary_info[5]}</td>
                </tr>
            </table>
        </div>
        """
        query = QSqlQuery()
        query.prepare("SELECT * FROM inr WHERE patient_id = :id ORDER BY date DESC LIMIT 1")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            query.next()
            if query.isValid():
                html += f"""
        &nbsp;<br>
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style = "margin-bottom: 0px">Most Recent Regimen</h3>
            <em>-Warfarin dose is in milligrams (mg)-</em>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Monday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Tuesday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Wednesday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Thursday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Friday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Saturday</th>
                    <th style="background-color: #04AA6D; color: white; text-align: center">Sunday</th>
                </tr>
                <tr>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_mon')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_tue')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_wed')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_thu')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_fri')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_sat')}</td>
                    <td style="background-color: gray; color: white; text-align: center">{query.value('dose_sun')}</td>
                </tr>
                </table>
            </div>

            &nbsp;<br>
            
            <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
                <h3 style="margin-bottom: 0px">Results</h3>
                <em>-Past 6 months displayed.</em>
            
                <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse; padding: 5px">
                    <tr>
                        <th style="background-color: #04AA6D; color: white; text-align: center">Date</th>
                        <th style="background-color: #04AA6D; color: white; text-align: center">INR</th>
                        <th style="background-color: #04AA6D; color: white; text-align: center">Goal</th>
                        <th style="background-color: #04AA6D; color: white; text-align: center">Total Dose</th>
                        <th style="background-color: #04AA6D; color: white; text-align: left">Comment</th>
                    </tr>
            """

        today = datetime.date.today()
        delta = dateutil.relativedelta.relativedelta(months=6)
        six_months_ago = today - delta

        query = QSqlQuery()
        query.prepare("SELECT * FROM inr WHERE date >= :past AND date <= :today AND patient_id = :id "
                      "ORDER BY date DESC")
        query.bindValue(":id", self.mrn)
        query.bindValue(":past", str(six_months_ago))
        query.bindValue(":today", str(today))
        bOk = query.exec()
        if bOk:
            while query.next():
                html += f"""
        <tr>
            <td style="background-color: gray; color: white; text-align: center">{query.value('date')}</td>
            <td style="background-color: gray; color: white; text-align: center">{query.value('result')}</td>
            <td style="background-color: gray; color: white; text-align: center">{query.value('inr_goal_from')} - {query.value('inr_goal_to')}</td>
            <td style="background-color: gray; color: white; text-align: center">
            {Decimal(query.value('dose_mon')) + 
            Decimal(query.value('dose_tue')) + 
            Decimal(query.value('dose_wed')) + 
            Decimal(query.value('dose_thu')) + 
            Decimal(query.value('dose_fri')) + 
            Decimal(query.value('dose_sat')) + 
            Decimal(query.value('dose_sun'))}</td>
            <td style="background-color: gray; color: white; text-align: center">{query.value('comment')}</td>
        </tr>
        """
            html += """
        </table>
        </div>
        """
        return html

    def populate_patient_summary(self):
        """
        Populate information in the summary tab in the patient profile
        1. Send a query to retrieve information from patient table
        2. Populate line edit widgets of the patient summary tab
        """
        self.list_patient_summary_info, self.list_patient_indication_name = self.query_get_patient_summary_info()
        self.list_patient_indication_name.sort()
        self.ledFirstName.setText(self.list_patient_summary_info[0])
        self.ledLastName.setText(self.list_patient_summary_info[1])
        self.ledDOB.setText(self.list_patient_summary_info[2])
        self.ledIndications.setText(', '.join(self.list_patient_indication_name))
        self.ledGoal.setText(f"{self.list_patient_summary_info[4]} - {self.list_patient_summary_info[5]}")
        self.lblName.setText(f"{self.list_patient_summary_info[1]}, {self.list_patient_summary_info[0]}")
        if self.list_patient_summary_info[7] == "A":
            self.ledStatus.setText("Active")
        else:
            self.ledStatus.setText("Inactive")

        self.check_status()

    def populate_result_table(self):
        """
        Populates the result table widget with information from the database
        1. Clear the result table widget and set row count to 0 to prevent duplicate entries after the database has been
            updated
        2. Send a query to the database to get information specific to table widget columns
        3. Populate the result table widget with information from the query
        4. Format the background color of the result column of the table widget
        5. Hide column 0, which contains the inr_id. Creates a default selection on the table widget.
        """
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

                self.format_result_col(row, tbl_result_col_value, inr_low, inr_high)
            self.format_weekly_dose()
            self.format_goal()

        self.tblResult.setColumnHidden(0, True)  # hide inr_id column from view
        self.tblResult.setCurrentCell(0, 1)  # set default selection

    def format_result_col(self, row, tbl_result_col_value, inr_low, inr_high):
        """
        Will provide formatting of the table widget item's background color based on the result: red for
        supratherapeutic, yellow for subtherapeutic and green for therapeutic
        """
        if tbl_result_col_value.text() > inr_high:
            self.tblResult.item(row, 2).setBackground(QColor("#ff3300"))
        elif tbl_result_col_value.text() < inr_low:
            self.tblResult.item(row, 2).setBackground(QColor("#ffff00"))
        else:
            self.tblResult.item(row, 2).setBackground(QColor("#00ff80"))
            self.number_of_results_in_range += 1

    def format_weekly_dose(self):
        """Bold and set color to the weekly dose column when there are changes from the previous row"""
        self.total_rows = self.tblResult.rowCount()
        for row in range(self.total_rows - 1):
            self.current_weekly_dose = self.tblResult.item(row, 4)
            self.next_weekly_dose = self.tblResult.item(row+1, 4)

            if self.current_weekly_dose.text() != self.next_weekly_dose.text():
                font = QtGui.QFont()
                font.setBold(True)
                self.current_weekly_dose.setFont(font)
                self.current_weekly_dose.setForeground(QBrush(QColor("blue")))

    def format_goal(self):
        """Bold and set color to the INR goal column when there are changes from the previous row"""
        self.total_rows = self.tblResult.rowCount()
        for row in range(self.total_rows - 1):
            self.current_inr_goal = self.tblResult.item(row, 3)
            self.next_inr_goal = self.tblResult.item(row+1, 3)

            if self.current_inr_goal.text() != self.next_inr_goal.text():
                font = QtGui.QFont()
                font.setBold(True)
                self.current_inr_goal.setFont(font)
                self.current_inr_goal.setForeground(QBrush(QColor("darkMagenta")))

    def get_current_row_and_inr_id(self):
        """Create variables that contain the row value and inr_id of the current selection in the result table widget"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_inr_id = self.tblResult.item(self.current_selection_row, 0).text()

    def display_comment_column(self, selected):
        """Display a message box containing any filled comment column selected"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_comment = self.tblResult.item(self.current_selection_row, 5).text()

        for i in selected.indexes():
            if i.column() == 5 and self.current_selection_comment:
                QMessageBox.information(self, "Comment", self.current_selection_comment)

    def check_status(self):
        # Disables ability to edit inr table widget for inactive patients
        if self.ledStatus.text() == "Inactive":
            self.btnAdd.setDisabled(True)
            self.btnEdit.setDisabled(True)
            self.btnDelete.setDisabled(True)
        else:
            self.btnAdd.setDisabled(False)
            self.btnEdit.setDisabled(False)
            self.btnDelete.setDisabled(False)

    def query_get_patient_summary_info(self):
        """Prepares and executes a query search for patient information joining of multiple tables"""
        self.list_patient_summary_info = []
        self.list_patient_indication_name = []

        # Check if patient has an indication on file
        query = QSqlQuery()
        query.prepare("SELECT patient_id, indication_id FROM patient_indication WHERE patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            query.next()
            if query.isValid():
                # Retrieve patient summary information
                query = QSqlQuery()
                query.prepare("SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to, indication_name "
                              "FROM patient p JOIN patient_indication pi ON p.patient_id = pi.patient_id "
                              "JOIN indication i ON pi.indication_id = i.indication_id WHERE p.patient_id = :id")
                query.bindValue(":id", self.mrn)
                bOk = query.exec()
                if bOk:
                    while query.next():
                        self.list_patient_summary_info = ([query.value('fname'), query.value('lname'), query.value('dob'),
                                                           query.value('status'), query.value('inr_goal_from'),
                                                           query.value('inr_goal_to'), query.value('indication_name'),
                                                           query.value('status')])
                        self.list_patient_indication_name.append(self.list_patient_summary_info[6])

                    return self.list_patient_summary_info, self.list_patient_indication_name

            else:
                # Will create an alternative query if there is no indication on record
                query = QSqlQuery()
                query.prepare(
                    "SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to FROM patient WHERE patient_id = :id")
                query.bindValue(":id", self.mrn)
                bOk = query.exec()
                if bOk:
                    query.next()
                    self.list_patient_summary_info = ([query.value('fname'), query.value('lname'), query.value('dob'),
                                                       query.value('status'), query.value('inr_goal_from'),
                                                       query.value('inr_goal_to'), "No Indication On Record",
                                                       query.value('status')])
                    self.list_patient_indication_name.append(self.list_patient_summary_info[6])

                return self.list_patient_summary_info, self.list_patient_indication_name

    def query_get_inr_information(self):
        """Sends a query to retrieve information from patient table"""
        query = QSqlQuery()
        query.prepare("SELECT inr_id, patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, "
                      "dose_sat, dose_sun, comment, inr_goal_from, inr_goal_to from inr WHERE inr_id = :id")
        query.bindValue(":id", self.current_selection_inr_id)
        bOk = query.exec()
        if bOk:
            return query


class DlgAddUpdateResult(QDialog, Ui_DlgAddResult):
    """Dialog box for adding INR result to database"""
    def __init__(self, patient_id, inr_id=None):
        """
        :param patient_id: patient_id of current patient
        :param inr_id: inr_id of currently selected row
        """
        super(DlgAddUpdateResult, self).__init__()
        self.setupUi(self)
        self.mrn = patient_id  # Patient MRN for use in query
        self.inr_id = inr_id  # inr_id for the selected result
        self.dteDate.setDate(QDate.currentDate())  # Set current date as the default for the date object
        self.ledResult.setFocus()
        self.gbxNewGoal.setHidden(True)

        # Set the text for the radio button for default INR goal
        self.patient_inr_goal_from, self.patient_inr_goal_to = self.query_get_patient_inr_goal()
        self.rbtn_Goal_Default.setText(f"Default: {self.patient_inr_goal_from} - {self.patient_inr_goal_to}")

        # set default values for line edit boxes
        self.set_daily_doses_to_zero()

        # Signal for text changes in line edit widgets for doses; calculate weekly dose
        self.ledMonday.textEdited.connect(self.calculate_weekly_dose)
        self.ledTuesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledWednesday.textEdited.connect(self.calculate_weekly_dose)
        self.ledThursday.textEdited.connect(self.calculate_weekly_dose)
        self.ledFriday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSaturday.textEdited.connect(self.calculate_weekly_dose)
        self.ledSunday.textEdited.connect(self.calculate_weekly_dose)

        # Signal for buttons
        self.chkNoChanges.clicked.connect(self.evt_chkbox_no_changes_clicked)
        self.btnCancel.clicked.connect(self.close)
        self.rbtnGoal_New.clicked.connect(self.evt_rbtn_new_goal_clicked)
        self.rbtn_Goal_Default.clicked.connect(self.evt_rbtn_default_goal_clicked)

    def evt_btn_ok_clicked(self):
        """
        Insert data into the INR table if no error message is returned
        1. Retrieve an error message from calling a validation function
        2. If error message is blank (passed validation), then send a query to insert information into the inr table
        """
        error_message = self.validate_entry()

        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            sql_command = """
            INSERT INTO inr (patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, dose_sat, 
            dose_sun, comment, inr_goal_from, inr_goal_to) 
            VALUES (:id, :date, :result, :mon, :tue, :wed, :thu, :fri, :sat, :sun, :com, :goal_from, :goal_to)
            """
            query = self.query_inr_table_prepare_and_bind_query(sql_command)
            bOk = query.exec()
            if bOk:
                QMessageBox.information(self, "Success", "Result added to the database.")
                self.close()
            else:
                print(query.lastError().text())
                QMessageBox.critical(self, "Error", "Could not save results into the database.")

    def evt_btn_update_result_clicked(self):
        """
        Update the result table
        1. Retrieve an error message from calling a validation function
        2. If error message is blank (passed validation), will send a query to update inr table
        """

        error_message = self.validate_entry()
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
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
                QMessageBox.information(self, "Success", "Record updated.")
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Not able to update record.")

    def evt_chkbox_no_changes_clicked(self, chk):
        """
        Affects the line edit widgets for the doses
        1. If the No Changes checkbox is checked, the line edit widgets for the doses will be changed to read-only, and
            be populated with the most recent doses in the inr table.
        2. If False, the read-only state will be changed to False, and the line edit widget text will be set to 0.
        3. Will return a message box if no prior entries in the database.
        :param chk: True if checkbox is checked; False if checkbox is not checked
        """
        if chk:
            # Set line edit boxes for daily doses to read only
            self.ledMonday.setReadOnly(True)
            self.ledTuesday.setReadOnly(True)
            self.ledWednesday.setReadOnly(True)
            self.ledThursday.setReadOnly(True)
            self.ledFriday.setReadOnly(True)
            self.ledSaturday.setReadOnly(True)
            self.ledSunday.setReadOnly(True)

            # Populate line edit boxes for daily doses
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
            self.set_daily_doses_to_zero()

    def evt_rbtn_new_goal_clicked(self):
        """Reveal widgets for entering a new INR goal when the associated radio button is selected."""
        self.gbxNewGoal.setHidden(False)

    def evt_rbtn_default_goal_clicked(self):
        """Hide widgets for entering a new INR goal when the default radio button is selected"""
        self.gbxNewGoal.setHidden(True)

    def set_read_only_false(self):
        """Set the read-only line edit boxes for doses to False"""
        self.ledMonday.setReadOnly(False)
        self.ledTuesday.setReadOnly(False)
        self.ledWednesday.setReadOnly(False)
        self.ledThursday.setReadOnly(False)
        self.ledFriday.setReadOnly(False)
        self.ledSaturday.setReadOnly(False)
        self.ledSunday.setReadOnly(False)

    def calculate_weekly_dose(self):
        """
        Calculates the total dose of warfarin, and displays in line edit box. Uses the Decimal module to prevent
        floating point error during calculations.
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

    def set_daily_doses_to_zero(self):
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

    def validate_entry(self):
        """
        Returns an error message based on validation. Error message will be blank if no errors.
        1. Reset style sheet for line edit widgets prior to validation
        2. Set validation for the line edit widget for the result
        3. Set validation for the line edit widgets for the daily doses
        4. Set validation for new INR goal entered
        """
        error_message = ""
        format_string ="^[0-9]\d*(\.\d+)?$"  # only positive integers and decimal numbers

        # Reset style sheet for line edit boxes
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

    def query_inr_table_prepare_and_bind_query(self, sql_command):
        """
        Prepares and bind values to a query associated with the inr table
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


class DlgNewUpdatePatient(QDialog, Ui_DlgNewPatient):
    """Dialog box for adding new patients"""
    def __init__(self, id=None, patient_indications=None):
        super(DlgNewUpdatePatient, self).__init__()
        self.setupUi(self)
        self.mrn = id
        self.list_of_patient_indications = patient_indications
        if self.mrn:
            self.ledMRN.setReadOnly(True)  # This is a primary key; should not be allowed to edit
        self.populate_indication_list()

        # Signals
        self.btnAddIndication.clicked.connect(self.evt_btn_add_patient_indication_clicked)
        self.btnRemoveIndication.clicked.connect(self.evt_btn_remove_patient_indication_clicked)
        self.btnNewIndication.clicked.connect(self.evt_btn_new_indication_clicked)
        self.buttonBox.accepted.connect(self.evt_btn_ok_clicked)
        self.buttonBox.rejected.connect(self.close)

    def evt_btn_add_patient_indication_clicked(self):
        """Move list widget item to patient-set indication list widget"""
        selected_row = self.lstExistingIndications.row(self.lstExistingIndications.currentItem())
        selected_item = self.lstExistingIndications.takeItem(selected_row)
        self.lstPatientIndications.addItem(selected_item)
        self.lstPatientIndications.sortItems()

    def evt_btn_remove_patient_indication_clicked(self):
        """Move list item widget to non-patient indication list widget"""
        selected_row = self.lstPatientIndications.row(self.lstPatientIndications.currentItem())
        selected_item = self.lstPatientIndications.takeItem(selected_row)
        self.lstExistingIndications.addItem(selected_item)
        self.lstExistingIndications.sortItems()

    def evt_btn_new_indication_clicked(self):
        """
        Add new indication to database
        1. Takes the text from the line edit widget for new indication, and passes it to a validation function
        2. If error message is blank (passes validation), a query will be sent to insert data into the indication table
            and also to the patient_indication linking table
        3. Repopulate indication list widget after database has been updated
        4. Clears the line edit widget for new indication
        """
        self.new_indication_name = self.ledNewIndication.text().lower().strip()
        error_message = validate_new_indication(self.new_indication_name)
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
            self.ledNewIndication.setStyleSheet(style_line_edit_error())
        else:
            # Insert input into indication table
            query = QSqlQuery()
            query.prepare("INSERT INTO indication ('indication_name') VALUES (:ind)")
            query.bindValue(":ind", self.new_indication_name)
            bOk = query.exec()
            if bOk:
                # Retrieve indication_id for new indication
                query = QSqlQuery()
                query.prepare("SELECT indication_id FROM indication WHERE indication_name = :ind")
                query.bindValue(":id", self.new_indication_name)
                bOk = query.exec()
                if bOk:
                    # Insert input into patient_indication linking table
                    new_indication_id = query.value('indication_id')
                    query = QSqlQuery()
                    query.prepare("INSERT INTO patient_indication (patient_id, indication_id) "
                                  "VALUES (:patient_id, :indication_id)")
                    query.bindValue(":patient_id", self.mrn)
                    query.bindValue(":indication_id", new_indication_id)
                    bOk = query.exec()
                    if bOk:
                        QMessageBox.information(self, "Success", "Indication added to the database.")
        self.populate_indication_list()
        self.ledNewIndication.setText("")

    def evt_btn_ok_clicked(self):
        """
        Add or update patient and patient_indication tables
        1. If error_message is blank (passes validation), perform various queries
        2. Query to update or insert data into the patient table
        3. If updating a patient, delete all records from the patient_indication table associated with the patient prior
            to inserting. If new patient, skip this step.
        4. Insert indication id and patient id in the patient_indication table
        """
        error_message = self.validate_patient_information()
        action = ""
        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            if self.lblHeader.text() != "New Patient":
                self.query_update_patient_table()
                action = "updated"
            else:
                self.query_insert_patient_table()
                action = "added"

            patient_indication_id = self.query_get_patient_indication_ids()
            self.query_update_patientindication_table(patient_indication_id)

            QMessageBox.information(self, "Success", f"Patient profile has been {action}.")
            self.close()

    def query_insert_patient_table(self):
        """For new patient, send a query to insert data to patient table"""
        query = QSqlQuery()
        query.prepare("INSERT INTO patient (patient_id, fname, lname, dob, status, inr_goal_from, inr_goal_to) "
                      "VALUES (:id, :fname, :lname, :dob, :status, :inr_goal_from, :inr_goal_to)")
        query.bindValue(":id", self.ledMRN.text())
        query.bindValue(":fname", self.ledFirstName.text().title())
        query.bindValue(":lname", self.ledLastName.text().title())
        query.bindValue(":dob", self.ledDOB.text())
        query.bindValue(":status", "A")
        query.bindValue(":inr_goal_from", "{:.1f}".format(Decimal(self.ledGoalFrom.text())))
        query.bindValue(":inr_goal_to", "{:.1f}".format(Decimal(self.ledGoalTo.text())))
        query.exec()

    def query_update_patientindication_table(self, patient_indication_id):
        """Updates the patient_indication table based on if new or updating profile"""

        # If updating patient, clear all rows from patient_indication corresponding to patient_id
        if self.lblHeader.text() != "New Patient":
            query = QSqlQuery()
            query.prepare("DELETE FROM patient_indication WHERE patient_id = :id")
            query.bindValue(":id", self.mrn)
            query.exec()

        # Insert new indications into the patient_indication table
        for id in patient_indication_id:
            query = QSqlQuery()
            query.prepare("INSERT INTO patient_indication (indication_id, patient_id) "
                          "VALUES (:indication_id, :patient_id)")
            query.bindValue(":indication_id", id)
            query.bindValue(":patient_id", self.ledMRN.text())
            query.exec()

    def query_get_patient_indication_ids(self):
        """
        Perform a series of steps to create a list of indication ids
        :return: a list of indication_ids associated with the patient
        """

        # List of patient-set indication names
        num_of_patient_indications = self.lstPatientIndications.count()
        self.list_of_patient_indications = []
        for row in range(num_of_patient_indications):
            list_widget_item = self.lstPatientIndications.item(row)
            self.list_of_patient_indications.append(list_widget_item.text())
        # Use the list of patient-set indication names to get a list of associated indication ids
        patient_indication_id = []
        bOk, query = self.query_get_indication_names_and_ids()
        if bOk:
            while query.next():
                if query.value('indication_name') in self.list_of_patient_indications:
                    patient_indication_id.append(query.value('indication_id'))
        return patient_indication_id

    def query_update_patient_table(self):
        """Send a query to update the patient table"""
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
        query.bindValue(":inr_goal_from", "{:.1f}".format(Decimal(self.ledGoalFrom.text())))
        query.bindValue(":inr_goal_to", "{:.1f}".format(Decimal(self.ledGoalTo.text())))
        query.bindValue(":id", self.mrn)
        query.exec()

    def populate_indication_list(self):
        """Populate list widgets for both patient and non-patient indications"""
        self.lstPatientIndications.clear()
        self.lstExistingIndications.clear()

        # Populate the patient indication list box from patient table
        if self.mrn:
            self.lstPatientIndications.addItems(self.list_of_patient_indications)
            self.lstPatientIndications.sortItems()

        # Populate the non-patient indication list box from the indication table
        bOk, query = self.query_get_indication_names_and_ids()
        if bOk:
            while query.next():
                try:
                    if query.value('indication_name') not in self.list_of_patient_indications:
                        self.lstExistingIndications.addItem(query.value('indication_name'))
                except:
                    self.lstExistingIndications.addItem(query.value('indication_name'))

        self.lstExistingIndications.sortItems()

    def query_get_indication_names_and_ids(self):
        """Retrieves all indication ids and names from the indication table"""
        query = QSqlQuery()
        bOk = query.exec("SELECT indication_id, indication_name FROM indication")
        return bOk, query

    def validate_patient_information(self):
        """
        Sets validation for line edit widgets
        1. Reset stylesheet for line edit widgets prior to validation
        2. Validate line edit widget for first name, last name, date of birth, list widget item count, INR goal
        3. Validate MRN if new patient
        """
        error_message = ""
        format_string_name = "[\w+\-]+$"
        format_string_birthdate = "\d{4}-\d{2}-\d{2}"
        format_string_inr_goal = "^[0-9]\d*(\.\d+)?$"

        self.ledMRN.setStyleSheet("")
        self.ledFirstName.setStyleSheet("")
        self.ledLastName.setStyleSheet("")
        self.ledDOB.setStyleSheet("")
        self.ledGoalFrom.setStyleSheet("")
        self.ledGoalTo.setStyleSheet("")

        # Validate MRN if new patient
        if self.lblHeader.text() == "New Patient":
            if self.ledMRN.text() == "":
                error_message += "Medical record number cannot be blank.\n"
                self.ledMRN.setStyleSheet(style_line_edit_error())
            elif not self.ledMRN.text().isnumeric():
                error_message += "Medical record number must be numeric.\n"
                self.ledMRN.setStyleSheet(style_line_edit_error())
            else:
                if self.is_duplicate(self.ledMRN.text()):
                    error_message += "Duplicate medical record number already on file.\n"
                    self.ledMRN.setStyleSheet(style_line_edit_error())


        # Validate first name
        if self.ledFirstName.text() == "":
            error_message += "First name cannot be blank.\n"
            self.ledFirstName.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_name, self.ledFirstName.text()):
            error_message += "First name can only contain letters and hyphens.\n"
            self.ledFirstName.setStyleSheet(style_line_edit_error())

        # Validate last name
        if self.ledLastName.text() == "":
            error_message += "Last name cannot be blank.\n"
            self.ledLastName.setStyleSheet(style_line_edit_error())
        elif not re.match(format_string_name, self.ledLastName.text()):
            error_message += "Last name can only contain letters and hyphens.\n"
            self.ledLastName.setStyleSheet(style_line_edit_error())

        # Validate date of birth
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

        # Validate indication
        if self.lstPatientIndications.count() == 0:
            error_message += "Patient must have at least one indication.\n"

        # Validate INR goal
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

    # def validate_new_indication(self):
    #     """Validates line edit widget for new indication and duplicate entries"""
    #     string_format = "^[\w() -]{2,}$"  # only allow words, spaces, hyphens, and parenthesis
    #     error_message = ""
    #
    #     # Validate line edit widget
    #     if not re.match(string_format, self.new_indication):
    #         error_message += "Indication name can only contain words, spaces, hyphens, and parenthesis.\n"
    #
    #     if len(self.new_indication) <= 2:
    #         error_message += "Indication name must contain more than two characters.\n"
    #
    #     # Validate duplicate entries
    #     bOk, query = self.query_get_indication_names_and_ids()
    #     if bOk:
    #         all_indications = []
    #         while query.next():
    #             all_indications.append((query.value('indication_id'), query.value('indication_name')))
    #
    #         for indication in all_indications:
    #             if self.new_indication == indication[1]:
    #                 error_message += "This indication already exists.\n"
    #
    #     return error_message

    def is_duplicate(self, id):
        """Determines if there is a duplicate patient_id in the patient table"""
        list_of_patient_ids = []
        query = QSqlQuery()
        bOk = query.exec("SELECT patient_id FROM patient")
        if bOk:
            while query.next():
                list_of_patient_ids.append(query.value('patient_id'))
        if int(id) in list_of_patient_ids:
            return True

        return False


class DlgAnalytics(QDialog):
    """Dialog box to display analytics"""
    def __init__(self, percent_ttr, total_days_in_ttr, total_days, total_tests, number_of_results_in_range):
        super(DlgAnalytics, self).__init__()
        self.resize(700, 600)
        self.setWindowTitle("Analytics")
        self.lytMain = QVBoxLayout()

        # Create Pie Chart
        self.pie_ttr = QPieSeries()
        self.pie_ttr.append("% Days In Range", percent_ttr)
        self.pie_ttr.append("% Days Out Of Range ", 1 - percent_ttr)
        self.pie_slice_ttr = QPieSlice()
        self.pie_slice_ttr = self.pie_ttr.slices()[0]
        self.pie_slice_not_ttr = self.pie_ttr.slices()[1]

        chart = QChart()
        chart.addSeries(self.pie_ttr)
        chart.setTitle("<h1>Time Within Therapeutic Range</h1>")
        chart.setTheme(QChart.ChartThemeBlueNcs)
        chart.legend().hide()

        self.pie_ttr.setLabelsVisible()

        self.pie_slice_ttr.setLabel(str(int(self.pie_slice_ttr.percentage() * 100)) + f"% TTR: {round(total_days_in_ttr)} days")
        self.pie_slice_ttr.setLabelColor(QColor("green"))

        self.pie_slice_not_ttr.setLabel(str(int(self.pie_slice_not_ttr.percentage() * 100)) + f"% Out of range: {round(total_days - total_days_in_ttr)} days")
        self.pie_slice_not_ttr.setLabelColor(QColor("red"))

        for slice in self.pie_ttr.slices():
            font = QtGui.QFont()
            font.setBold(True)
            font.setPixelSize(12)
            slice.setLabelFont(font)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create text edit box for summary data
        description = f"""
        <h2>Summary</h2>
        <ul style="font-size: 14px">
            <li><strong>Total Days On Record: </strong> <span style="color: blue">{round(total_days)}</span></li>
            <li><strong>Days Within Range: </strong> <span style="color: blue">{round(total_days_in_ttr)}</span></li>
            <li><strong>Percent of Days Within Range: </strong> <span style="color: blue">{round((total_days_in_ttr / total_days) * 100)}%</span><br></li>
            <li><strong>Total Number of Tests:</strong> <span style="color: blue">{total_tests}</span></li>
            <li><strong>Number of Tests in Range: </strong> <span style="color: blue">{number_of_results_in_range}</span></li>
            <li><strong>Percent of Test in Range: </strong> <span style="color: blue">{round((number_of_results_in_range / total_tests) * 100)}%</span></li>
        </ul>
        
        <div style = "font-size: 14px">
        <em>TTR was calculated using the Rosendaal linear interpolation method, which assumes a linear change between INR 
        measurements over time. Clinical judgement should be used when evaluating the significance of TTR in clinical
        decision making.</em>
        </div>
        """

        text_edit = QTextEdit(description)
        text_edit.setReadOnly(True)

        self.lytMain.addWidget(chart_view)
        self.lytMain.addWidget(text_edit)
        self.setLayout(self.lytMain)

class DlgReport(QDialog, Ui_DlgReport):
    """Dialog box for the clinic report"""
    def __init__(self):
        super(DlgReport, self).__init__()
        self.setupUi(self)


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


def validate_new_indication(new_indication):
    """Validates line edit widget for new indication and duplicate entries"""
    string_format = "^[\w() -]{2,}$"  # only allow words, spaces, hyphens, and parenthesis
    error_message = ""

    # Validate line edit widget
    if not re.match(string_format, new_indication):
        error_message += "Indication name can only contain words, spaces, hyphens, and parenthesis.\n"

    if len(new_indication) <= 2:
        error_message += "Indication name must contain more than two characters.\n"

    # Validate duplicate entries
    query = QSqlQuery()
    bOk = query.exec("SELECT indication_id, indication_name FROM indication")
    if bOk:
        all_indications = []
        while query.next():
            all_indications.append((query.value('indication_id'), query.value('indication_name')))

        for indication in all_indications:
            if new_indication == indication[1]:
                error_message += "This indication already exists.\n"

    return error_message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
