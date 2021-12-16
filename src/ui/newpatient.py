# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpatient.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgNewPatient(object):
    def setupUi(self, DlgNewPatient):
        DlgNewPatient.setObjectName("DlgNewPatient")
        DlgNewPatient.resize(614, 754)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        DlgNewPatient.setPalette(palette)
        DlgNewPatient.setStyleSheet("QPushButton {\n"
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
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-family:  \"Readex Pro\";\n"
"    font: 12px;\n"
"\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #5E60CE;\n"
"    font-family: \"Raleway\";\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    margin-top: 10px;\n"
"}\n"
"\n"
"QLabel#lblHeader {\n"
"    font-family: \"Raleway\";\n"
"    font-size: 36px;    \n"
"    font-weight: bold;\n"
"    margin: 0;\n"
"}\n"
"")
        self.widget = QtWidgets.QWidget(DlgNewPatient)
        self.widget.setGeometry(QtCore.QRect(11, 11, 591, 726))
        self.widget.setObjectName("widget")
        self.lytMain = QtWidgets.QVBoxLayout(self.widget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblHeader.setFont(font)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytFormTop = QtWidgets.QFormLayout()
        self.lytFormTop.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytFormTop.setObjectName("lytFormTop")
        self.lblMRN = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblMRN.setFont(font)
        self.lblMRN.setObjectName("lblMRN")
        self.lytFormTop.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblMRN)
        self.ledMRN = QtWidgets.QLineEdit(self.widget)
        self.ledMRN.setMinimumSize(QtCore.QSize(0, 20))
        self.ledMRN.setObjectName("ledMRN")
        self.lytFormTop.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ledMRN)
        self.lblFirstName = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblFirstName.setFont(font)
        self.lblFirstName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblFirstName.setObjectName("lblFirstName")
        self.lytFormTop.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblFirstName)
        self.ledFirstName = QtWidgets.QLineEdit(self.widget)
        self.ledFirstName.setMinimumSize(QtCore.QSize(0, 20))
        self.ledFirstName.setObjectName("ledFirstName")
        self.lytFormTop.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ledFirstName)
        self.lblLastName = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblLastName.setFont(font)
        self.lblLastName.setObjectName("lblLastName")
        self.lytFormTop.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lblLastName)
        self.ledLastName = QtWidgets.QLineEdit(self.widget)
        self.ledLastName.setMinimumSize(QtCore.QSize(0, 20))
        self.ledLastName.setObjectName("ledLastName")
        self.lytFormTop.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ledLastName)
        self.lblDOB = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblDOB.setFont(font)
        self.lblDOB.setObjectName("lblDOB")
        self.lytFormTop.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lblDOB)
        self.ledDOB = QtWidgets.QLineEdit(self.widget)
        self.ledDOB.setMinimumSize(QtCore.QSize(0, 20))
        self.ledDOB.setObjectName("ledDOB")
        self.lytFormTop.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.ledDOB)
        self.lblStatus = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblStatus.setFont(font)
        self.lblStatus.setObjectName("lblStatus")
        self.lytFormTop.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lblStatus)
        self.rbtnStatusActive = QtWidgets.QRadioButton(self.widget)
        self.rbtnStatusActive.setChecked(True)
        self.rbtnStatusActive.setObjectName("rbtnStatusActive")
        self.lytFormTop.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.rbtnStatusActive)
        self.rbtnStatusInactive = QtWidgets.QRadioButton(self.widget)
        self.rbtnStatusInactive.setObjectName("rbtnStatusInactive")
        self.lytFormTop.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.rbtnStatusInactive)
        self.lytMain.addLayout(self.lytFormTop)
        self.line_indication_top = QtWidgets.QFrame(self.widget)
        self.line_indication_top.setLineWidth(3)
        self.line_indication_top.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_indication_top.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_indication_top.setObjectName("line_indication_top")
        self.lytMain.addWidget(self.line_indication_top)
        self.lblIndications = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblIndications.setFont(font)
        self.lblIndications.setObjectName("lblIndications")
        self.lytMain.addWidget(self.lblIndications)
        self.lytIndicationMain = QtWidgets.QHBoxLayout()
        self.lytIndicationMain.setObjectName("lytIndicationMain")
        self.lytIndicationLeft = QtWidgets.QVBoxLayout()
        self.lytIndicationLeft.setObjectName("lytIndicationLeft")
        self.lytIndicationAdd = QtWidgets.QHBoxLayout()
        self.lytIndicationAdd.setObjectName("lytIndicationAdd")
        self.ledNewIndication = QtWidgets.QLineEdit(self.widget)
        self.ledNewIndication.setMinimumSize(QtCore.QSize(0, 40))
        self.ledNewIndication.setObjectName("ledNewIndication")
        self.lytIndicationAdd.addWidget(self.ledNewIndication)
        self.btnNewIndication = QtWidgets.QPushButton(self.widget)
        self.btnNewIndication.setMinimumSize(QtCore.QSize(60, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNewIndication.setIcon(icon)
        self.btnNewIndication.setObjectName("btnNewIndication")
        self.lytIndicationAdd.addWidget(self.btnNewIndication)
        self.lytIndicationLeft.addLayout(self.lytIndicationAdd)
        self.lstExistingIndications = QtWidgets.QListWidget(self.widget)
        self.lstExistingIndications.setObjectName("lstExistingIndications")
        self.lytIndicationLeft.addWidget(self.lstExistingIndications)
        self.lytIndicationMain.addLayout(self.lytIndicationLeft)
        self.lytButton = QtWidgets.QVBoxLayout()
        self.lytButton.setObjectName("lytButton")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytButton.addItem(spacerItem)
        self.btnAddIndication = QtWidgets.QPushButton(self.widget)
        self.btnAddIndication.setMinimumSize(QtCore.QSize(40, 0))
        self.btnAddIndication.setObjectName("btnAddIndication")
        self.lytButton.addWidget(self.btnAddIndication)
        self.btnRemoveIndication = QtWidgets.QPushButton(self.widget)
        self.btnRemoveIndication.setObjectName("btnRemoveIndication")
        self.lytButton.addWidget(self.btnRemoveIndication)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytButton.addItem(spacerItem1)
        self.lytIndicationMain.addLayout(self.lytButton)
        self.lstPatientIndications = QtWidgets.QListWidget(self.widget)
        self.lstPatientIndications.setObjectName("lstPatientIndications")
        self.lytIndicationMain.addWidget(self.lstPatientIndications)
        self.lytMain.addLayout(self.lytIndicationMain)
        self.line_indication_bottom = QtWidgets.QFrame(self.widget)
        self.line_indication_bottom.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_indication_bottom.setLineWidth(3)
        self.line_indication_bottom.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_indication_bottom.setObjectName("line_indication_bottom")
        self.lytMain.addWidget(self.line_indication_bottom)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblGoalFrom = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblGoalFrom.setFont(font)
        self.lblGoalFrom.setObjectName("lblGoalFrom")
        self.horizontalLayout.addWidget(self.lblGoalFrom)
        self.ledGoalFrom = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ledGoalFrom.sizePolicy().hasHeightForWidth())
        self.ledGoalFrom.setSizePolicy(sizePolicy)
        self.ledGoalFrom.setMinimumSize(QtCore.QSize(0, 20))
        self.ledGoalFrom.setObjectName("ledGoalFrom")
        self.horizontalLayout.addWidget(self.ledGoalFrom)
        self.lblGoalTo = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblGoalTo.setFont(font)
        self.lblGoalTo.setObjectName("lblGoalTo")
        self.horizontalLayout.addWidget(self.lblGoalTo)
        self.ledGoalTo = QtWidgets.QLineEdit(self.widget)
        self.ledGoalTo.setMinimumSize(QtCore.QSize(0, 20))
        self.ledGoalTo.setObjectName("ledGoalTo")
        self.horizontalLayout.addWidget(self.ledGoalTo)
        self.lytMain.addLayout(self.horizontalLayout)
        self.lytBottomButtons = QtWidgets.QHBoxLayout()
        self.lytBottomButtons.setObjectName("lytBottomButtons")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytBottomButtons.addItem(spacerItem2)
        self.btnOk = QtWidgets.QPushButton(self.widget)
        self.btnOk.setMinimumSize(QtCore.QSize(60, 30))
        self.btnOk.setObjectName("btnOk")
        self.lytBottomButtons.addWidget(self.btnOk)
        self.btnExit = QtWidgets.QPushButton(self.widget)
        self.btnExit.setMinimumSize(QtCore.QSize(60, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytBottomButtons.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytBottomButtons)

        self.retranslateUi(DlgNewPatient)
        QtCore.QMetaObject.connectSlotsByName(DlgNewPatient)

    def retranslateUi(self, DlgNewPatient):
        _translate = QtCore.QCoreApplication.translate
        DlgNewPatient.setWindowTitle(_translate("DlgNewPatient", "Dialog"))
        self.lblHeader.setText(_translate("DlgNewPatient", "New Patient"))
        self.lblMRN.setText(_translate("DlgNewPatient", "Medical Record Number"))
        self.ledMRN.setPlaceholderText(_translate("DlgNewPatient", "Enter medical record number"))
        self.lblFirstName.setText(_translate("DlgNewPatient", "First Name"))
        self.ledFirstName.setPlaceholderText(_translate("DlgNewPatient", "Enter first name"))
        self.lblLastName.setText(_translate("DlgNewPatient", "Last Name"))
        self.ledLastName.setPlaceholderText(_translate("DlgNewPatient", "Enter last name"))
        self.lblDOB.setText(_translate("DlgNewPatient", "Date of Birth"))
        self.ledDOB.setPlaceholderText(_translate("DlgNewPatient", "Enter date of birth in the following format: YYYY-MM-DD"))
        self.lblStatus.setText(_translate("DlgNewPatient", "Status"))
        self.rbtnStatusActive.setText(_translate("DlgNewPatient", "Active"))
        self.rbtnStatusInactive.setText(_translate("DlgNewPatient", "Inactive"))
        self.lblIndications.setText(_translate("DlgNewPatient", "Indication(s)"))
        self.ledNewIndication.setPlaceholderText(_translate("DlgNewPatient", "Type new indication here"))
        self.btnNewIndication.setToolTip(_translate("DlgNewPatient", "Add new indication to list of indications in the database"))
        self.btnNewIndication.setText(_translate("DlgNewPatient", "Add"))
        self.btnAddIndication.setToolTip(_translate("DlgNewPatient", "Add indication to patient\'s profile"))
        self.btnAddIndication.setText(_translate("DlgNewPatient", "-->"))
        self.btnRemoveIndication.setToolTip(_translate("DlgNewPatient", "Remove indication from patient\'s profile"))
        self.btnRemoveIndication.setText(_translate("DlgNewPatient", "<--"))
        self.lblGoalFrom.setText(_translate("DlgNewPatient", "INR Goal from:"))
        self.ledGoalFrom.setPlaceholderText(_translate("DlgNewPatient", "Enter lower end of INR goal"))
        self.lblGoalTo.setText(_translate("DlgNewPatient", "to:"))
        self.ledGoalTo.setPlaceholderText(_translate("DlgNewPatient", "Enter higher end of INR goal"))
        self.btnOk.setText(_translate("DlgNewPatient", "OK"))
        self.btnExit.setText(_translate("DlgNewPatient", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgNewPatient = QtWidgets.QDialog()
    ui = Ui_DlgNewPatient()
    ui.setupUi(DlgNewPatient)
    DlgNewPatient.show()
    sys.exit(app.exec_())