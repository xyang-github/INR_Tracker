# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_update_result.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgAddResult(object):
    def setupUi(self, DlgAddResult):
        DlgAddResult.setObjectName("DlgAddResult")
        DlgAddResult.resize(264, 862)
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
        DlgAddResult.setPalette(palette)
        DlgAddResult.setStyleSheet(
            """
        QDialog {
                background-color: #f5f5f5;}
        
        QLabel {
                font-family: \"Source Sans Pro\";
                font-size: 16px;
                font-weight: bold;
                color: #696969;}

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
                border-left: 2px solid #00b4d8;
                border-right: 2px solid #00b4d8;
                padding: 10px;
                font-family:  \"Raleway\";
                font: 12px;
                border-radius: 10px;} 
                
        QTextEdit{
            border: 2px dashed #00b4d8; 
            border-radius:10px; 
            background-color: palette(base);
            padding: 15px;}            
            """
        )
        self.layoutWidget = QtWidgets.QWidget(DlgAddResult)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 241, 841))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lytDateResult = QtWidgets.QFormLayout()
        self.lytDateResult.setObjectName("lytDateResult")
        self.lblDate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblDate.setFont(font)
        self.lblDate.setObjectName("lblDate")
        self.lytDateResult.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblDate)
        self.dteDate = QtWidgets.QDateEdit(self.layoutWidget)
        self.dteDate.setMinimumSize(QtCore.QSize(0, 25))
        self.dteDate.setDateTime(QtCore.QDateTime(QtCore.QDate(2021, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dteDate.setCalendarPopup(True)
        self.dteDate.setObjectName("dteDate")
        self.lytDateResult.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dteDate)
        self.ledResult = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledResult.setMinimumSize(QtCore.QSize(0, 40))
        self.ledResult.setObjectName("ledResult")
        self.lytDateResult.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ledResult)
        self.lblResult = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblResult.setFont(font)
        self.lblResult.setObjectName("lblResult")
        self.lytDateResult.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblResult)
        self.lytMain.addLayout(self.lytDateResult)
        self.line1 = QtWidgets.QFrame(self.layoutWidget)
        self.line1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setObjectName("line1")
        self.lytMain.addWidget(self.line1)
        self.lytDose = QtWidgets.QVBoxLayout()
        self.lytDose.setObjectName("lytDose")
        self.lblDoseTitle = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblDoseTitle.setFont(font)
        self.lblDoseTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblDoseTitle.setObjectName("lblDoseTitle")
        self.lytDose.addWidget(self.lblDoseTitle)
        self.chkNoChanges = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.chkNoChanges.setFont(font)
        self.chkNoChanges.setObjectName("chkNoChanges")
        self.lytDose.addWidget(self.chkNoChanges)
        self.lytDailyDoses = QtWidgets.QFormLayout()
        self.lytDailyDoses.setObjectName("lytDailyDoses")
        self.lblMonday = QtWidgets.QLabel(self.layoutWidget)
        self.lblMonday.setObjectName("lblMonday")
        self.lytDailyDoses.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblMonday)
        self.ledMonday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledMonday.setMinimumSize(QtCore.QSize(0, 20))
        self.ledMonday.setObjectName("ledMonday")
        self.lytDailyDoses.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ledMonday)
        self.lblTuesday = QtWidgets.QLabel(self.layoutWidget)
        self.lblTuesday.setObjectName("lblTuesday")
        self.lytDailyDoses.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblTuesday)
        self.ledTuesday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledTuesday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledTuesday.setObjectName("ledTuesday")
        self.lytDailyDoses.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ledTuesday)
        self.lblWednesday = QtWidgets.QLabel(self.layoutWidget)
        self.lblWednesday.setObjectName("lblWednesday")
        self.lytDailyDoses.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lblWednesday)
        self.ledWednesday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledWednesday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledWednesday.setObjectName("ledWednesday")
        self.lytDailyDoses.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ledWednesday)
        self.lblThursday = QtWidgets.QLabel(self.layoutWidget)
        self.lblThursday.setObjectName("lblThursday")
        self.lytDailyDoses.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lblThursday)
        self.ledThursday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledThursday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledThursday.setObjectName("ledThursday")
        self.lytDailyDoses.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.ledThursday)
        self.lblFriday = QtWidgets.QLabel(self.layoutWidget)
        self.lblFriday.setObjectName("lblFriday")
        self.lytDailyDoses.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lblFriday)
        self.ledFriday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledFriday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledFriday.setObjectName("ledFriday")
        self.lytDailyDoses.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ledFriday)
        self.lblSaturday = QtWidgets.QLabel(self.layoutWidget)
        self.lblSaturday.setObjectName("lblSaturday")
        self.lytDailyDoses.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lblSaturday)
        self.ledSaturday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledSaturday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledSaturday.setObjectName("ledSaturday")
        self.lytDailyDoses.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ledSaturday)
        self.lblSunday = QtWidgets.QLabel(self.layoutWidget)
        self.lblSunday.setObjectName("lblSunday")
        self.lytDailyDoses.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lblSunday)
        self.ledSunday = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledSunday.setMinimumSize(QtCore.QSize(0, 30))
        self.ledSunday.setObjectName("ledSunday")
        self.lytDailyDoses.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.ledSunday)
        self.lblTotal = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblTotal.setFont(font)
        self.lblTotal.setObjectName("lblTotal")
        self.lytDailyDoses.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.lblTotal)
        self.ledTotal = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledTotal.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ledTotal.setFont(font)
        self.ledTotal.setReadOnly(True)
        self.ledTotal.setObjectName("ledTotal")
        self.lytDailyDoses.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.ledTotal)
        self.lytDose.addLayout(self.lytDailyDoses)
        self.lytMain.addLayout(self.lytDose)
        self.line2 = QtWidgets.QFrame(self.layoutWidget)
        self.line2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setObjectName("line2")
        self.lytMain.addWidget(self.line2)
        self.lytGoal = QtWidgets.QVBoxLayout()
        self.lytGoal.setObjectName("lytGoal")
        self.lblGoal = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblGoal.setFont(font)
        self.lblGoal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblGoal.setObjectName("lblGoal")
        self.lytGoal.addWidget(self.lblGoal)
        self.rbtnGoalDefault = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtnGoalDefault.setChecked(True)
        self.rbtnGoalDefault.setObjectName("rbtn_Goal_Default")
        self.rbtnGroup_Goal = QtWidgets.QButtonGroup(DlgAddResult)
        self.rbtnGroup_Goal.setObjectName("rbtnGroup_Goal")
        self.rbtnGroup_Goal.addButton(self.rbtnGoalDefault)
        self.lytGoal.addWidget(self.rbtnGoalDefault)
        self.rbtnGoalNew = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtnGoalNew.setObjectName("rbtnGoal_New")
        self.rbtnGroup_Goal.addButton(self.rbtnGoalNew)
        self.lytGoal.addWidget(self.rbtnGoalNew)
        self.gbxNewGoal = QtWidgets.QGroupBox(self.layoutWidget)
        self.gbxNewGoal.setCheckable(False)
        self.gbxNewGoal.setChecked(False)
        self.gbxNewGoal.setObjectName("gbxNewGoal")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbxNewGoal)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblNewGoalFrom = QtWidgets.QLabel(self.gbxNewGoal)
        self.lblNewGoalFrom.setObjectName("lblNewGoalFrom")
        self.horizontalLayout.addWidget(self.lblNewGoalFrom)
        self.ledNewGoalFrom = QtWidgets.QLineEdit(self.gbxNewGoal)
        self.ledNewGoalFrom.setMinimumSize(QtCore.QSize(0, 40))
        self.ledNewGoalFrom.setObjectName("ledNewGoalFrom")
        self.horizontalLayout.addWidget(self.ledNewGoalFrom)
        self.lblNewGoalTo = QtWidgets.QLabel(self.gbxNewGoal)
        self.lblNewGoalTo.setObjectName("lblNewGoalTo")
        self.horizontalLayout.addWidget(self.lblNewGoalTo)
        self.ledNewGoalTo = QtWidgets.QLineEdit(self.gbxNewGoal)
        self.ledNewGoalTo.setMinimumSize(QtCore.QSize(0, 40))
        self.ledNewGoalTo.setObjectName("ledNewGoalTo")
        self.horizontalLayout.addWidget(self.ledNewGoalTo)
        self.lytGoal.addWidget(self.gbxNewGoal)
        self.lytMain.addLayout(self.lytGoal)
        self.line3 = QtWidgets.QFrame(self.layoutWidget)
        self.line3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setObjectName("line3")
        self.lytMain.addWidget(self.line3)
        self.lytComment = QtWidgets.QVBoxLayout()
        self.lytComment.setObjectName("lytComment")
        self.lblComment = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblComment.setFont(font)
        self.lblComment.setAlignment(QtCore.Qt.AlignCenter)
        self.lblComment.setObjectName("lblComment")
        self.lytComment.addWidget(self.lblComment)
        self.txtComment = QtWidgets.QTextEdit(self.layoutWidget)
        self.txtComment.setTabChangesFocus(False)
        self.txtComment.setObjectName("txtComment")
        self.lytComment.addWidget(self.txtComment)
        self.lytMain.addLayout(self.lytComment)
        self.lytButton = QtWidgets.QHBoxLayout()
        self.lytButton.setObjectName("lytButton")
        self.btnOK = QtWidgets.QPushButton(self.layoutWidget)
        self.btnOK.setMinimumSize(QtCore.QSize(0, 25))
        self.btnOK.setObjectName("btnOK")
        self.lytButton.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(self.layoutWidget)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 25))
        self.btnCancel.setObjectName("btnCancel")
        self.lytButton.addWidget(self.btnCancel)
        self.lytMain.addLayout(self.lytButton)

        self.retranslateUi(DlgAddResult)
        QtCore.QMetaObject.connectSlotsByName(DlgAddResult)
        DlgAddResult.setTabOrder(self.dteDate, self.ledResult)
        DlgAddResult.setTabOrder(self.ledResult, self.chkNoChanges)
        DlgAddResult.setTabOrder(self.chkNoChanges, self.ledMonday)
        DlgAddResult.setTabOrder(self.ledMonday, self.ledTuesday)
        DlgAddResult.setTabOrder(self.ledTuesday, self.ledWednesday)
        DlgAddResult.setTabOrder(self.ledWednesday, self.ledThursday)
        DlgAddResult.setTabOrder(self.ledThursday, self.ledFriday)
        DlgAddResult.setTabOrder(self.ledFriday, self.ledSaturday)
        DlgAddResult.setTabOrder(self.ledSaturday, self.ledSunday)
        DlgAddResult.setTabOrder(self.ledSunday, self.rbtnGoalDefault)
        DlgAddResult.setTabOrder(self.rbtnGoalDefault, self.rbtnGoalNew)
        DlgAddResult.setTabOrder(self.rbtnGoalNew, self.ledNewGoalFrom)
        DlgAddResult.setTabOrder(self.ledNewGoalFrom, self.ledNewGoalTo)
        DlgAddResult.setTabOrder(self.ledNewGoalTo, self.txtComment)
        DlgAddResult.setTabOrder(self.txtComment, self.btnOK)
        DlgAddResult.setTabOrder(self.btnOK, self.btnCancel)
        DlgAddResult.setTabOrder(self.btnCancel, self.ledTotal)

    def retranslateUi(self, DlgAddResult):
        _translate = QtCore.QCoreApplication.translate
        DlgAddResult.setWindowTitle(_translate("DlgAddResult", "Add Result"))
        self.lblDate.setText(_translate("DlgAddResult", "Date"))
        self.dteDate.setToolTip(_translate("DlgAddResult", "Enter date of the blood draw"))
        self.ledResult.setToolTip(_translate("DlgAddResult", "Enter the INR result"))
        self.ledResult.setPlaceholderText(_translate("DlgAddResult", "Enter INR result"))
        self.lblResult.setText(_translate("DlgAddResult", "Result"))
        self.lblDoseTitle.setText(_translate("DlgAddResult", "Dose"))
        self.chkNoChanges.setToolTip(_translate("DlgAddResult", "Click the checkbox if no changes were made to the regimen from the patient\'s last appointment."))
        self.chkNoChanges.setText(_translate("DlgAddResult", "No Changes"))
        self.lblMonday.setText(_translate("DlgAddResult", "Monday"))
        self.lblTuesday.setText(_translate("DlgAddResult", "Tuesday"))
        self.lblWednesday.setText(_translate("DlgAddResult", "Wednesday"))
        self.lblThursday.setText(_translate("DlgAddResult", "Thursday"))
        self.lblFriday.setText(_translate("DlgAddResult", "Friday"))
        self.lblSaturday.setText(_translate("DlgAddResult", "Saturday"))
        self.lblSunday.setText(_translate("DlgAddResult", "Sunday"))
        self.lblTotal.setText(_translate("DlgAddResult", "Total"))
        self.lblGoal.setText(_translate("DlgAddResult", "INR Goal"))
        self.rbtnGoalDefault.setText(_translate("DlgAddResult", "Default"))
        self.rbtnGoalNew.setText(_translate("DlgAddResult", "New"))
        self.lblNewGoalFrom.setText(_translate("DlgAddResult", "From:"))
        self.lblNewGoalTo.setText(_translate("DlgAddResult", "To:"))
        self.lblComment.setText(_translate("DlgAddResult", "Comment"))
        self.txtComment.setToolTip(_translate("DlgAddResult", "Add clinically relevant comments"))
        self.txtComment.setPlaceholderText(_translate("DlgAddResult", "Type any clinically relevant information pertaining to the result."))
        self.btnOK.setText(_translate("DlgAddResult", "OK"))
        self.btnCancel.setText(_translate("DlgAddResult", "Cancel"))
import resource.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgAddResult = QtWidgets.QDialog()
    ui = Ui_DlgAddResult()
    ui.setupUi(DlgAddResult)
    DlgAddResult.show()
    sys.exit(app.exec_())
