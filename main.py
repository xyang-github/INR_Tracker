import sys

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
        self.actionExit.triggered.connect(self.evt_actionExit_triggered)
        self.btnSearch.clicked.connect(self.evt_btnSearch_clicked)

    def evt_btnSearch_clicked(self):
        """
        Creates database connection when the search button is clicked
        """
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("database.db")
        if self.database.open():
            self.searchPatient()
        else:
            QMessageBox.critical(self, "Database Error", "Could not connect with the database.")

    def searchPatient(self):
        """
        Find a match in the database with the provided MRN. Will show message boxes for errors.
        """
        self.mrn = self.ledMRN.text()
        if self.ledMRN.text() == "":
            QMessageBox.critical(self, "No MRN Entered", "Please enter a medical record number.")
        else:
            query = QSqlQuery()
            query.prepare("SELECT patient_id from patient WHERE patient_id = (:id)")
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


    def evt_actionExit_triggered(self):
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
        self.lst_patient_summary_info = self.populatePatientSummary(self.mrn)
        self.ledFirstName.setText(self.lst_patient_summary_info[0])
        self.ledLastName.setText(self.lst_patient_summary_info[1])
        self.ledDOB.setText(self.lst_patient_summary_info[2])
        self.ledIndications.setText(self.lst_patient_summary_info[6])
        self.ledGoal.setText(f"{self.lst_patient_summary_info[4]} - {self.lst_patient_summary_info[5]}")
        self.lblName.setText(f"{self.lst_patient_summary_info[1]}, {self.lst_patient_summary_info[0]}")

        # Event handlers
        self.btnAdd.clicked.connect(self.evt_addResult_clicked)

    def populatePatientSummary(self, id):
        """
        :param id:  the medical record number for patient
        :return:  a list of values in the patient table
        """
        query = QSqlQuery()
        bOk = query.exec("SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to, indication_name FROM patient p JOIN patient_indication pi ON p.patient_id = pi.patient_id JOIN indication i ON pi.indication_id = i.indication_id WHERE p.patient_id = {}".format(id))
        if bOk:
            query.next()
            if query.isValid():
                return ([query.value('fname'), query.value('lname'), query.value('dob'), query.value('status'), query.value('inr_goal_from'), query.value('inr_goal_to'), query.value('indication_name')])

    def evt_addResult_clicked(self):
        dlgAddResult = DlgAddResult(self.mrn)
        dlgAddResult.show()
        dlgAddResult.exec_()


class DlgAddResult(QDialog, Ui_DlgAddResult):
    """
    Dialog box for adding INR result to database
    """
    def __init__(self, id):
        super(DlgAddResult, self).__init__()
        self.setupUi(self)
        self.dteDate.setDate(QDate.currentDate())
        self.ledResult.setFocus()
        self.mrn = id  # patient MRN for use in query

        self.btnOK.clicked.connect(self.evt_acceptResults_clicked)
        self.chkNoChanges.clicked.connect(self.evt_noChanges_clicked)

    def evt_acceptResults_clicked(self):
        self.result = self.ledResult.text()


    def evt_noChanges_clicked(self, chk):
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
            bOk = query.exec(f"SELECT * FROM patient JOIN inr ON patient.patient_id = inr.patient_id WHERE patient.patient_id = {self.mrn} ORDER BY date DESC LIMIT 1")
            if bOk:
                query.next()
                if query.isValid():  # False for some reason, seems like query is not pulling up data
                    self.ledMonday.setText(query.value('dose_mon'))
                    self.ledTuesday.setText(query.value('dose_tue'))
                    self.ledWednesday.setText(query.value('dose_wed'))
                    self.ledThursday.setText(query.value('dose_thu'))
                    self.ledFriday.setText(query.value('dose_fri'))
                    self.ledSaturday.setText(query.value('dose_sat'))
                    self.ledSunday.setText(query.value('dose_sun'))
                else:
                    QMessageBox.critical(self, "Error", "No previous doses detected on record.")
                    self.chkNoChanges.setChecked(False)




    def calculateTotal(self):
        pass







if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
