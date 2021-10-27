import re
from main_ui import Ui_MainWindow
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


con = sqlite3.connect('inr_database.db')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushEnter.clicked.connect(self.search_patient)

    def validate_mrn(self, candidate):
        """
        :param candidate: the value typed into the MRN textbox
        :return: a message box if invalid entry, or no matching record found
        """
        if re.match("[^0-9]+", candidate):
            QMessageBox.warning(None, "Error", "Only enter the numeric medical record number.")

        return candidate

    def search_patient(self):
        """
        Takes a valid medical record number, and select a matching entry from the database
        """
        patient_mrn = int(self.validate_mrn(self.textMRN.text()))
        cur = con.cursor()
        cur.execute("select * from patient where patient_id = ?;", (patient_mrn,))
        print(cur.fetchone())


if __name__ == "__main__":
    myapp = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(myapp.exec_())
