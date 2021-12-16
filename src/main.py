import sys
import dateutil
from dateutil.relativedelta import relativedelta
from PyQt5.QtSql import *
from ui.main_ui import *
from ui.message_box_critical import *
from ui.add_update_event import *
from src.clinic.help import *
from src.clinic.indications import *
from src.clinic.report import *
from src.profile.profile_main import *


class DlgMain(QMainWindow, Ui_dlgMain):
    """Main window for application"""
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # Create database connection
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("../data/inr_tracker.db")
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
        dlgReport = DlgReport()
        dlgReport.show()
        dlgReport.exec_()

    def evt_action_help_triggered(self):
        html = self.get_html_help()

        dlgHelp = DlgHelp()
        dlgHelp.tbrDocument.setHtml(html)
        dlgHelp.adjustSize()
        dlgHelp.show()
        dlgHelp.exec_()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
