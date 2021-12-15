from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from src.gui.patientlist import Ui_DlgPatients


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