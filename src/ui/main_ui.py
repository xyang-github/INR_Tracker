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
        dlgMain.setFixedSize(701, 300)
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
        dlgMain.setStyleSheet(
            """
            QWidget {
                background-color: #f5f5f5;}
                
            QLabel {
                font-family: \"Source Sans Pro\";
                font-size: 16px;
                font-weight: bold;}

            QPushButton {
                background-color: #00b4d8;
                color: white;
                border-radius: 8px;
                font-family: \"Raleway\";
                font-size: 12px;
                border: none;}
                
            QPushButton::hover {
                background-color: #b3e9f3;}
                
            QLineEdit {
                background-color: white;
                border: none;
                border-bottom: 2px solid #00b4d8;
                padding: 10px;
                font-family:  \"Raleway\";
                font: 12px;
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;}
            
            QLabel#lblTitle {
                color: #5E60CE;
                margin-bottom: 5px;
                font-family: "Righteous";
                font-size: 48px;
                font-weight: bold;}
            
            QMenuBar {
                background-color: #f5f5f5;
                color: #555555;}
            
            QMenuBar::item {
                height: 30px;
                padding: 8px;
                background-color: transparent;
                color: #555555;}
            
            QMenuBar::item:selected,
            QMenuBar::item:pressed {
                color: #3c3c3c;
                background-color: #b3e9f3;}
                
            QMenu::item {
                height: 26px;
                color: #555555;}
            
            QMenu::item:selected {
                color: #3c3c3c;
                background-color: #b3e9f3;}
            """
        )
        self.centralwidget = QtWidgets.QWidget(dlgMain)
        palette = QtGui.QPalette()
        self.centralwidget.setPalette(palette)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(140, 30, 541, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytButtons = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.lytButtons.setContentsMargins(0, 0, 0, 0)
        self.lytButtons.setObjectName("lytButtons")
        self.btnNewPatient = QtWidgets.QPushButton(self.layoutWidget)
        self.btnNewPatient.setProperty('class', 'big_button')


        self.btnNewPatient.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        self.btnNewPatient.setFont(font)
        self.btnNewPatient.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNewPatient.setIcon(icon)
        self.btnNewPatient.setIconSize(QtCore.QSize(25, 25))
        self.btnNewPatient.setObjectName("btnNewPatient")
        self.lytButtons.addWidget(self.btnNewPatient)
        self.btnIndications = QtWidgets.QPushButton(self.layoutWidget)
        self.btnIndications.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        self.btnIndications.setFont(font)
        self.btnIndications.setStyleSheet("")
        self.btnIndications.setIcon(icon)
        self.btnIndications.setIconSize(QtCore.QSize(20, 20))
        self.btnIndications.setObjectName("btnIndications")
        self.lytButtons.addWidget(self.btnIndications)
        self.btnEvents = QtWidgets.QPushButton(self.layoutWidget)
        self.btnEvents.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        self.btnEvents.setFont(font)
        self.btnEvents.setStyleSheet("")
        self.btnEvents.setIcon(icon)
        self.btnEvents.setIconSize(QtCore.QSize(20, 20))
        self.btnEvents.setObjectName("btnEvents")
        self.lytButtons.addWidget(self.btnEvents)
        self.btnReports = QtWidgets.QPushButton(self.layoutWidget)
        self.btnReports.setMinimumSize(QtCore.QSize(0, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/icon/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReports.setIcon(icon1)
        self.btnReports.setIconSize(QtCore.QSize(20, 20))
        self.btnReports.setObjectName("btnReports")
        self.lytButtons.addWidget(self.btnReports)
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
        self.ledMRN.setFont(font)
        self.ledMRN.setText("")
        self.ledMRN.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ledMRN.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ledMRN.setObjectName("ledMRN")
        self.lytMiddle.addWidget(self.ledMRN)
        self.btnSearchPatient = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearchPatient.sizePolicy().hasHeightForWidth())
        self.btnSearchPatient.setSizePolicy(sizePolicy)
        self.btnSearchPatient.setMinimumSize(QtCore.QSize(50, 40))
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
        self.btnSearchPatient.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Readex Pro")
        font.setPointSize(-1)
        self.btnSearchPatient.setFont(font)
        self.btnSearchPatient.setStyleSheet("")
        self.btnSearchPatient.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/icon/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearchPatient.setIcon(icon2)
        self.btnSearchPatient.setIconSize(QtCore.QSize(24, 24))
        self.btnSearchPatient.setFlat(False)
        self.btnSearchPatient.setObjectName("btnSearchPatient")
        self.lytMiddle.addWidget(self.btnSearchPatient)
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
        self.menuAction = QtWidgets.QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")
        dlgMain.setMenuBar(self.menuBar)
        self.menuExit = QtWidgets.QAction(dlgMain)
        self.menuExit.setObjectName("menuExit")
        self.menuHelpDialog = QtWidgets.QAction(dlgMain)
        self.menuHelpDialog.setObjectName("menuHelpDialog")
        self.menuNewPatient = QtWidgets.QAction(dlgMain)
        self.menuNewPatient.setObjectName("menuNewPatient")
        self.menuNewPatient = QtWidgets.QAction(dlgMain)
        self.menuNewPatient.setObjectName("menuNewPatient")
        self.menuIndications = QtWidgets.QAction(dlgMain)
        self.menuIndications.setObjectName("menuIndications")
        self.menuEvents = QtWidgets.QAction(dlgMain)
        self.menuEvents.setObjectName("menuEvents")
        self.menuReports = QtWidgets.QAction(dlgMain)
        self.menuReports.setObjectName("menuReports")
        self.menuFile.addAction(self.menuExit)
        self.menuHelp.addAction(self.menuHelpDialog)
        self.menuAction.addAction(self.menuNewPatient)
        self.menuAction.addAction(self.menuIndications)
        self.menuAction.addAction(self.menuEvents)
        self.menuAction.addAction(self.menuReports)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(dlgMain)
        QtCore.QMetaObject.connectSlotsByName(dlgMain)

    def retranslateUi(self, dlgMain):
        _translate = QtCore.QCoreApplication.translate
        dlgMain.setWindowTitle(_translate("dlgMain", "INR Tracker"))
        self.btnNewPatient.setToolTip(_translate("dlgMain", "Create a new patient profile"))
        self.btnNewPatient.setStatusTip(_translate("dlgMain", "New patient profile"))
        self.btnNewPatient.setText(_translate("dlgMain", "New Patient"))
        self.btnNewPatient.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.btnIndications.setToolTip(_translate("dlgMain", "Add, edit or delete indications"))
        self.btnIndications.setStatusTip(_translate("dlgMain", "Update indication list"))
        self.btnIndications.setText(_translate("dlgMain", "Indications"))
        self.btnIndications.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.btnEvents.setToolTip(_translate("dlgMain", "Add, edit or delete events"))
        self.btnEvents.setStatusTip(_translate("dlgMain", "Update event list"))
        self.btnEvents.setText(_translate("dlgMain", "Events"))
        self.btnEvents.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.btnReports.setToolTip(_translate("dlgMain", "View clinic reports"))
        self.btnReports.setStatusTip(_translate("dlgMain", "View clinic reports"))
        self.btnReports.setText(_translate("dlgMain", "Reports"))
        self.lblTitle.setText(_translate("dlgMain", "inr tracker >>"))
        self.ledMRN.setToolTip(_translate("dlgMain", "Enter patient\'s medical record number"))
        self.ledMRN.setStatusTip(_translate("dlgMain", "Enter medical record number"))
        self.ledMRN.setPlaceholderText(_translate("dlgMain", "Enter patient\'s MRN"))
        self.btnSearchPatient.setToolTip(_translate("dlgMain", "Click to search patient profile"))
        self.btnSearchPatient.setStatusTip(_translate("dlgMain", "Search patient profile"))
        self.btnSearchPatient.setShortcut(_translate("dlgMain", "Return"))
        self.menuFile.setTitle(_translate("dlgMain", "File"))
        self.menuHelp.setTitle(_translate("dlgMain", "Help"))
        self.menuAction.setTitle(_translate("dlgMain", "Action"))
        self.menuExit.setText(_translate("dlgMain", "Exit"))
        self.menuExit.setShortcut(_translate("dlgMain", "Ctrl+E"))
        self.menuHelpDialog.setText(_translate("dlgMain", "INR Tracker Help"))
        self.menuHelpDialog.setShortcut(_translate("dlgMain", "Ctrl+H"))
        self.menuNewPatient.setText(_translate("dlgMain", "Add New Patient"))
        self.menuNewPatient.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.menuNewPatient.setText(_translate("dlgMain", "New Patient"))
        self.menuNewPatient.setShortcut(_translate("dlgMain", "Ctrl+N"))
        self.menuIndications.setText(_translate("dlgMain", "Indications"))
        self.menuIndications.setShortcut(_translate("dlgMain", "Ctrl+I"))
        self.menuEvents.setText(_translate("dlgMain", "Events"))
        self.menuEvents.setShortcut(_translate("dlgMain", "Ctrl+M"))
        self.menuReports.setText(_translate("dlgMain", "Reports"))
        self.menuReports.setShortcut(_translate("dlgMain", "Ctrl+R"))
import resource.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgMain = QtWidgets.QMainWindow()
    ui = Ui_dlgMain()
    ui.setupUi(dlgMain)
    dlgMain.show()
    sys.exit(app.exec_())
