# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patientlist.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgPatients(object):
    def setupUi(self, DlgPatients):
        DlgPatients.setObjectName("DlgPatients")
        DlgPatients.resize(404, 584)
        DlgPatients.setStyleSheet("QDialog {\n"
"    background-color: #e2f2ff;\n"
"}\n"
"\n"
"QPushButton {\n"
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
"    border: none;\n"
"    background-color: #e2f2ff;\n"
"}\n"
"\n"
"QLineEdit {color: #03045e; font-emphasis: bold; font-family: 'Raleway'; font-size: 16px;}"                                     
"QLabel {\n"
"    color: #5E60CE;\n"
"    font-family: \"Raleway\";\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QLabel#lblHeader {\n"
"    font-family: \"Raleway\";\n"
"    font-size: 36px;    \n"
"    font-weight: bold;\n"
"    margin: 0;\n"
"}")
        self.widget = QtWidgets.QWidget(DlgPatients)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 561))
        self.widget.setObjectName("widget")
        self.lytMain = QtWidgets.QVBoxLayout(self.widget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.widget)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytRadioButton = QtWidgets.QHBoxLayout()
        self.lytRadioButton.setObjectName("lytRadioButton")
        self.rbtAll = QtWidgets.QRadioButton(self.widget)
        self.rbtAll.setStyleSheet("")
        self.rbtAll.setChecked(True)
        self.rbtAll.setObjectName("rbtAll")
        self.buttonGroup = QtWidgets.QButtonGroup(DlgPatients)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.rbtAll)
        self.lytRadioButton.addWidget(self.rbtAll)
        self.rbtActive = QtWidgets.QRadioButton(self.widget)
        self.rbtActive.setStyleSheet("")
        self.rbtActive.setObjectName("rbtActive")
        self.buttonGroup.addButton(self.rbtActive)
        self.lytRadioButton.addWidget(self.rbtActive)
        self.rbtInactive = QtWidgets.QRadioButton(self.widget)
        self.rbtInactive.setStyleSheet("")
        self.rbtInactive.setObjectName("rbtInactive")
        self.buttonGroup.addButton(self.rbtInactive)
        self.lytRadioButton.addWidget(self.rbtInactive)
        self.lytMain.addLayout(self.lytRadioButton)
        self.lytTotal = QtWidgets.QHBoxLayout()
        self.lytTotal.setObjectName("lytTotal")
        self.lblTotal = QtWidgets.QLabel(self.widget)
        self.lblTotal.setObjectName("lblTotal")
        self.lytTotal.addWidget(self.lblTotal)
        self.ledTotal = QtWidgets.QLineEdit(self.widget)
        self.ledTotal.setReadOnly(True)
        self.ledTotal.setObjectName("ledTotal")
        self.lytTotal.addWidget(self.ledTotal)
        self.lytMain.addLayout(self.lytTotal)
        self.tblPatientList = QtWidgets.QTableWidget(self.widget)
        self.tblPatientList.setObjectName("tableWidget")
        self.tblPatientList.setColumnCount(3)
        self.tblPatientList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 170, 255))
        self.tblPatientList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblPatientList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblPatientList.setHorizontalHeaderItem(2, item)
        self.lytMain.addWidget(self.tblPatientList)
        self.lytExit = QtWidgets.QHBoxLayout()
        self.lytExit.setObjectName("lytExit")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytExit.addItem(spacerItem)
        self.btnExit = QtWidgets.QPushButton(self.widget)
        self.btnExit.setMinimumSize(QtCore.QSize(60, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytExit.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytExit)

        self.retranslateUi(DlgPatients)
        QtCore.QMetaObject.connectSlotsByName(DlgPatients)

    def retranslateUi(self, DlgPatients):
        _translate = QtCore.QCoreApplication.translate
        DlgPatients.setWindowTitle(_translate("DlgPatients", "Patient List"))
        self.lblHeader.setText(_translate("DlgPatients", "Patient List"))
        self.rbtAll.setText(_translate("DlgPatients", "All"))
        self.rbtActive.setText(_translate("DlgPatients", "Active"))
        self.rbtInactive.setText(_translate("DlgPatients", "Inactive"))
        self.lblTotal.setText(_translate("DlgPatients", "Total:"))
        item = self.tblPatientList.horizontalHeaderItem(0)
        item.setText(_translate("DlgPatients", "MRN"))
        item = self.tblPatientList.horizontalHeaderItem(1)
        item.setText(_translate("DlgPatients", "Last Name"))
        item = self.tblPatientList.horizontalHeaderItem(2)
        item.setText(_translate("DlgPatients", "First Name"))
        self.btnExit.setText(_translate("DlgPatients", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgPatients = QtWidgets.QDialog()
    ui = Ui_DlgPatients()
    ui.setupUi(DlgPatients)
    DlgPatients.show()
    sys.exit(app.exec_())
