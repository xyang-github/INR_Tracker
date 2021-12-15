import datetime
import re
from decimal import Decimal

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog

from src.gui.newpatient import Ui_DlgNewPatient
from src.validate import validate_new_indication
from src.style import style_line_edit_error
from src.message_boxes.format_msg import message_box_critical


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