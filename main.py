import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *
from gui.patientprofile import *


class DlgMain(QMainWindow, Ui_dlgMain):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # event handlers
        self.actionExit.triggered.connect(self.evt_actionExit_triggered)  # exit signal
        self.btnSearch.clicked.connect(self.evt_btnSearch_clicked)


    def evt_btnSearch_clicked(self):
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
    def __init__(self, id):
        super(DlgPatientProfile, self).__init__()
        self.setupUi(self)
        self.lst_patient_summary_info = self.populatePatientSummary(id)

        self.ledFirstName.setText(self.lst_patient_summary_info[0])

    def populatePatientSummary(self, id):
        """
        :param id:  the medical record number for patient
        :return:  a list of values in the patient table
        """
        query = QSqlQuery()
        bOk = query.exec("SELECT fname, lname, dob, status, inr_goal_from, inr_goal_to from patient WHERE patient_id = {}".format(id))
        if bOk:
            query.next()
            if query.isValid():
                return ([query.value('fname'), query.value('lname'), query.value('dob'), query.value('status'), query.value('inr_goal_from'), query.value('inr_goal_to')])






if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
