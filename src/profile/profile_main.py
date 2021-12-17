import csv
import dateutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QListWidgetItem
from src.ui.patientprofile import Ui_DlgProfile
from src.message_boxes.format_msg import message_box_question
from src.profile.event import *
from src.profile.analytic import *
from src.profile.result import *
from src.profile.new_update_patient import *


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
        self.tblResult.setSelectionMode(1)

        # Event table widget formatting
        self.tblEvents.horizontalHeader().setStretchLastSection(True)
        self.tblEvents.setSelectionBehavior(QtWidgets.QTableWidget.SelectItems)
        self.tblEvents.setSelectionMode(1)

        # Populate patient summary, result and event tabs
        self.populate_patient_summary()
        self.populate_result_table()
        self.populate_event_table()
        self.if_no_indication_on_record()

        # Event handlers for result tab
        self.tblResult.itemDoubleClicked.connect(lambda: self.edit_result_dialog(self.tblResult.currentRow()))
        self.tblResult.selectionModel().selectionChanged.connect(self.display_result_comment_column)
        self.btnAddResult.clicked.connect(self.add_result_dialog)
        self.btnEditResult.clicked.connect(self.edit_result_dialog)
        self.btnDeleteResult.clicked.connect(self.delete_result)
        self.btnEditPatient.clicked.connect(self.edit_patient_dialog)
        self.btnExitProfile.clicked.connect(self.close)
        self.btnAnalytics.clicked.connect(self.show_analytics)
        self.btnCSV.clicked.connect(self.export_csv)
        self.btnPDF.clicked.connect(self.export_pdf)

        # Event handlers for the event tab
        self.tblEvents.itemDoubleClicked.connect(self.edit_event_dialog)
        self.tblEvents.selectionModel().selectionChanged.connect(self.display_event_comment_column)
        self.btnAddEvent.clicked.connect(self.add_event_dialog)
        self.btnEditEvent.clicked.connect(self.edit_event_dialog)
        self.btnDeleteEvent.clicked.connect(self.evt_btn_delete_event_clicked)

    def if_no_indication_on_record(self):
        """Show a message box and disables push buttons if no indication on record"""
        msg = "There is no indication on record for this patient. Please add an indication in order to add, " \
              "edit or delete any further results."

        if self.ledIndications.text() == "No Indication On Record":
            message_box_critical(msg)

            self.btnAddResult.setDisabled(True)
            self.btnEditResult.setDisabled(True)
            self.btnDeleteResult.setDisabled(True)
        else:
            self.btnAddResult.setDisabled(False)
            self.btnEditResult.setDisabled(False)
            self.btnDeleteResult.setDisabled(False)

    # Result Tab
    def add_result_dialog(self):
        """Create a dialog window to add new results to the result table widget and database"""
        dlgAddResult = DlgAddUpdateResult(self.mrn)
        dlgAddResult.show()
        dlgAddResult.exec_()
        self.populate_result_table()

    def edit_result_dialog(self, row=None):
        """Creates a dialog window to edit a result selected from the result table widget"""
        if self.tblResult.rowCount() == 0:
            message_box_critical("No entries to edit.")
            return
        else:
            self.current_selection_row = self.tblResult.currentRow()
            self.current_selection_inr_id = self.tblResult.item(self.current_selection_row, 0).text()

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
            dlgEditResult.rbtnGoalNew.setChecked(True)
            dlgEditResult.set_new_goal()
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
        dlgEditResult.btnOK.clicked.connect(dlgEditResult.update_result)

        dlgEditResult.show()
        dlgEditResult.exec_()
        self.populate_result_table()

    def delete_result(self):
        """Ask for verification to delete the selected row from the result table widget and database"""
        if self.tblResult.rowCount() == 0:
            message_box_critical("No entries to delete.")
            return

        self.question = message_box_question(f"You have selected row {self.current_selection_row + 1} to be deleted.")
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
                self.row = self.tblResult.rowCount()
                self.tblResult.insertRow(self.row)
                for col in range(6):
                    tbl_row_value = QTableWidgetItem(str(query.value(col)))
                    self.tblResult.setItem(self.row, col, tbl_row_value)

                    if col == 2:
                        self.tbl_result_col_value = QTableWidgetItem(str(query.value(col)))

                    if col == 3:
                        self.tbl_goal_col_value = QTableWidgetItem(str(query.value(col))).text()
                        self.inr_low = self.tbl_goal_col_value.split("-")[0].strip(" ")
                        self.inr_high = self.tbl_goal_col_value.split("-")[1].strip(" ")

                self.format_result_col()

            self.format_weekly_dose()
            self.format_goal()

        self.tblResult.setColumnHidden(0, True)  # Hide 'inr_id' column from view
        self.tblResult.setCurrentCell(0, 1)  # Set default selection to the most recent entry

    def format_result_col(self):
        """
        Format the background color of the result column in the result table widget. Green for therapeutic, yellow
        for subtherapeutic and red for supratherapeutic results.
        """
        if self.tbl_result_col_value.text() > self.inr_high:
            self.tblResult.item(self.row, 2).setBackground(QColor("#ff3300"))
        elif self.tbl_result_col_value.text() < self.inr_low:
            self.tblResult.item(self.row, 2).setBackground(QColor("#ffff00"))
        else:
            self.tblResult.item(self.row, 2).setBackground(QColor("#00ff80"))
            self.number_of_results_in_range += 1

    def format_weekly_dose(self):
        """
        Change the font formatting of the weekly dose column in the result table widget.  Formatting will be
        applied if the weekly dose has changed from the previous entry.
        """
        for i in range(self.tblResult.rowCount() - 1):
            self.current_weekly_dose = self.tblResult.item(i, 4)
            self.next_weekly_dose = self.tblResult.item(i+1, 4)

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
        for i in range(self.tblResult.rowCount() - 1):
            self.current_inr_goal = self.tblResult.item(i, 3)
            self.next_inr_goal = self.tblResult.item(i+1, 3)

            if self.current_inr_goal.text() != self.next_inr_goal.text():
                font = QtGui.QFont()
                font.setBold(True)
                self.current_inr_goal.setFont(font)
                self.current_inr_goal.setForeground(QBrush(QColor("darkMagenta")))

    def display_result_comment_column(self, selected):
        """Display a dialog box containing comments if the comment column if the result table is filled"""
        self.current_selection_row = self.tblResult.currentRow()
        self.current_selection_comment = self.tblResult.item(self.current_selection_row, 5).text()

        for i in selected.indexes():
            if i.column() == 5 and self.current_selection_comment:
                self.current_selection_comment = f"<b>Comment:</b> <br>" \
                                                 f"{self.tblResult.item(self.current_selection_row, 5).text()}"
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

    def edit_patient_dialog(self):
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

    def show_analytics(self):
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

            date_range = [6, 12, 'all']
            number_of_events = []
            for date in date_range:
                if date == 'all':
                    query = QSqlQuery()
                    query.prepare("SELECT COUNT(*) AS total FROM patient_event WHERE patient_id = :id")
                    query.bindValue(":id", int(self.mrn))
                    bOk = query.exec()
                    if bOk:
                        query.next()
                        number_of_events.append(query.value('total'))
                else:
                    today = datetime.date.today()
                    delta = dateutil.relativedelta.relativedelta(months=date)
                    date_limit = today - delta

                    query = QSqlQuery()
                    query.prepare("SELECT COUNT(*) AS total FROM patient_event WHERE patient_id = :id AND date >= :date")
                    query.bindValue(":id", int(self.mrn))
                    query.bindValue(":date", str(date_limit))
                    bOk = query.exec()
                    if bOk:
                        query.next()
                        number_of_events.append(query.value('total'))

            dlgAnalytics = DlgAnalytics(percent_ttr, self.days_in_ttr, self.total_days,
                                        self.total_rows, self.number_of_results_in_range, number_of_events)
            dlgAnalytics.show()
            dlgAnalytics.exec_()

    def export_csv(self):
        """Save the result table widget to a csv file"""
        column_header = []
        for col in range(1, self.tblResult.columnCount()):
            column_header.append(self.tblResult.horizontalHeaderItem(col).text())

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

    def export_pdf(self):
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
        results and events will be disabled"""
        if self.ledStatus.text() == "Inactive":
            self.btnAddResult.setDisabled(True)
            self.btnEditResult.setDisabled(True)
            self.btnDeleteResult.setDisabled(True)
            self.btnAddEvent.setDisabled(True)
            self.btnEditEvent.setDisabled(True)
            self.btnDeleteEvent.setDisabled(True)
            self.lblNotice.setText("This patient's status is currently INACTIVE. Only ACTIVE patients can have "
                                   "results and events added,\n edited, and deleted.")
        else:
            self.lblNotice.setText("")
            self.btnAddResult.setDisabled(False)
            self.btnEditResult.setDisabled(False)
            self.btnDeleteResult.setDisabled(False)
            self.btnAddEvent.setDisabled(False)
            self.btnEditEvent.setDisabled(False)
            self.btnDeleteEvent.setDisabled(False)

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

    def add_event_dialog(self):
        dlgAddEvent = DlgAddEditEvent(self.mrn)
        dlgAddEvent.show()
        dlgAddEvent.btnOK.clicked.connect(dlgAddEvent.add_to_database)
        dlgAddEvent.exec()
        self.populate_event_table()

    def edit_event_dialog(self):
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
        self.dlgEditEvent.btnAddToEventList.setDisabled(True)
        self.dlgEditEvent.btnAddToPatient.setDisabled(True)
        self.dlgEditEvent.btnRemoveFromPatient.setDisabled(True)

        # Event handler for push button when editing an event entry
        self.dlgEditEvent.btnOK.clicked.connect(self.evt_btn_update_event_clicked)

        self.dlgEditEvent.show()
        self.dlgEditEvent.exec()
        self.populate_event_table()

    def evt_btn_update_event_clicked(self):
        """Update the comment column. Date, event id and patient id are composite primary keys"""
        msg = "Record updated."
        query1 = QSqlQuery()
        query1.prepare("SELECT event_id FROM patient_event WHERE patient_id = :id AND date = :date_event")
        query1.bindValue(":id", int(self.mrn))
        query1.bindValue(":date_event", self.date)
        bOk = query1.exec()
        if bOk:
            while query1.next():
                query2 = QSqlQuery()
                query2.prepare("UPDATE patient_event SET comment = :comment WHERE date = :date AND patient_id = "
                               ":patient_id AND event_id = :event_id")
                query2.bindValue(":comment", self.dlgEditEvent.txtComment_event.toPlainText())
                query2.bindValue(":date", self.date)
                query2.bindValue(":patient_id", int(self.mrn))
                query2.bindValue(":event_id", int(query1.value('event_id')))

                bOk = query2.exec()
                if not bOk:
                    msg = "Not able to update record."

        message_box_critical(msg)

        self.dlgEditEvent.close()

    def evt_btn_delete_event_clicked(self):
        """Ask for verification to delete the selected row from the events table widget and database"""

        # Check if there is any item in the event table widget to edit
        if self.tblEvents.rowCount() == 0:
            message_box_critical("No entries to delete.")
            return

        # Check if a selection has been made to edit
        if not self.tblEvents.selectedItems():
            message_box_critical("No entry selected to delete.")
            return

        # Retrieve information from the selected row
        row = self.tblEvents.currentRow()
        self.date = self.tblEvents.item(row, 0).text()
        self.event_name = self.tblEvents.item(row, 1).text()

        query = QSqlQuery()
        query.prepare("SELECT event_id from event WHERE event_name = :name")
        query.bindValue(":name", self.event_name)
        query.exec()
        query.next()
        self.event_id = query.value('event_id')

        # Ask for verification to delete record
        self.question = message_box_question(f"You have selected row {row + 1} to be deleted.")

        # Event handler to delete record from the result table and database
        self.question.btnAccept.clicked.connect(self.query_delete_event)

        self.question.show()
        self.question.exec_()

        self.populate_event_table()

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

        # Make duplicate comments not visible
        count = self.tblEvents.rowCount()
        for i in range(count-1):
            if self.tblEvents.item(i, 2).text() == self.tblEvents.item(i+1, 2).text():
                self.tblEvents.item(i+1, 2).setForeground(QColor("white"))

    def display_event_comment_column(self, selected):
        """Display a dialog box containing comments if the comment column if the result table is filled"""
        self.current_selection_row = self.tblEvents.currentRow()
        self.current_selection_comment = self.tblEvents.item(self.current_selection_row, 2).text()

        for i in selected.indexes():
            if i.column() == 2 and self.current_selection_comment:
                message_box_critical("<b>Comment:</b><br>" + self.current_selection_comment)
                self.tblEvents.selectionModel().clearSelection()
                return  # prevent duplicate message boxes for merged comment fields

    def query_delete_event(self):
        """Query a request to delete record from the database"""
        query = QSqlQuery()
        query.prepare("DELETE FROM patient_event WHERE date = :event_date AND event_id = :event_id "
                      "AND patient_id = :patient_id")
        query.bindValue(":event_date", self.date)
        query.bindValue(":event_id", int(self.event_id))
        query.bindValue(":patient_id", int(self.mrn))
        bOk = query.exec()
        if bOk:
            self.question.close()
            message_box_critical("Record deleted.")

        self.question.close()  # close dialog box