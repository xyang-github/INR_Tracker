import datetime
import dateutil
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from src.ui.report import *
from src.clinic.patient_list import *


class DlgReport(QDialog, Ui_DlgReport):
    """Dialog window for the clinic report"""
    def __init__(self):
        super(DlgReport, self).__init__()
        self.setupUi(self)

        self.get_html_clinic_report()

        # Event handlers for push buttons
        self.btnPDF.clicked.connect(self.export_pdf)
        self.btnPatientList.clicked.connect(self.patient_list_dialog)
        self.btnExit.clicked.connect(self.close)

        # Event handlers for radio buttons
        self.rbtnAllPatients.clicked.connect(lambda toggle="All": self.get_html_clinic_report(toggle="All"))
        self.rbtnActivePatients.clicked.connect(lambda toggle="Active": self.get_html_clinic_report(toggle="Active"))
        self.rbtnInactivePatients.clicked.connect(
            lambda toggle="Inactive": self.get_html_clinic_report(toggle="Inactive")
        )

    def export_pdf(self):
        """Create and save a PDF document"""
        header = f"""
        <h1 style="text-align: center;">Clinic Report</h1>
        <h3 style="text-align: center;">Date: {QDate.currentDate().toString("yyyy-MM-dd")}<br></h3>
        """

        if self.rbtnAllPatients.isChecked():
            header += "<h3 style='text-align: center;'>All Patients</h3>"
        if self.rbtnActivePatients.isChecked():
            header += "<h3 style='text-align: center;'>Active Patients Only</h3>"
        if self.rbtnInactivePatients.isChecked():
            header += "<h3 style='text-align: center;'>Inactive Patients Only</h3>"

        document = QTextDocument()
        document.setHtml(header + self.html)
        printer = QPrinter()
        document.print_(printer)

    def patient_list_dialog(self):
        """Create a dialog window to display a patient list"""
        dlgPatientList = DlgPatientList()
        dlgPatientList.show()
        dlgPatientList.exec()

    def get_html_clinic_report(self, toggle="Active"):
        """Create and return an HTML string for the clinic report"""

        # Retrieve number of active patients
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) AS total FROM patient WHERE status = :status")
        query.bindValue(":status", "A")
        query.exec()
        query.next()
        total_actives = query.value('total')

        # Retrieve number of inactive patients
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) AS total FROM patient WHERE status = :status")
        query.bindValue(":status", "I")
        query.exec()
        query.next()
        total_inactives = query.value('total')

        # Retrieve total number of patients
        query = QSqlQuery()
        query.exec("SELECT COUNT(*) AS total FROM patient")
        query.next()
        total_all_patients = query.value('total')
        self.html = f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style = "background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">Patient Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td><strong>Total Patients:</strong></td>
                    <td>{total_all_patients}</td>
                </tr>
                <tr>
                    <td><strong>Active Patients:</strong></td>
                    <td>{total_actives}</td>
                </tr>
                <tr>
                    <td><strong>Inactive Patients:</strong></td>
                    <td>{total_inactives}</td>
                </tr>
            </table>
        </div>
        &nbsp;<br>
        """

        # Retrieve breakdown of indications
        list_indications = []
        if toggle == "All":
            query = self.query_indications_all_patients()
        if toggle == "Active":
            query = self.query_indications_active_patients()
        if toggle == "Inactive":
            query = self.query_indications_inactive_patients()

        total = 0
        while query.next():
            total += query.value('total')
            list_indications.append((query.value('indication_name'), query.value('total')))

        list_indications.sort()

        self.html += f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style = "background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">
            Indication Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td style="width: 150px"><strong>Total Indications:</strong></td>
                    <td>{total}</th>
                </tr>
        """
        for indication in list_indications:
            self.html += f"""
            <tr>
                <td>{indication[0]}</td>
                <td>{indication[1]}</td>
            </tr>
            """
        self.html += """
            </table>
        </div>
        &nbsp;<br>
        """

        # Retrieve breakdown of INR goals
        list_goals = []
        if toggle == "All":
            query = self.query_goal_all_patients()
        if toggle == "Active":
            query = self.query_goal_active_patients()
        if toggle == "Inactive":
            query = self.query_goal_inactive_patients()

        total = 0
        while query.next():
            total += query.value('total')
            list_goals.append((query.value('goal'), query.value('total')))

        list_goals.sort()

        self.html += f"""
        <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; border-color: gray">
            <h3 style="background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">Goal Metrics</h3>
            <table cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                <tr>
                    <td style="width: 150px"><strong>Total Goals:</strong></th>
                    <td>{total}</th>
                </tr>
        """
        for goal in list_goals:
            self.html += f"""
                <tr>
                    <td>{goal[0]}</td>
                    <td>{goal[1]}</td>
                </tr>
            """
        self.html += """
            </table>
            </div>
                <div style="font-family: arial; border-style: solid; border-radius: 15px; padding: 10px; 
                border-color: gray">
                    <h3 style = "background-color: #04AA6D; color: white; margin-top: 5px; margin-bottom: 10px">
                    Clinical Events Metrics</h3>
                    <table width="100%" cellpadding=5 cellspacing=5 style="border: none; border-collapse: collapse">
                """

        # Retrieve clinical events in the past 6 months, 12 months, and all time for ALL patients
        date_range = [6, 12, 'all']
        if toggle == "All":
            for date in date_range:
                if date == 'all':
                    number_of_events = []  # Resets the list for each iteration
                    command = """
                    SELECT COUNT(*) AS total, e.event_name FROM patient p JOIN patient_event pe 
                    ON p.patient_id = pe.patient_id JOIN event e ON pe.event_id = e.event_id 
                    GROUP BY event_name ORDER BY event_name ASC
                    """

                    query = QSqlQuery()
                    bOk = query.exec(command)
                    if bOk:
                        while query.next():
                            number_of_events.append((query.value('total'), query.value('event_name')))

                        count_events = 0
                        breakdown_stats = "<ul>"
                        for i in range(len(number_of_events)):
                            count_events += number_of_events[i][0]
                            breakdown_stats += f"<li>{number_of_events[i][1]}: {number_of_events[i][0]}</li>"
                        breakdown_stats += "</ul>"

                        self.html += f"""
                                <tr>
                                    <td width="50%"><strong>Number of events,</strong> {date} months:</td>
                                    <td>{count_events}</td>
                                </tr>
                                <tr>
                                    <td colspan='2'>{breakdown_stats}</td>
                                </tr>
                            """
                else:
                    number_of_events = []
                    today = datetime.date.today()
                    delta = dateutil.relativedelta.relativedelta(months=date)
                    date_limit = today - delta
                    command = """
                    SELECT COUNT(*) AS total, e.event_name FROM patient p JOIN patient_event pe 
                    ON p.patient_id = pe.patient_id JOIN event e ON pe.event_id = e.event_id 
                    GROUP BY event_name HAVING pe.date > :date ORDER BY event_name ASC
                    """

                    query = QSqlQuery()
                    query.prepare(command)
                    query.bindValue(":date", str(date_limit))
                    bOk = query.exec()
                    if bOk:
                        while query.next():
                            number_of_events.append((query.value('total'), query.value('event_name')))

                    count_events = 0
                    breakdown_stats = "<ul>"
                    for i in range(len(number_of_events)):
                        count_events += number_of_events[i][0]
                        breakdown_stats += f"<li>{number_of_events[i][1]}: {number_of_events[i][0]}</li>"
                    breakdown_stats += "</ul>"

                    self.html += f"""
                            <tr>
                                <td width="50%"><strong>Number of events,</strong> {date} months:</td>
                                <td>{count_events}</td>
                            </tr>
                            <tr>
                                <td colspan='2'>{breakdown_stats}</td>
                            </tr>
                        """

        # Retrieve clinical events in the past 6 months, 12 months, and all time for Active or Inactive patients
        if toggle == "Active" or toggle == "Inactive":
            status = toggle
            for date in date_range:
                if date == 'all':
                    number_of_events = []  # Resets the list for each iteration
                    query = QSqlQuery()
                    command = """
                    SELECT COUNT(*) AS total, e.event_name FROM patient p JOIN patient_event pe 
                    ON p.patient_id = pe.patient_id JOIN event e ON pe.event_id = e.event_id 
                    GROUP BY event_name HAVING p.status = :status ORDER BY event_name ASC
                    """

                    query.prepare(command)
                    query.bindValue(":status", status[0])
                    bOk = query.exec()
                    if bOk:
                        while query.next():
                            number_of_events.append((query.value('total'), query.value('event_name')))

                    count_events = 0
                    breakdown_stats = "<ul>"
                    for i in range(len(number_of_events)):
                        count_events += number_of_events[i][0]
                        breakdown_stats += f"<li>{number_of_events[i][1]}: {number_of_events[i][0]}</li>"
                    breakdown_stats += "</ul>"

                    self.html += f"""
                            <tr>
                                <td width="50%"><strong>Number of events,</strong> {date} months:</td>
                                <td>{count_events}</td>
                            </tr>
                            <tr>
                                <td colspan='2'>{breakdown_stats}</td>
                            </tr>
                        """
                else:
                    number_of_events = []  # Resets the list for each iteration
                    today = datetime.date.today()
                    delta = dateutil.relativedelta.relativedelta(months=date)
                    date_limit = today - delta
                    command = """
                    SELECT COUNT(*) AS total, e.event_name FROM patient p JOIN patient_event pe 
                    ON p.patient_id = pe.patient_id JOIN event e ON pe.event_id = e.event_id 
                    GROUP BY event_name HAVING p.status = :status AND pe.date > :date ORDER BY event_name ASC
                    """

                    query = QSqlQuery()
                    query.prepare(command)
                    query.bindValue(":date", str(date_limit))
                    query.bindValue(":status", status[0])
                    bOk = query.exec()
                    if bOk:
                        while query.next():
                            number_of_events.append((query.value('total'), query.value('event_name')))

                    count_events = 0
                    breakdown_stats = "<ul>"
                    for i in range(len(number_of_events)):
                        count_events += number_of_events[i][0]
                        breakdown_stats += f"<li>{number_of_events[i][1]}: {number_of_events[i][0]}</li>"
                    breakdown_stats += "</ul>"

                    self.html += f"""
                            <tr>
                                <td width="50%"><strong>Number of events,</strong> {date} months:</td>
                                <td>{count_events}</td>
                            </tr>
                            <tr>
                                <td colspan='2'>{breakdown_stats}</td>
                            </tr>
                        """

        self.html += """
            </table>
            </div>
        """

        self.populate_clinic_report()

    def populate_clinic_report(self):
        """Set the html string as output for the text edit widget"""
        self.tedReport.setHtml(self.html)

    def query_indications_all_patients(self):
        """Create and return a query for indications of all patients"""
        query = QSqlQuery()
        query.exec("SELECT COUNT(i.indication_id) AS total, indication_name FROM indication i "
                   "JOIN patient_indication pi ON i.indication_id = pi.indication_id GROUP BY indication_name "
                   "ORDER BY indication_name DESC")
        query.exec()
        return query

    def query_indications_inactive_patients(self):
        """Create and return a query for indications of inactive patients only"""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(i.indication_id) AS total, indication_name FROM indication i "
                   "JOIN patient_indication pi ON i.indication_id = pi.indication_id "
                   "JOIN patient p ON pi.patient_id = p.patient_id "
                   "GROUP BY indication_name HAVING status = :status ORDER BY indication_name DESC")
        query.bindValue(":status", "I")
        query.exec()
        return query

    def query_indications_active_patients(self):
        """Create and return a query for indications of active patients only"""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(i.indication_id) AS total, indication_name FROM indication i "
                   "JOIN patient_indication pi ON i.indication_id = pi.indication_id "
                   "JOIN patient p ON pi.patient_id = p.patient_id "
                   "GROUP BY indication_name HAVING status = :status ORDER BY indication_name DESC")
        query.bindValue(":status", "A")
        query.exec()
        return query

    def query_goal_all_patients(self):
        """Create and return a query for goals of all patients"""
        query = QSqlQuery()
        query.exec("SELECT COUNT(inr_goal_from || '-' || inr_goal_to) AS total, (inr_goal_from || '-' || inr_goal_to) "
                   "AS goal FROM patient GROUP BY goal")
        return query

    def query_goal_active_patients(self):
        """Create and return a query for goals of active patients only"""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(inr_goal_from || '-' || inr_goal_to) AS total, "
                      "(inr_goal_from || '-' || inr_goal_to) AS goal FROM patient WHERE status = :status "
                      "GROUP BY goal")
        query.bindValue(":status", "A")
        query.exec()
        return query

    def query_goal_inactive_patients(self):
        """Create and return a query for goals of inactive patients only"""
        query = QSqlQuery()
        query.prepare("SELECT COUNT(inr_goal_from || '-' || inr_goal_to) AS total, "
                      "(inr_goal_from || '-' || inr_goal_to) AS goal FROM patient WHERE status = :status "
                      "GROUP BY goal")
        query.bindValue(":status", "I")
        query.exec()
        return query