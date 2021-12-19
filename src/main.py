import sys
import dateutil
from dateutil.relativedelta import relativedelta
from PyQt5.QtSql import *
from ui.main_ui import *
from ui.message_box_critical import *
from src.clinic.help import *
from src.clinic.indications import *
from src.clinic.report import *
from src.profile.profile_main import *
from src.clinic.events import *


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
        self.menuExit.triggered.connect(self.exit_program)
        self.menuNewPatient.triggered.connect(self.add_new_patient_dialog)
        self.menuIndications.triggered.connect(self.indication_dialog)
        self.menuEvents.triggered.connect(self.event_dialog)
        self.menuReports.triggered.connect(self.reports_dialog)
        self.menuHelpDialog.triggered.connect(self.help_dialog)
        self.btnSearchPatient.clicked.connect(self.search_patient)
        self.btnNewPatient.clicked.connect(self.add_new_patient_dialog)
        self.btnIndications.clicked.connect(self.indication_dialog)
        self.btnEvents.clicked.connect(self.event_dialog)
        self.btnReports.clicked.connect(self.reports_dialog)

    def search_patient(self):
        """Searches for a matching patient in the database, and creates a patient profile dialog"""
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

    def exit_program(self):
        """Closes the main application"""
        sys.exit(app.exec_())

    def add_new_patient_dialog(self):
        """Creates a new patient dialog window"""
        dlgNewPatient = DlgNewUpdatePatient()
        dlgNewPatient.rbtnStatusInactive.setEnabled(False)  # Cannot add inactive patients
        dlgNewPatient.show()
        dlgNewPatient.exec_()
        dlgNewPatient.populate_indication_list()

    def indication_dialog(self):
        """Create a dialog window to add/edit/delete indication list"""
        dlgIndications = DlgIndications()
        dlgIndications.show()
        dlgIndications.exec_()

    def event_dialog(self):
        """Careate a dialog window to add/edit/delete event list"""
        dlgEvents = DlgEvents()
        dlgEvents.show()
        dlgEvents.exec_()

    def reports_dialog(self):
        """Create a dialog window for the clinic report"""
        dlgReport = DlgReport()
        dlgReport.show()
        dlgReport.exec_()

    def help_dialog(self):
        """Create a dialog window for help information"""
        html = self.get_html_help()

        dlgHelp = DlgHelp()
        dlgHelp.tbrDocument.setHtml(html)
        dlgHelp.adjustSize()
        dlgHelp.show()
        dlgHelp.exec_()

    def get_html_help(self):
        """Create and return an HTML string for the help document"""
        html = """
<center><img src="../resource/screenshot/main.JPG"></center>

    <h2>Introduction</h2>
    <p>INR Tracker is a comprehensive desktop application intended to assist with the management of anticoagulation clinics.
Specifically, for patients on warfarin. Overall, this application can create patient profiles, tracking of INR results,
    record clinically significant events, and to derive metrics from data.</p>

    <p>All information is stored locally in a relational database called <b>inr_tracker.db</b>. <i>Deleting or moving
        this file will erase all records.</i></p>

<p>Each patient has an <b>identifier</b>, which will be referred to as a medical record number (MRN). The MRN is added
upon creation of a new patient profile. The MRN cannot be changed later. If an MRN is on record, the patient profile
    will be displayed.</p>

<hr>

<h2>Creating a new patient profile</h2>

<center><img src="../resource/screenshot/new patient.jpg"></center>
<ul>
    <li>From the main window, click on the "New Patient" button. A New Patient dialog will appear.</li>
    <li>Enter the requested information: medical record number, first name, last name, date of birth (YYYY-MM-DD),
        indications and INR goal. Note that the anticoagulation status can only be Active for new patients.</li>
    <li>New indications can be entered where prompted, or from the main menu.</li>
    <li>Invalid entries in any of the text boxes, or failure to enter at least one indication, will cause an error
        message to appear.</li>
</ul>

<h2>Patient Profile - Summary Tab</h2>
<center><img src="../resource/screenshot/patient profile.JPG"></center>

<ul>
    <li>From the main window, a medical record number can be entered and searched for. If a matching record is found, the patient profile will appear.</li>
    <li>Patient profiles are organized into tabs:
    <ul>
        <li>Summary - display a summary of information; contains various patient functions</li>
        <li>Results - display, add, edit and delete INR results</li>
        <li>Events - display, add, edit and delete clinically significant events</li>
    </ul></li>
</ul>

<p>Other functionalities include the following:</p>
<ul>
    <li>Edit Patient</li>
    <li>Analytics</li>
    <li>Export to PDF</li>
    <li>Export to CSV</li>
</ul>

<hr>

<h2>Patient Profile - Editing</h2>
<center><img src="../resource/screenshot/patient_profile_update.JPG"></center>
<p>
    The patient profile can also be edited, <b>with the exception of the medical record number</b>. Changing the status
to inactive will disable the ability to add, edit or delete results and events. Note that the INR goal in the patient
profile should not be changed for temporary changes in the goal (e.g. a lower goal for an upcoming procedure).
Instead, a different INR goal can be provided when entering or editing a result.
</p>

<hr>

<h2>Patient Analytics</h2>
<center><img src="../resource/screenshot/patient analytics.JPG"></center>
<p>
Analytics can be produced if patient has at least two results on record. The TTR is calculated using the Rosendaal
linear interpolation method. Other information includes total days on record, days within range, percent of days
within range, total number of tests, number of tests in range, and percent of test in range. The number of clinical
events is also displayed for the past 6 months, 12 months, and all time.
</p>

<hr>

<h2>Export To PDF</h2>
<center><img src="../resource/screenshot/patient pdf.JPG"></center>
<p>
A summary report can be saved for each patient. This report can be provided at the request of medical facilities
    requesting for records.
</p>

<hr>

<h2>Patient Profile - Results Tab</h2>
<center><img src="../resource/screenshot/patient results.JPG"></center>
<p>The Results tab will display a table of results in the database. The information displayed are Date, INR, Goal,
    Total Dose (in milligrams) and Comment. </p>

<p>The INR column will be colored depending if the result is within goal,
    supratherapeutic or subtherapeutic. The goal defaults to the INR goal established in the patient profile, but a
    different goal can be specified for any specific result.</p>

<p>A single click in the Comment column will display the comment in a pop-up dialog window if the cell is not empty.
</p>

<p>A double click on any of the other columns (or an empty Comment column) will automatically produce a dialog window to
    update the result.</p>

<hr>

<h2>Add/Update Result</h2>
<center><img src="../resource/screenshot/add result.JPG">
<img src="../resource/screenshot/edit result.jpg"></center>
<ul>
    <li>When adding a result to the patient’s profile, a dialog window will appear. The date is defaulted to the
        current date, but can be changed.</li>
    <li>Clicking the “No Changes” checkbox will pre-populate the dose with the most recent regimen on file. </li>
    <li>The INR goal will also default to the goal that has been entered for the patient, but a new INR can be
        specified in certain cases (e.g. a lower goal for a procedure). </li>
    <li>A comment can be entered.</li>
</ul>

<hr>

<h2>Patient Profile - Events Tab</h2>
<center>
<img src="../resource/screenshot/event.JPG">
<img src="../resource/screenshot/add event.jpg">
<img src="../resource/screenshot/edit event.jpg"></center>

<p>The Events tab will display a table of events in the database. The information displayed are Date, Clinical Event,
    and Comment.</p>
<p>If more than one event is entered per date, the comment will only appear once instead of for each individual event.
    When editing events, only the comment can be changed. If anything else needs to be changed, it is best to delete
    the event and re-enter with the updated information.</p>

<hr>

<h2>Indications</h2>
<center><img src="../resource/screenshot/indication.JPG"></center>
<p>Displays all the indications entered. Indications can be added, edited or deleted from this window. It is best to avoid
    abbreviations (e.g. afib, dvt, pe). It is best to denote treatment versus prophylaxis in parentheses. For example:
    "pulmonary embolism (treatment)" and "pulmonary embolism (prophylaxis)."</p>

<hr>

<h2>Events</h2>
<center><img src="../resource/screenshot/event_list"></center>
<p>Displays all the events entered. Events can be added, edited or deleted from this window.</p>

<hr>

<h2>Clinic Summary</h2>
<center><img src="../resource/screenshot/clinic report.JPG"></center>
<p>A clinic report can be generated with certain metrics. These metrics can be toggled between All patients, Active 
    patients and Inactive patients. The information can also be exported to a PDF format if desired.</p>
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
        bOk = query.exec_(command)
        if bOk:
            default_indications = [
                "atrial fibrillation",
                "aortic valve replacement",
                "mitral valve replacement",
                "pulmonary embolism (treatment)",
                "pulmonary embolism (prophylaxis)",
                "venous thromboembolism (treatment)",
                "venous thromboembolism (prophylaxis)"
            ]
            for indication in default_indications:
                query = QSqlQuery()
                command = "INSERT INTO indication ('indication_name') VALUES (:indication)"
                query.prepare(command)
                query.bindValue(":indication", indication)
                query.exec()

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
        bOk = query.exec_(command)
        if bOk:
            default_events = [
                "bleeding (clinically-significant)",
                "stroke or thromboembolism",
                "emergency or urgent department visit",
                "hospitalization",
                "death"
            ]

            for event in default_events:
                query = QSqlQuery()
                command = "INSERT INTO event ('event_name') VALUES (:event)"
                query.prepare(command)
                query.bindValue(":event", event)
                query.exec()

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

    font_database = QFontDatabase()
    font_database.addApplicationFont(":/tff/font/Righteous-Regular.ttf")
    font_database.addApplicationFont(":/tff/font/Raleway-Regular.ttf")
    font_database.addApplicationFont(":/tff/font/SourceSansPro-Regular.ttf")

    dlgMain.show()
    sys.exit(app.exec_())
