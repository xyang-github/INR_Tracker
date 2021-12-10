import re
from decimal import Decimal
import datetime
import csv
import dateutil
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor, QBrush, QPainter, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtSql import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from gui.main_ui import *
from gui.patientprofile import *
from gui.add_update_result import *
from gui.newpatient import *
from gui.indications import *
from gui.editindication import *
from gui.report import *
from gui.message_box_critical import *
from gui.message_box_question import *
from gui.help import *
from gui.patientlist import *
from gui.add_update_event import *


class DlgMain(QMainWindow, Ui_dlgMain):
    """Main window for application"""
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # Create database connection
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
            if "event" not in self.database.tables():
                self.create_event_table()
            if "patient_event" not in self.database.tables():
                self.create_patient_event_table()
        else:
            message_box_critical("Could not connect with the database.")

        # Event handlers for action and button widgets
        self.actionExit.triggered.connect(self.evt_action_exit_triggered)
        self.actionAdd_New_Patient.triggered.connect(self.evt_btn_new_patient_clicked)
        self.actionINR_Tracker_Help.triggered.connect(self.evt_action_help_triggered)
        self.btnSearch.clicked.connect(self.evt_btn_search_clicked)
        self.btnNewPatient.clicked.connect(self.evt_btn_new_patient_clicked)
        self.btnIndications.clicked.connect(self.evt_btn_indications_clicked)
        self.btnReports.clicked.connect(self.evt_btn_reports_clicked)

    def evt_btn_search_clicked(self):
        """Searches for a matching patient in the database"""
        self.mrn = self.ledMRN.text()

        if self.ledMRN.text() == "":
            message_box_critical("Please enter a medical record number.")
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
                message_box_critical("The medical record number entered does not match a patient on record.")

        self.ledMRN.clear()  # Clear line edit widget after searching

    def evt_action_exit_triggered(self):
        """Closes the main application"""
        sys.exit(app.exec_())

    def evt_btn_new_patient_clicked(self):
        """Creates a new patient dialog window"""
        dlgNewPatient = DlgNewUpdatePatient()
        dlgNewPatient.rbtnStatusInactive.setEnabled(False)
        dlgNewPatient.show()
        dlgNewPatient.exec_()
        dlgNewPatient.populate_indication_list()

    def evt_btn_indications_clicked(self):
        """Create a dialog window to add/edit/delete indication list"""
        dlgIndications = DlgIndications()
        dlgIndications.show()
        dlgIndications.exec_()

    def evt_btn_reports_clicked(self):
        """Create a dialog box for the clinic report"""
        html = self.get_html_clinic_report()

        dlgReport = DlgReport(html)
        dlgReport.tedReport.setHtml(html)
        dlgReport.show()
        dlgReport.exec_()

    def evt_action_help_triggered(self):
        html = self.get_html_help()

        dlgHelp = DlgHelp()
        dlgHelp.tbrDocument.setHtml(html)
        dlgHelp.adjustSize()
        dlgHelp.show()
        dlgHelp.exec_()

    def get_html_clinic_report(self):
        """Create and return an HTML string for the clinic report"""

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

    def get_html_help(self):
        """Create and return an HTML string for the help document"""
        html = """

<h2>INR Tracker</h2><br>
<img src="screenshot/main.JPG"><br>

INR Tracker is a desktop application intended to assist with the management of Anticoagulation Clinics (specifically 
for patients on warfarin). Overall, this application can create patient profiles, allow the input of INR results and 
to produce analytics from those results. All information is stored into a relational database, which allows editing 
and deleting of information.<br><br>

Each patient has an <b>identifier</b>, which will be referred to as a medical record number (MRN). The MRN is added 
upon creation of a new patient profile. The MRN cannot be changed later. If an MRN is on record, the patient profile 
will be displayed.

<hr>

<h2>Patient Profile - Summary Tab</h2><br>
<img src="screenshot/patient profile.JPG"><br>
The patient profile is organized within two tabs: the <b>Summary</b> and <b>Results</b> tab. The summary tab will 
display general information, including options to edit the patient profile, export patient information to CSV or PDF, 
and producing patient specific analytics. 

<hr>

<h2>Patient Profile - Updating</h2><br>
<img src="screenshot/edit profile.JPG"><br>
The patient profile can also be edited, with the exception of the medical record number. Note that changing the status 
to inactive will disable the ability to add, edit or delete results. The indication can be changed here, and new 
indications can be added to the database. The INR goal can also be changed here as well.

<hr>

<h2>Patient Profile - Results Tab</h2><br>
<img src="screenshot/patient results.JPG"><br>
The Results tab will display a table of results in the database. The information displayed are Date, INR, Goal, 
Total Dose (in milligrams) and Comment. The INR column will be colored depending on if the INR is within goal, 
supratherapeutic or subtherapeutic. The goal defaults to the INR goal established in the patient profile, but a 
different goal can be specified for any specific result. <br>

A single click in the Comment column will display the comment in a pop-up dialog window if the cell is not empty.
<br><br>
A double click on any of the other columns (or an empty Comment column) will automatically produce a dialog window to 
update the result.


<hr>

<h2>Add/Update Result</h2><br>
<img src="screenshot/add result.JPG"><br>
<ul>
    <li>When adding a result to the patient’s profile, a dialog window will appear. The date is defaulted to the 
    current date, but can be changed.</li>
    <li>Clicking the “No Changes” dialog box will prepopulate the dose with the most recent regimen on file. </li>
    <li>The INR goal will also default to the goal that has been entered for the patient, but a new INR can be 
    specified in certain cases (e.g. a lower goal for a procedure). </li>
    <li>A comment can be entered as well.</li>
</ul>


<hr>

<h2>Patient Analytics</h2><br>
<img src="screenshot/patient analytics.JPG"><br>
Analytics can be produced if patient has at least two results on record. The TTR is calculated using the Rosendaal 
linear interpolation method. Other information includes total days on record, days within range, percent of days 
within range, total number of tests, number of tests in range, and percent of test in range.

<hr>

<h2>Patient Summary PDF</h2><br>
<img src="screenshot/patient pdf.JPG" width=500><br>
A summary report can be saved for each patient. The purpose of this function is to be able to provide relevant 
anticoagulation information to medical facilities requesting for such information.

<hr>

<h2>New Patient Profile</h2><br>
<img src="screenshot/new patient.JPG"><br>
A new patient profile can be entered from the main menu. The Status is referring to a patient’s anticoagulation 
status. Examples of an inactive patient can include those who have finished treatment for an acute VTE, or those that 
have transferred care to another facility. By default, you can only create a patient profile with an active status. 
Note that the date of birth has to be entered in the YYYY-MM-DD format.

<hr>

<h2>Indications</h2><br>
<img src="screenshot/indication.JPG"><br>
The list of indications on record can also be edited. Note that validation methods are in place to prevent duplicate 
entries. Best practice is to avoid abbreviations of indications.

<hr>

<h2>Clinic Summary</h2><br>
<img src="screenshot/clinic report.JPG"><br>
A clinic report can be generated with certain metrics. The information can also be exported to a PDF format if desired.
        """

        return html

    def create_indication_table(self):
        """Create the 'indication' table needed in the database"""
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
        """Create the 'inr' table needed in the database"""
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
        """Create the 'patient' table needed in the database"""
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
        """Create the 'patient_indication' linking table needed in the database"""
        command = """
            CREATE TABLE IF NOT EXISTS "patient_indication" (
                "indication_id"	INTEGER NOT NULL,
                "patient_id"	INTEGER NOT NULL,
                FOREIGN KEY("patient_id") REFERENCES "patient"("patient_id") on delete cascade
            )
        """
        query = QSqlQuery()
        query.exec_(command)

    def create_event_table(self):
        """Create the 'event' table needed in the database"""
        command = """
        CREATE TABLE IF NOT EXISTS "event" (
            "event_id"	INTEGER,
            "event_name"	TEXT,
            PRIMARY KEY("event_id" AUTOINCREMENT)
        );
        """
        query = QSqlQuery()
        query.exec_(command)

    def create_patient_event_table(self):
        """Create the 'patient_event' table needed in the database"""
        command = """
        CREATE TABLE IF NOT EXISTS "patient_event" (
            "event_id"	INTEGER,
            "patient_id"	INTEGER,
            "date"	TEXT,
            "comment"	TEXT,
            PRIMARY KEY("event_id","patient_id","date")
        );
        """
        query = QSqlQuery()
        query.exec_(command)


class DlgIndications(QDialog, Ui_DlgIndications):
    """Indication window for application"""
    def __init__(self):
        super(DlgIndications, self).__init__()
        self.setupUi(self)

        # Event handlers for push buttons
        self.btnAdd.clicked.connect(self.evt_btn_add_clicked)
        self.btnEdit.clicked.connect(self.evt_btn_edit_clicked)
        self.btnDelete.clicked.connect(self.evt_btn_delete_clicked)
        self.btnExit.clicked.connect(self.close)

        self.populate_indication_list()

    def evt_btn_add_clicked(self):
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

    def evt_btn_edit_clicked(self):
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

    def evt_btn_delete_clicked(self):
        """Delete selected list item widget from the database"""
        error_message = self.validate_if_selected()

        if error_message:
            message_box_critical(error_message)
        else:
            self.selected_indication = self.lstIndications.selectedItems()[0].text()
            self.question = message_box_question(f"Are you sure you want to delete the indication: "
                                                 f"{self.selected_indication}? This will remove the indication from "
                                                 f"all patients that have this indication.")
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


class DlgPatientProfile(QDialog, Ui_DlgProfile):
    """Dialog window for the patient profile"""
    def __init__(self, id):
        super(DlgPatientProfile, self).__init__()
        self.setupUi(self)
        self.number_of_results_in_range = 0
        self.mrn = id

        # Result table widget formatting
        self.tblResult.setAlternatingRowColors(True)
        self.tblResult.setColumnWidth(2, 50)
        self.tblResult.setColumnWidth(3, 60)
        self.tblResult.setColumnWidth(4, 80)
        self.tblResult.horizontalHeader().setStretchLastSection(True)
        self.tblResult.setSortingEnabled(True)
        self.tblResult.setSelectionBehavior(QtWidgets.QTableWidget.SelectItems)
        self.tblResult.setSelectionMode(1)  # Single selection mode
        self.tblResult.selectionModel().selectionChanged.connect(self.display_comment_column)

        # Event table widget formatting
        self.tblEvents.setAlternatingRowColors(True)
        self.tblEvents.horizontalHeader().setStretchLastSection(True)
        self.tblEvents.setSortingEnabled(True)
        self.tblEvents.setSelectionBehavior(QtWidgets.QTableWidget.SelectItems)
        self.tblEvents.setSelectionMode(1)

        self.populate_patient_summary()

        # Warning message will display if no indication on record for a patient.
        # Also disables buttons to add, edit and delete results.
        if self.ledIndications.text() == "No Indication On Record":
            message_box_critical("""
            There is no indication on record for this patient. Please add an indication in order to add, edit or 
            delete any further results."
            """)

            self.btnAdd.setDisabled(True)
            self.btnEdit.setDisabled(True)
            self.btnDelete.setDisabled(True)
        else:
            self.btnAdd.setDisabled(False)
            self.btnEdit.setDisabled(False)
            self.btnDelete.setDisabled(False)

        self.populate_result_table()
        self.populate_event_table()

        # Event handlers for push buttons and double clicking
        self.tblResult.itemDoubleClicked.connect(self.evt_btn_edit_result_clicked)
        # self.tblEvents.itemDoubleClicked.connect()
        self.btnAdd.clicked.connect(self.evt_btn_add_result_clicked)
        self.btnEdit.clicked.connect(self.evt_btn_edit_result_clicked)
        self.btnDelete.clicked.connect(self.evt_btn_delete_result_clicked)
        self.btnEditPatient.clicked.connect(self.evt_btn_edit_patient_clicked)
        self.btnExit.clicked.connect(self.close)
        self.btnAnalytics.clicked.connect(self.evt_btn_analytics_clicked)
        self.btnCSV.clicked.connect(self.evt_btn_csv_clicked)
        self.btnPDF.clicked.connect(self.evt_btn_pdf_clicked)
        self.btnAdd_event.clicked.connect(self.evt_btn_add_event_clicked)
        self.btnEdit_event.clicked.connect(self.evt_btn_edit_event_clicked)

# Result Tab
    def evt_btn_add_result_clicked(self):
        """Create a dialog window to add new results to the result table widget and database"""
        dlgAddResult = DlgAddUpdateResult(self.mrn)
        dlgAddResult.btnOK.clicked.connect(dlgAddResult.evt_btn_add_result_clicked)
        dlgAddResult.show()
        dlgAddResult.exec_()
        self.populate_result_table()

    def evt_btn_edit_result_clicked(self):
        """Creates a dialog window to edit a result selected from the result table widget"""

        # Check if there is any item in the result table widget to edit
        try:
            self.get_current_row_and_inr_id()
        except AttributeError:
            message_box_critical("No entries to edit.")
            return

        # Create the dialog window to edit the selected result
        dlgEditResult = DlgAddUpdateResult(self.mrn, self.current_selection_inr_id)
        dlgEditResult.setWindowTitle("Edit Result")
        dlgEditResult.btnOK.setText("Update")

        # Retrieve information from the database based on the selected row id of the result table
        query = self.query_get_inr_information()
        query.next()

        # Extract the date from the database information
        original_date = query.value('date').split("-")
        original_year = int(original_date[0])
        original_month = int(original_date[1])
        original_day = int(original_date[2])
        original_date_object = QDate(original_year, original_month, original_day)

        # Extract the patient-set INR goal and the result-set INR goal from the database information
        inr_goal_from = query.value('inr_goal_from')
        inr_goal_to = query.value('inr_goal_to')
        patient_inr_goal_from, patient_inr_goal_to = dlgEditResult.query_get_patient_inr_goal()

        # Toggles radio buttons for default or new INR goal
        if patient_inr_goal_from != query.value('inr_goal_from') and patient_inr_goal_to != query.value('inr_goal_to'):
            dlgEditResult.rbtnGoal_New.setChecked(True)
            dlgEditResult.evt_rbtn_new_goal_clicked()
            dlgEditResult.ledNewGoalFrom.setText(inr_goal_from)
            dlgEditResult.ledNewGoalTo.setText(inr_goal_to)

        # Populates the line edit widgets for each daily dose from the database information
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

        # Event handler for push button to update the result table widget and database
        dlgEditResult.btnOK.clicked.connect(dlgEditResult.evt_btn_update_result_clicked)

        dlgEditResult.show()
        dlgEditResult.exec_()
        self.populate_result_table()

    def evt_btn_delete_result_clicked(self):
        """Ask for verification to delete the selected row from the result table widget and database"""
        try:
            self.get_current_row_and_inr_id()
        except AttributeError:
            message_box_critical("No entries to delete.")
            return

        self.question = message_box_question(f"You have selected row {self.current_selection_row + 1} to be deleted.")

        # Event handler to delete record from the result table and database
        self.question.btnAccept.clicked.connect(self.query_delete_inr)

        self.question.show()
        self.question.exec_()

        self.populate_result_table()

    def populate_result_table(self):
        """Populates the result table widget with information from the database"""
        self.tblResult.clearContents()  # Clears the result table widget to prevent displaying of duplicate entries
        self.tblResult.setRowCount(0)  # Resets row count to prevent empty rows

        # Query a request for information from the database
        query = QSqlQuery()
        query.prepare("SELECT inr_id, date, result, (i.inr_goal_from || '-' || i.inr_goal_to) AS goal, "
                      "(dose_mon + dose_tue + dose_wed + dose_thu + dose_fri + dose_sat + dose_sun) AS total_dose, "
                      "comment FROM inr i JOIN patient p ON  p.patient_id = i.patient_id "
                      "WHERE p.patient_id = :id ORDER BY date DESC")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                # Populate the result table widget with information retrieved from the database
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

        self.tblResult.setColumnHidden(0, True)  # Hide 'inr_id' column from view
        self.tblResult.setCurrentCell(0, 1)  # Set default selection to the most recent entry

    def format_result_col(self, row, tbl_result_col_value, inr_low, inr_high):
        """
        Format the background color of the result column in the result table widget. Green for therapeutic, yellow
        for subtherapeutic and red for supratherapeutic results.
        """
        if tbl_result_col_value.text() > inr_high:
            self.tblResult.item(row, 2).setBackground(QColor("#ff3300"))
        elif tbl_result_col_value.text() < inr_low:
            self.tblResult.item(row, 2).setBackground(QColor("#ffff00"))
        else:
            self.tblResult.item(row, 2).setBackground(QColor("#00ff80"))
            self.number_of_results_in_range += 1

    def format_weekly_dose(self):
        """
        Change the font formatting of the weekly dose column in the result table widget.  Formatting will be
        applied if the weekly dose has changed from the previous entry.
        """
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
        """
        Change the font formatting of the goal column in the result table widget.  Formatting will be
        applied if the inr-specific goal has changed from the previous entry.
        """
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
        """
        Retrieve the row number and inr_id of the current selection in the result table widget. These values are stored
        in a variable to be used in other functions.
        """
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_inr_id = self.tblResult.item(self.current_selection_row, 0).text()

    def display_comment_column(self, selected):
        """Display a dialog box containing comments if the comment column if the result table is filled"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_comment = f"<b>Comment:</b> <br>" \
                                         f"{self.tblResult.item(self.current_selection_row, 5).text()}"

        for i in selected.indexes():
            if i.column() == 5 and self.current_selection_comment:
                message_box_critical(self.current_selection_comment)
                self.tblResult.selectionModel().clearSelection()

    def query_get_inr_information(self):
        """Query a request to retrieve patient specific INR information from the database"""
        query = QSqlQuery()
        query.prepare("SELECT inr_id, patient_id, date, result, dose_mon, dose_tue, dose_wed, dose_thu, dose_fri, "
                      "dose_sat, dose_sun, comment, inr_goal_from, inr_goal_to from inr WHERE inr_id = :id")
        query.bindValue(":id", self.current_selection_inr_id)
        bOk = query.exec()
        if bOk:
            return query

    def query_delete_inr(self):
        """Query a request to delete record from the database"""
        query = QSqlQuery()
        query.prepare("DELETE FROM inr WHERE inr_id = :id")
        query.bindValue(":id", self.current_selection_inr_id)
        bOk = query.exec()
        if bOk:
            message_box_critical("Record deleted.")

        self.question.close()  # close dialog box

# Summary Tab

    def evt_btn_edit_patient_clicked(self):
        """Creates a dialog window to edit patient information"""
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

        # Create and edit dialog widget
        dlgEditPatient = DlgNewUpdatePatient(self.mrn, self.list_patient_indication_name)
        dlgEditPatient.setWindowTitle("Edit Patient Information")
        dlgEditPatient.lblHeader.setText("Update Information")
        dlgEditPatient.populate_indication_list()

        # Populate line edit widgets with patient information
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
        """Calculates the TTR and opens a dialog window to display the results"""
        self.total_rows = self.tblResult.rowCount()
        self.total_days = 0
        self.days_in_ttr = 0

        # Check if enough results to perform analytics. Must have at least 2 results in the result table widget.
        if self.total_rows < 2:
            message_box_critical("Must have at least 2 INR results to produce analytics.")
        else:
            # Calculate the analytics
            for i in range(self.total_rows - 1):
                ttr = 0
                shift_in_ttr = 0
                calculate_ttr = "(shift_in_ttr / total_shift) * days_between_results"

                # Retrive dates of the first two results
                date1 = self.tblResult.item(i+1, 1).text().split("-")  # Date for the older result
                date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))

                date2 = self.tblResult.item(i, 1).text().split("-")  # Date for the newer result
                date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
                days_between_results = abs((date2 - date1).days)

                # Retrieve the INR result for the first two results
                result1 = Decimal(self.tblResult.item(i+1, 2).text())  # Older result pertaining to date1
                result2 = Decimal(self.tblResult.item(i, 2).text())  # Newer result pertaining to date2
                total_shift = abs(result2 - result1)

                # Retrieve result-set INR goal for the first two results
                inr_goal = self.tblResult.item(i, 3).text().split("-")
                inr_goal_lower_limit = Decimal(inr_goal[0])
                inr_goal_upper_limit = Decimal(inr_goal[1])

                # Calculates TTR
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

                self.days_in_ttr += ttr
                self.total_days += days_between_results

            percent_ttr = self.days_in_ttr / self.total_days

            dlgAnalytics = DlgAnalytics(percent_ttr, self.days_in_ttr, self.total_days,
                                        self.total_rows, self.number_of_results_in_range)
            dlgAnalytics.show()
            dlgAnalytics.exec_()

    def evt_btn_csv_clicked(self):
        """Save the result table widget to a csv file"""
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
        """Save a patient summary report to a pdf"""
        html = self.create_html()
        document = QTextDocument()
        document.setHtml(html)
        printer = QPrinter()
        document.print_(printer)

    def populate_patient_summary(self):
        """Populate the patient profile's summary tab with patient specific information"""
        self.list_patient_summary_info, self.list_patient_indication_name = self.query_get_patient_summary_info()
        self.list_patient_indication_name.sort()

        self.ledFirstName.setText(self.list_patient_summary_info[0])
        self.ledLastName.setText(self.list_patient_summary_info[1])
        self.ledDOB.setText(self.list_patient_summary_info[2])
        self.ledIndications.setText(', '.join(self.list_patient_indication_name))
        self.ledGoal.setText(f"{self.list_patient_summary_info[4]} - {self.list_patient_summary_info[5]}")
        self.lblName.setText(f"{self.list_patient_summary_info[1]}, {self.list_patient_summary_info[0]}")
        self.lblName_events.setText(f"{self.list_patient_summary_info[1]}, {self.list_patient_summary_info[0]}")
        if self.list_patient_summary_info[7] == "A":
            self.ledStatus.setText("Active")
        else:
            self.ledStatus.setText("Inactive")

        self.check_status()

    def create_html(self):
        """Creates and returns an HTML string for PDF output"""
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

    def check_status(self):
        """Check for inactive patient status. If patient is inactive, the buttons to add, edit and delete
        results will be disabled"""
        if self.ledStatus.text() == "Inactive":
            self.btnAdd.setDisabled(True)
            self.btnEdit.setDisabled(True)
            self.btnDelete.setDisabled(True)
            self.lblNotice.setText("This patient's status is currently INACTIVE. Only ACTIVE patients can have "
                                   "results added, edited, \nand deleted.")
        else:
            self.lblNotice.setText("")
            self.btnAdd.setDisabled(False)
            self.btnEdit.setDisabled(False)
            self.btnDelete.setDisabled(False)

    def query_get_patient_summary_info(self):
        """Query a request for patient information. Returns a list of patient information and patient indications."""
        self.list_patient_summary_info = []
        self.list_patient_indication_name = []

        query = QSqlQuery()
        query.prepare("SELECT patient_id, indication_id FROM patient_indication WHERE patient_id = :id")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            query.next()
            if query.isValid():
                # If patient has an indication on record, will retrieve needed information from the database
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
                # An alternative query if there is no indication on record
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

# Event Tab

    def evt_btn_add_event_clicked(self):
        dlgAddEvent = DlgAddEditEvent(self.mrn)
        dlgAddEvent.show()
        dlgAddEvent.btnOK_event.clicked.connect(dlgAddEvent.evt_btn_ok_event_clicked)
        dlgAddEvent.exec()
        self.populate_event_table()

    def evt_btn_edit_event_clicked(self):
        """Creates a dialog window to edit an event selected from the event table widget"""

        # Check if there is any item in the event table widget to edit
        if self.tblEvents.rowCount() == 0:
            message_box_critical("No entries to edit.")
            return

        # Check if a selection has been made to edit
        if not self.tblEvents.selectedItems():
            message_box_critical("No entry selected to edit.")
            return

        self.dlgEditEvent = DlgAddEditEvent(self.mrn)
        self.dlgEditEvent.setWindowTitle("Edit Event")
        self.dlgEditEvent.lstCurrentEvent.clear()
        self.dlgEditEvent.lstPatientEvent.clear()

        # Retrieve information from the selected row in the event table widget
        row = self.tblEvents.currentRow()
        self.date = self.tblEvents.item(row, 0).text()
        date_list = self.date.split("-")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        self.event_name = self.tblEvents.item(row, 1).text()
        self.comments = self.tblEvents.item(row, 2).text()

        # Populates the input widgets on the window
        self.dlgEditEvent.dteDate_event.setDate(QDate(year, month, day))
        self.dlgEditEvent.txtComment_event.insertPlainText(self.comments)
        self.dlgEditEvent.lstPatientEvent.addItem(QListWidgetItem(self.event_name))

        query = QSqlQuery()
        bOk = query.exec("SELECT event_id, event_name FROM event")
        if bOk:
            while query.next():
                if query.value('event_name') != self.event_name:
                    self.dlgEditEvent.lstCurrentEvent.addItem(query.value('event_name'))

        # Set input widgets to read only except the comment
        self.dlgEditEvent.dteDate_event.setReadOnly(True)
        self.dlgEditEvent.ledNewEvent.setPlaceholderText("Disabled when editing entry.")
        self.dlgEditEvent.ledNewEvent.setReadOnly(True)
        self.dlgEditEvent.btnAddEvent.setDisabled(True)
        self.dlgEditEvent.btnRemoveEvent.setDisabled(True)
        self.dlgEditEvent.btnNewEvent.setDisabled(True)

        # Event handler for push button when editing an event entry
        self.dlgEditEvent.btnOK_event.clicked.connect(self.evt_btn_update_event_clicked)

        self.dlgEditEvent.show()
        self.dlgEditEvent.exec()
        self.populate_event_table()

    def evt_btn_update_event_clicked(self):
        """Update the comment column. Date, event id and patient id are composite primary keys"""
        query = QSqlQuery()
        query.prepare("SELECT event_id from event WHERE event_name = :name")
        query.bindValue(":name", self.event_name)
        query.exec()
        query.next()
        event_id = query.value('event_id')

        query = QSqlQuery()
        query.prepare("UPDATE patient_event SET comment = :comment WHERE date = :event_date AND event_id = :event_id "
                      "AND patient_id = :patient_id")
        query.bindValue(":comment", self.dlgEditEvent.txtComment_event.toPlainText())
        query.bindValue(":event_date", self.date)
        query.bindValue(":event_id", int(event_id))
        query.bindValue(":patient_id", int(self.mrn))
        bOk = query.exec()
        if bOk:
            message_box_critical("Record updated.")
            self.dlgEditEvent.close()
        else:
            message_box_critical("Not able to update record.")

    def populate_event_table(self):
        """Populates the event table widget with information from the database"""
        self.tblEvents.clearContents()
        self.tblEvents.setRowCount(0)

        query = QSqlQuery()
        query.prepare("SELECT pe.date, e.event_name, pe.comment FROM patient p JOIN patient_event pe "
                      "ON p.patient_id = pe.patient_id JOIN event e ON pe.event_id = e.event_id "
                      "WHERE p.patient_id = :id ORDER BY date DESC")
        query.bindValue(":id", self.mrn)
        bOk = query.exec()
        if bOk:
            while query.next():
                row = self.tblEvents.rowCount()
                self.tblEvents.insertRow(row)
                for col in range(3):
                    tbl_row_value = QTableWidgetItem(str(query.value(col)))
                    self.tblEvents.setItem(row, col, tbl_row_value)


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

        # Set radio button default selection
        self.patient_inr_goal_from, self.patient_inr_goal_to = self.query_get_patient_inr_goal()
        self.rbtn_Goal_Default.setText(f"Default: {self.patient_inr_goal_from} - {self.patient_inr_goal_to}")

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
        self.chkNoChanges.clicked.connect(self.evt_chkbox_no_changes_clicked)
        self.rbtnGoal_New.clicked.connect(self.evt_rbtn_new_goal_clicked)
        self.rbtn_Goal_Default.clicked.connect(self.evt_rbtn_default_goal_clicked)
        self.btnCancel.clicked.connect(self.close)

    def evt_btn_add_result_clicked(self):
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

    def evt_btn_update_result_clicked(self):
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

    def evt_chkbox_no_changes_clicked(self, chk):
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
                    message_box_critical("No previous doses detected on record.")
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

                if self.new_inr_goal_from == str(patient_inr_goal_from) and \
                        self.new_inr_goal_to == str(patient_inr_goal_to):
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
    """Dialog window for adding new patients"""
    def __init__(self, id=None, patient_indications=None):
        super(DlgNewUpdatePatient, self).__init__()
        self.setupUi(self)
        self.mrn = id
        self.list_of_patient_indications = patient_indications

        if self.mrn:
            self.ledMRN.setReadOnly(True)  # Prevents editing the medical record number, which is a primary key

        self.populate_indication_list()

        # Event handlers for push buttons
        self.btnAddIndication.clicked.connect(self.evt_btn_add_patient_indication_clicked)
        self.btnRemoveIndication.clicked.connect(self.evt_btn_remove_patient_indication_clicked)
        self.btnNewIndication.clicked.connect(self.evt_btn_new_indication_clicked)
        self.btnOk.clicked.connect(self.evt_btn_ok_clicked)
        self.btnExit.clicked.connect(self.close)

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
        """Add new indication to database"""
        self.new_indication_name = self.ledNewIndication.text().lower().strip()
        error_message = validate_new_indication(self.new_indication_name)
        if error_message:
            message_box_critical(error_message)
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
                        message_box_critical("Indication added to the database.")
        self.populate_indication_list()
        self.ledNewIndication.setText("")

    def evt_btn_ok_clicked(self):
        """Add or update patient and patient_indication tables"""
        error_message = self.validate_patient_information()
        action = ""
        if error_message:
            message_box_critical(error_message)
        else:
            if self.lblHeader.text() != "New Patient":
                self.query_update_patient_table()
                action = "updated"
            else:
                self.query_insert_patient_table()
                action = "added"

            patient_indication_id = self.query_get_patient_indication_ids()
            self.query_update_patientindication_table(patient_indication_id)

            message_box_critical(f"Patient profile has been {action}.")
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
    """Dialog window to display analytics"""
    def __init__(self, percent_ttr, total_days_in_ttr, total_days, total_tests, number_of_results_in_range):
        super(DlgAnalytics, self).__init__()
        width = 700
        height = 600
        self.setFixedSize(width, height)
        self.setWindowTitle("Analytics")
        self.lytMain = QVBoxLayout()

        # Create pie chart
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

        # Format pie chart
        self.pie_ttr.setLabelsVisible()
        self.pie_slice_ttr.setLabel(str(int(self.pie_slice_ttr.percentage() * 100)) +
                                    f"% TTR: {round(total_days_in_ttr)} days")
        self.pie_slice_ttr.setLabelColor(QColor("green"))
        self.pie_slice_not_ttr.setLabel(str(int(self.pie_slice_not_ttr.percentage() * 100)) +
                                        f"% Out of range: {round(total_days - total_days_in_ttr)} days")
        self.pie_slice_not_ttr.setLabelColor(QColor("red"))

        for slice in self.pie_ttr.slices():
            font = QtGui.QFont()
            font.setBold(True)
            font.setPixelSize(12)
            slice.setLabelFont(font)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create text edit widget for summary data
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
    """Dialog window for the clinic report"""
    def __init__(self, html):
        super(DlgReport, self).__init__()
        self.setupUi(self)
        header = """
        <h1>Clinic Report</h1>
        <br>
        """
        self.html = header + html

        # Event handlers for push buttons
        self.btnPDF.clicked.connect(self.evt_btn_pdf_clicked)
        self.btnPatientList.clicked.connect(self.evt_btn_patient_list_clicked)
        self.btnExit.clicked.connect(self.close)

    def evt_btn_pdf_clicked(self):
        """Create and save a PDF document"""
        document = QTextDocument()
        document.setHtml(self.html)
        printer = QPrinter()
        document.print_(printer)

    def evt_btn_patient_list_clicked(self):
        dlgPatientList = DlgPatientList()
        dlgPatientList.show()
        dlgPatientList.exec()


class DlgMessageBoxCritical(Ui_DlgMessageBoxCritical):
    """Dialog window for the clinic report"""
    def __init__(self):
        super(DlgMessageBoxCritical, self).__init__()
        self.setupUi(self)

        self.btnOk.setText("OK")
        self.btnOk.clicked.connect(self.close)


class DlgMessageBoxQuestion(Ui_DlgMessageBoxQuestion):
    """Dialog window for the clinic report"""
    def __init__(self):
        super(DlgMessageBoxQuestion, self).__init__()
        self.setupUi(self)


class DlgHelp(QDialog, Ui_DlgHelp):
    """Dialog window for the help document"""
    def __init__(self):
        super(DlgHelp, self).__init__()
        self.setupUi(self)

        # Event handler for push button
        self.btnExit.clicked.connect(self.close)


class DlgPatientList(QDialog, Ui_DlgPatients):
    """Dialog window for the patient list"""
    def __init__(self):
        super(DlgPatientList, self).__init__()
        self.setupUi(self)

        self.query_all_patients()

        # Event handler for push button
        self.btnExit.clicked.connect(self.close)
        self.rbtAll.clicked.connect(self.query_all_patients)
        self.rbtActive.clicked.connect(self.query_active_patients)
        self.rbtInactive.clicked.connect(self.query_inactive_patients)

    def query_all_patients(self):
        """Send a query to retrieve all patients"""
        query = QSqlQuery()
        bOk = query.exec("SELECT patient_id, lname, fname FROM patient")
        if bOk:
            self.populate_patient_list_table(query)

    def query_active_patients(self):
        """Send a query to retrieve only active patients"""
        print("Active")
        query = QSqlQuery()
        query.prepare("SELECT patient_id, lname, fname FROM patient WHERE status = :status")
        query.bindValue(":status", "A")
        bOk = query.exec()
        if bOk:
            self.populate_patient_list_table(query)

    def query_inactive_patients(self):
        """Send a query to retrieve only inactive patients"""
        query = QSqlQuery()
        query.prepare("SELECT patient_id, lname, fname FROM patient WHERE status = :status")
        query.bindValue(":status", "I")
        bOk = query.exec()
        if bOk:
            self.populate_patient_list_table(query)

    def populate_patient_list_table(self, query):
        """Populate the patient list table widget with information from the query"""
        self.tblPatientList.clearContents()
        self.tblPatientList.setRowCount(0)

        while query.next():
            row = self.tblPatientList.rowCount()
            self.tblPatientList.insertRow(row)
            for col in range(3):
                tbl_row_value = QTableWidgetItem((str(query.value(col))))
                self.tblPatientList.setItem(row, col, tbl_row_value)

        self.ledTotal.setText(str(self.tblPatientList.rowCount()))  # Total patient count for each category


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


def style_line_edit_error():
    """Create and return a CSS string for validation purposes"""
    sStyle = """
        QLineEdit {
            border: 1px solid red;
        }
    """

    return sStyle


def validate_new_indication(new_indication):
    """Validates line edit widget and returns an error message. Error message is blank if passes validation."""
    string_format = "^[\w() -]{2,}$"  # Allow words, spaces, hyphens, and parenthesis
    error_message = ""

    # Validate line edit widget
    if not re.match(string_format, new_indication):
        error_message += "Indication name can only contain words, spaces, hyphens, and parenthesis; must be " \
                         "at least 2 characters in length.\n"
    else:
        query = QSqlQuery()
        bOk = query.exec("SELECT indication_id, indication_name FROM indication")
        if bOk:
            all_indications = []
            while query.next():
                all_indications.append((query.value('indication_id'), query.value('indication_name')))

            # Check for duplicate entries
            for indication in all_indications:
                if new_indication == indication[1]:
                    error_message += "This indication already exists.\n"

    return error_message


def message_box_critical(msg):
    """Creates a dialog window showing a critical message"""
    msg_box = DlgMessageBoxCritical()
    msg_box.setWindowFlag(Qt.FramelessWindowHint)
    msg_box.setAttribute(Qt.WA_TranslucentBackground)
    msg_box.tedMessage.setText(msg)
    msg_box.show()
    msg_box.exec()


def message_box_question(msg):
    """Creates a dialog window asking for verification"""
    msg_box = DlgMessageBoxQuestion()
    msg_box.setWindowFlag(Qt.FramelessWindowHint)
    msg_box.setAttribute(Qt.WA_TranslucentBackground)
    msg_box.tedMsg.setText(msg)
    msg_box.btnDecline.clicked.connect(msg_box.done)
    return msg_box


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
