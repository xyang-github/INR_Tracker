import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *
from gui.patientprofile import *


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

        self.lst_patient_summary_info = self.populatePatientSummary(id)
        self.ledFirstName.setText(self.lst_patient_summary_info[0])
        self.ledLastName.setText(self.lst_patient_summary_info[1])
        self.ledDOB.setText(self.lst_patient_summary_info[2])
        self.ledIndications.setText(self.lst_patient_summary_info[6])
        self.ledGoal.setText(f"{self.lst_patient_summary_info[4]} - {self.lst_patient_summary_info[5]}")

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






if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
