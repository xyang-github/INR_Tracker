# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patientprofile.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgProfile(object):
    def setupUi(self, DlgProfile):
        DlgProfile.setObjectName("DlgProfile")
        DlgProfile.resize(703, 529)
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
        DlgProfile.setPalette(palette)
        self.verticalLayout = QtWidgets.QVBoxLayout(DlgProfile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabProfile = QtWidgets.QTabWidget(DlgProfile)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.tabProfile.setPalette(palette)
        self.tabProfile.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabProfile.setObjectName("tabProfile")
        self.Summary = QtWidgets.QWidget()
        self.Summary.setFocusPolicy(QtCore.Qt.TabFocus)
        self.Summary.setObjectName("Summary")
        self.formLayoutWidget = QtWidgets.QWidget(self.Summary)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 161))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.lytSummary = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.lytSummary.setContentsMargins(0, 0, 0, 0)
        self.lytSummary.setObjectName("lytSummary")
        self.lblFirstName = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblFirstName.setFont(font)
        self.lblFirstName.setObjectName("lblFirstName")
        self.lytSummary.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblFirstName)
        self.ledFirstName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledFirstName.setReadOnly(True)
        self.ledFirstName.setObjectName("ledFirstName")
        self.lytSummary.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ledFirstName)
        self.lblLastName = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblLastName.setFont(font)
        self.lblLastName.setObjectName("lblLastName")
        self.lytSummary.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblLastName)
        self.ledLastName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledLastName.setReadOnly(True)
        self.ledLastName.setObjectName("ledLastName")
        self.lytSummary.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ledLastName)
        self.lblDOB = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblDOB.setFont(font)
        self.lblDOB.setObjectName("lblDOB")
        self.lytSummary.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lblDOB)
        self.ledDOB = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledDOB.setReadOnly(True)
        self.ledDOB.setObjectName("ledDOB")
        self.lytSummary.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ledDOB)
        self.lblIndications = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblIndications.setFont(font)
        self.lblIndications.setObjectName("lblIndications")
        self.lytSummary.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lblIndications)
        self.ledIndications = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledIndications.setReadOnly(True)
        self.ledIndications.setObjectName("ledIndications")
        self.lytSummary.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.ledIndications)
        self.lblGoal = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblGoal.setFont(font)
        self.lblGoal.setObjectName("lblGoal")
        self.lytSummary.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lblGoal)
        self.ledGoal = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledGoal.setReadOnly(True)
        self.ledGoal.setObjectName("ledGoal")
        self.lytSummary.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ledGoal)
        self.lblTTR = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblTTR.setFont(font)
        self.lblTTR.setObjectName("lblTTR")
        self.lytSummary.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lblTTR)
        self.ledTTR = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ledTTR.setReadOnly(True)
        self.ledTTR.setObjectName("ledTTR")
        self.lytSummary.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ledTTR)
        self.tabProfile.addTab(self.Summary, "")
        self.Results = QtWidgets.QWidget()
        self.Results.setObjectName("Results")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.Results)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 661, 431))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.lytResultsMain = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.lytResultsMain.setContentsMargins(0, 0, 0, 0)
        self.lytResultsMain.setObjectName("lytResultsMain")
        self.tblResult = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tblResult.setObjectName("tblResult")
        self.tblResult.setColumnCount(5)
        self.tblResult.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblResult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblResult.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblResult.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblResult.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tblResult.setHorizontalHeaderItem(4, item)
        self.lytResultsMain.addWidget(self.tblResult)
        self.lytResultRight = QtWidgets.QVBoxLayout()
        self.lytResultRight.setObjectName("lytResultRight")
        self.btnAdd = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnAdd.setObjectName("btnAdd")
        self.lytResultRight.addWidget(self.btnAdd)
        self.btnEdit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnEdit.setAutoDefault(False)
        self.btnEdit.setObjectName("btnEdit")
        self.lytResultRight.addWidget(self.btnEdit)
        self.btnDelete = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnDelete.setObjectName("btnDelete")
        self.lytResultRight.addWidget(self.btnDelete)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytResultRight.addItem(spacerItem)
        self.lytResultsMain.addLayout(self.lytResultRight)
        self.lblName = QtWidgets.QLabel(self.Results)
        self.lblName.setGeometry(QtCore.QRect(10, 10, 661, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblName.setFont(font)
        self.lblName.setObjectName("lblName")
        self.tabProfile.addTab(self.Results, "")
        self.Reports = QtWidgets.QWidget()
        self.Reports.setObjectName("Reports")
        self.tabProfile.addTab(self.Reports, "")
        self.verticalLayout.addWidget(self.tabProfile)

        self.retranslateUi(DlgProfile)
        self.tabProfile.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DlgProfile)

    def retranslateUi(self, DlgProfile):
        _translate = QtCore.QCoreApplication.translate
        DlgProfile.setWindowTitle(_translate("DlgProfile", "Patient Profile"))
        self.lblFirstName.setText(_translate("DlgProfile", "First Name"))
        self.lblLastName.setText(_translate("DlgProfile", "Last Name"))
        self.lblDOB.setText(_translate("DlgProfile", "Date of Birth"))
        self.lblIndications.setText(_translate("DlgProfile", "Indication(s)"))
        self.lblGoal.setText(_translate("DlgProfile", "INR Goal"))
        self.lblTTR.setText(_translate("DlgProfile", "TTR"))
        self.tabProfile.setTabText(self.tabProfile.indexOf(self.Summary), _translate("DlgProfile", "Summary"))
        item = self.tblResult.horizontalHeaderItem(0)
        item.setText(_translate("DlgProfile", "Date"))
        item = self.tblResult.horizontalHeaderItem(1)
        item.setText(_translate("DlgProfile", "INR"))
        item = self.tblResult.horizontalHeaderItem(2)
        item.setText(_translate("DlgProfile", "Goal"))
        item = self.tblResult.horizontalHeaderItem(3)
        item.setText(_translate("DlgProfile", "Total Dose"))
        item = self.tblResult.horizontalHeaderItem(4)
        item.setText(_translate("DlgProfile", "Comment"))
        self.btnAdd.setText(_translate("DlgProfile", "Add Result"))
        self.btnEdit.setText(_translate("DlgProfile", "Edit Result"))
        self.btnDelete.setText(_translate("DlgProfile", "Delete Result"))
        self.lblName.setText(_translate("DlgProfile", "Last name, First name"))
        self.tabProfile.setTabText(self.tabProfile.indexOf(self.Results), _translate("DlgProfile", "Results"))
        self.tabProfile.setTabText(self.tabProfile.indexOf(self.Reports), _translate("DlgProfile", "Reports"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgProfile = QtWidgets.QDialog()
    ui = Ui_DlgProfile()
    ui.setupUi(DlgProfile)
    DlgProfile.show()
    sys.exit(app.exec_())
