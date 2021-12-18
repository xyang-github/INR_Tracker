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
"    font-family: \"Raleway\";\n"
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
"QLabel {\n"
"    color: #5E60CE;\n"
"    font-family: \"Source Sans Pro\";\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#lblHeader {\n"
"    font-family: \"Source Sans Pro\";\n"
"    font-size: 24px;    \n"
"    font-weight: bold;\n"
"    color: #00b4d8;\n"
"    border: 2px solid #00b4d8;\n"
"    border-radius: 10px;\n"
"}")
        self.layoutWidget = QtWidgets.QWidget(DlgPatients)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 561))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.layoutWidget)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytRadioButton = QtWidgets.QHBoxLayout()
        self.lytRadioButton.setObjectName("lytRadioButton")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytRadioButton.addItem(spacerItem)
        self.rbtAll = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtAll.setStyleSheet("")
        self.rbtAll.setChecked(True)
        self.rbtAll.setObjectName("rbtAll")
        self.buttonGroup = QtWidgets.QButtonGroup(DlgPatients)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.rbtAll)
        self.lytRadioButton.addWidget(self.rbtAll)
        self.rbtActive = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtActive.setStyleSheet("")
        self.rbtActive.setObjectName("rbtActive")
        self.buttonGroup.addButton(self.rbtActive)
        self.lytRadioButton.addWidget(self.rbtActive)
        self.rbtInactive = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtInactive.setStyleSheet("")
        self.rbtInactive.setObjectName("rbtInactive")
        self.buttonGroup.addButton(self.rbtInactive)
        self.lytRadioButton.addWidget(self.rbtInactive)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytRadioButton.addItem(spacerItem1)
        self.lytMain.addLayout(self.lytRadioButton)
        self.lytTotal = QtWidgets.QHBoxLayout()
        self.lytTotal.setObjectName("lytTotal")
        self.lblTotal = QtWidgets.QLabel(self.layoutWidget)
        self.lblTotal.setObjectName("lblTotal")
        self.lytTotal.addWidget(self.lblTotal)
        self.ledTotal = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledTotal.setReadOnly(True)
        self.ledTotal.setObjectName("ledTotal")
        self.lytTotal.addWidget(self.ledTotal)
        self.lytMain.addLayout(self.lytTotal)
        self.tblPatientList = QtWidgets.QTableWidget(self.layoutWidget)
        self.tblPatientList.setObjectName("tblPatientList")
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
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytExit.addItem(spacerItem2)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
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
        item.setText(_translate("DlgPatients", "New Column"))
        item = self.tblPatientList.horizontalHeaderItem(2)
        item.setText(_translate("DlgPatients", "First Name"))
        self.btnExit.setText(_translate("DlgPatients", "Exit"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgPatients = QtWidgets.QDialog()
    ui = Ui_DlgPatients()
    ui.setupUi(DlgPatients)
    DlgPatients.show()
    sys.exit(app.exec_())
