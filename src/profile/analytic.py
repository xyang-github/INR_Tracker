from PyQt5 import QtGui
from PyQt5.QtChart import QPieSeries, QPieSlice, QChart, QChartView
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit


class DlgAnalytics(QDialog):
    """Dialog window to display analytics"""
    def __init__(self, percent_ttr, total_days_in_ttr, total_days, total_tests, number_of_results_in_range,
                 number_of_events):
        super(DlgAnalytics, self).__init__()
        width = 700
        height = 800
        self.setFixedSize(width, height)
        self.setWindowTitle("Analytics")
        self.lytMain = QVBoxLayout()
        self.setStyleSheet(
            """
        QTextEdit{
            border: 2px solid #00b4d8; 
            border-radius:10px; 
            background-color: palette(base);
            padding: 15px;} 
            
            """
        )

        # Create pie chart
        self.pie_ttr = QPieSeries()
        self.pie_ttr.append("% Days In Range", round(percent_ttr*100))
        self.pie_ttr.append("% Days Out Of Range ", 100-round(percent_ttr*100))
        self.pie_slice_ttr = QPieSlice()
        self.pie_slice_ttr = self.pie_ttr.slices()[0]
        self.pie_slice_not_ttr = self.pie_ttr.slices()[1]

        chart = QChart()
        chart.addSeries(self.pie_ttr)
        chart.setTitle("<h1>Time Within Therapeutic Range</h1>")
        chart.setTheme(QChart.ChartThemeBlueNcs)
        chart.legend().hide()

        # Format pie chart
        self.pie_ttr.setLabelsVisible()
        self.pie_slice_ttr.setLabel(str(int(self.pie_slice_ttr.percentage() * 100)) +
                                    f"% TTR: {round(total_days_in_ttr)} days")
        self.pie_slice_ttr.setLabelColor(QColor("green"))
        self.pie_slice_not_ttr.setLabel(str(int(self.pie_slice_not_ttr.percentage() * 100)) +
                                        f"% Out of range: {round(total_days - total_days_in_ttr)} days")
        self.pie_slice_not_ttr.setLabelColor(QColor("red"))

        # Format each slice
        for slice in self.pie_ttr.slices():
            font = QtGui.QFont()
            font.setBold(True)
            font.setPixelSize(12)
            slice.setLabelFont(font)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create text edit widget for summary data
        description = f"""
        <h2>Summary</h2>
        <table cellspacing=10>
            <tr>
                <td>Total Days On Record:</td>
                <td>{round(total_days)}</td>
            </tr>
            <tr>
                <td>Days Within Range:</td>
                <td>{round(total_days_in_ttr)}</td>
            </tr>
            <tr>
                <td><strong>Percent of Days Within Range: </strong></td>
                <td>{round((total_days_in_ttr / total_days) * 100)}%</td>
            </tr>
            <tr>
                <td>Total Number of Tests:</td>
                <td>{total_tests}</td>
            </tr>
            <tr>
                <td>Number of Tests in Range:</td>
                <td>{number_of_results_in_range}</td>
            </tr>
            <tr>
                <td><strong>Percent of Test in Range: </strong></td>
                <td> {round((number_of_results_in_range / total_tests) * 100)}%</td>
            </tr>
        </table>

        <br>
        <h2>Clinical Events:</h2>
        <table cellspacing=10>>
            <tr>
                <td>Past 6 months:</td>
                <td>{number_of_events[0]}</td>
            </tr>
            <tr>
                <td>Past 12 months:</td>
                <td>{number_of_events[1]}</td>
            </tr>
            <tr>
                <td>All time:</td>
                <td>{number_of_events[2]}</td>
            </tr>
        </table>
 
        <br>
        <div style = "font-size: 14px">
        <em>TTR was calculated using the Rosendaal linear interpolation method, which assumes a linear change between 
        INR measurements over time. Clinical judgement should be used when evaluating the significance of TTR in 
        clinical decision making.</em>
        </div>
        """

        text_edit = QTextEdit(description)
        text_edit.setReadOnly(True)

        self.lytMain.addWidget(chart_view)
        self.lytMain.addWidget(text_edit)
        self.setLayout(self.lytMain)