import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *


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
        mrn = self.ledMRN.text()
        if self.ledMRN.text() == "":
            QMessageBox.critical(self, "No MRN Entered", "Please enter a medical record number.")
        else:
            query = QSqlQuery()
            query.prepare("SELECT patient_id from patient WHERE patient_id = (:id)")
            query.bindValue(":id", mrn)
            query.exec_()
            query.next()

            if not query.isValid():
                QMessageBox.critical(self, "No Match Found", "The medical record number entered into the search "
                                                             "box does not match an existing record in the database.")

        self.ledMRN.clear()  # clear text box after searching


    def evt_actionExit_triggered(self):
        """
        Exit the program when user clicks on File > Exit
        """
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
