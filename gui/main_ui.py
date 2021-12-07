# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgMain(object):
    def setupUi(self, dlgMain):
        dlgMain.setObjectName("dlgMain")
        dlgMain.resize(701, 280)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgMain.sizePolicy().hasHeightForWidth())
        dlgMain.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(3, 4, 94))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 244, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(3, 4, 94))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 244, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 244, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 244, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        dlgMain.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("bodyText")
        dlgMain.setFont(font)
        dlgMain.setStyleSheet("QPushButton {\n"
"    background-color: #00b4d8;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    font-family: \"Readex Pro\";\n"
"    font: 12px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    border: 3px solid #0077b6;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 2px  solid gray;\n"
"    border-radius: 20px;\n"
"    padding: 10px;\n"
"    font-family:  \"Readex Pro\";\n"
"    font: 12px;\n"
"\n"
"}\n"
"\n"
"QLabel#lblTitle {\n"
"    color: #5E60CE;\n"
"    margin-bottom: 5px;\n"
"    font-family: \"Righteous\";\n"
"    font-size: 48px;\n"
"    font-weight: bold;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(dlgMain)
        palette = QtGui.QPalette()
        self.centralwidget.setPalette(palette)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(320, 30, 361, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytButtons = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.lytButtons.setContentsMargins(0, 0, 0, 0)
        self.lytButtons.setObjectName("lytButtons")
        self.btnReports = QtWidgets.QPushButton(self.layoutWidget)
        self.btnReports.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReports.setIcon(icon)
        self.btnReports.setIconSize(QtCore.QSize(20, 20))
        self.btnReports.setObjectName("btnReports")
        self.lytButtons.addWidget(self.btnReports)
        self.btnIndications = QtWidgets.QPushButton(self.layoutWidget)
        self.btnIndications.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnIndications.setFont(font)
        self.btnIndications.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnIndications.setIcon(icon1)
        self.btnIndications.setIconSize(QtCore.QSize(20, 20))
        self.btnIndications.setObjectName("btnIndications")
        self.lytButtons.addWidget(self.btnIndications)
        self.btnNewPatient = QtWidgets.QPushButton(self.layoutWidget)
        self.btnNewPatient.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnNewPatient.setFont(font)
        self.btnNewPatient.setStyleSheet("")
        self.btnNewPatient.setIcon(icon1)
        self.btnNewPatient.setIconSize(QtCore.QSize(25, 25))
        self.btnNewPatient.setObjectName("btnNewPatient")
        self.lytButtons.addWidget(self.btnNewPatient)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 110, 631, 99))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.lytMiddle = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.lytMiddle.setContentsMargins(0, 0, 0, 0)
        self.lytMiddle.setObjectName("lytMiddle")
        self.lblTitle = QtWidgets.QLabel(self.layoutWidget1)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 96, 206))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.lblTitle.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Righteous")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setStyleSheet("")
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setObjectName("lblTitle")
        self.lytMiddle.addWidget(self.lblTitle)
        self.ledMRN = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ledMRN.setFont(font)
        self.ledMRN.setText("")
        self.ledMRN.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledMRN.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ledMRN.setObjectName("ledMRN")
        self.lytMiddle.addWidget(self.ledMRN)
        self.btnSearch = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearch.sizePolicy().hasHeightForWidth())
        self.btnSearch.setSizePolicy(sizePolicy)
        self.btnSearch.setMinimumSize(QtCore.QSize(50, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 180, 216))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.btnSearch.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnSearch.setFont(font)
        self.btnSearch.setStyleSheet("")
        self.btnSearch.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearch.setIcon(icon2)
        self.btnSearch.setIconSize(QtCore.QSize(24, 24))
        self.btnSearch.setFlat(False)
        self.btnSearch.setObjectName("btnSearch")
        self.lytMiddle.addWidget(self.btnSearch)
        self.lblColor = QtWidgets.QLabel(self.centralwidget)
        self.lblColor.setGeometry(QtCore.QRect(10, 90, 671, 141))
        self.lblColor.setStyleSheet("QLabel#lblColor {\n"
"    border: 4px solid #5E60CE;\n"
"    border-radius: 10px;\n"
"}")
        self.lblColor.setText("")
        self.lblColor.setObjectName("lblColor")
        self.lblColor.lower()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        dlgMain.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(dlgMain)
        self.statusbar.setObjectName("statusbar")
        dlgMain.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(dlgMain)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 701, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        dlgMain.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(dlgMain)
        self.actionExit.setObjectName("actionExit")
        self.actionINR_Tracker_Help = QtWidgets.QAction(dlgMain)
        self.actionINR_Tracker_Help.setObjectName("actionINR_Tracker_Help")
        self.actionAdd_New_Patient = QtWidgets.QAction(dlgMain)
        self.actionAdd_New_Patient.setObjectName("actionAdd_New_Patient")
        self.menuFile.addAction(self.actionAdd_New_Patient)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionINR_Tracker_Help)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(dlgMain)
        QtCore.QMetaObject.connectSlotsByName(dlgMain)

    def retranslateUi(self, dlgMain):
        _translate = QtCore.QCoreApplication.translate
        dlgMain.setWindowTitle(_translate("dlgMain", "INR Tracker"))
        self.btnReports.setText(_translate("dlgMain", "Reports"))
        self.btnIndications.setToolTip(_translate("dlgMain", "Add, edit or delete indications"))
        self.btnIndications.setStatusTip(_translate("dlgMain", "Update indication list"))
        self.btnIndications.setText(_translate("dlgMain", "Indications"))
        self.btnIndications.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.btnNewPatient.setToolTip(_translate("dlgMain", "Create a new patient profile"))
        self.btnNewPatient.setStatusTip(_translate("dlgMain", "New patient profile"))
        self.btnNewPatient.setText(_translate("dlgMain", "New Patient"))
        self.btnNewPatient.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.lblTitle.setText(_translate("dlgMain", "inr tracker >>"))
        self.ledMRN.setToolTip(_translate("dlgMain", "Enter patient\'s medical record number"))
        self.ledMRN.setStatusTip(_translate("dlgMain", "Enter medical record number"))
        self.ledMRN.setPlaceholderText(_translate("dlgMain", "Enter patient\'s MRN"))
        self.btnSearch.setToolTip(_translate("dlgMain", "Click to search patient profile"))
        self.btnSearch.setStatusTip(_translate("dlgMain", "Search patient profile"))
        self.btnSearch.setShortcut(_translate("dlgMain", "Return"))
        self.menuFile.setTitle(_translate("dlgMain", "File"))
        self.menuHelp.setTitle(_translate("dlgMain", "Help"))
        self.actionExit.setText(_translate("dlgMain", "Exit"))
        self.actionExit.setShortcut(_translate("dlgMain", "Ctrl+E"))
        self.actionINR_Tracker_Help.setText(_translate("dlgMain", "INR Tracker Help"))
        self.actionINR_Tracker_Help.setShortcut(_translate("dlgMain", "Ctrl+H"))
        self.actionAdd_New_Patient.setText(_translate("dlgMain", "Add New Patient"))
        self.actionAdd_New_Patient.setShortcut(_translate("dlgMain", "Ctrl+N"))
import resource.resource


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgMain = QtWidgets.QMainWindow()
    ui = Ui_dlgMain()
    ui.setupUi(dlgMain)
    dlgMain.show()
    sys.exit(app.exec_())
