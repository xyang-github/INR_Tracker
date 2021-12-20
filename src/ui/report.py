# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'report.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgReport(object):
    def setupUi(self, DlgReport):
        DlgReport.setObjectName("DlgReport")
        DlgReport.setFixedSize(435, 646)
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
        DlgReport.setPalette(palette)
        DlgReport.setStyleSheet(
            """
            QDialog {
                background-color: #f5f5f5;}
                
            QLabel{
                font-family: \"Source Sans Pro\";
                font-size: 16px;
                font-weight: bold;
                color: #696969;}
            }
    
            QLabel#lblHeader{
                color: #5E60CE;
                font-family: \"Source Sans Pro\";
                font-size: 24px;
                }
            
            QRadioButton{
                spacing: 10px;
                color: #555555;
                line-height: 14px;
                height: 30px;
                background-color: transparent;
                spacing: 5px;}

            QRadioButton:disabled{
              color: {{#555555|opacity(0.3)}};}

            QRadioButton::indicator {
                background-color: transparent;
                width: 24px;
                height: 24px;
                border-radius: 4px;}
 
            QRadioButton::indicator:checked {
                image: url(../resource/icon/radio button checked.svg);}
            
            QRadioButton::indicator:unchecked {
                image: url(../resource/icon/radio button unchecked.svg);}
    
            QPushButton {
                background-color: #00b4d8;
                color: white;
                border-radius: 8px;
                font-family: \"Raleway\";
                font-size: 12px;
                border: none;}
    
            QPushButton::hover {
                background-color: #b3e9f3;}  
            """
        )
        self.layoutWidget = QtWidgets.QWidget(DlgReport)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 411, 621))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblHeader.setFont(font)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytRbtn = QtWidgets.QHBoxLayout()
        self.lytRbtn.setObjectName("lytRbtn")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytRbtn.addItem(spacerItem)
        self.rbtnAllPatients = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtnAllPatients.setObjectName("rbtAll")
        self.buttonGroup = QtWidgets.QButtonGroup(DlgReport)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.rbtnAllPatients)
        self.lytRbtn.addWidget(self.rbtnAllPatients)
        self.rbtnActivePatients = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtnActivePatients.setChecked(True)
        self.rbtnActivePatients.setObjectName("rbtActive")
        self.buttonGroup.addButton(self.rbtnActivePatients)
        self.lytRbtn.addWidget(self.rbtnActivePatients)
        self.rbtnInactivePatients = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbtnInactivePatients.setObjectName("rbtInactive")
        self.buttonGroup.addButton(self.rbtnInactivePatients)
        self.lytRbtn.addWidget(self.rbtnInactivePatients)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytRbtn.addItem(spacerItem1)
        self.lytMain.addLayout(self.lytRbtn)
        self.tedReport = QtWidgets.QTextEdit(self.layoutWidget)
        self.tedReport.setReadOnly(True)
        self.tedReport.setObjectName("tedReport")
        self.lytMain.addWidget(self.tedReport)
        self.lytButtons = QtWidgets.QHBoxLayout()
        self.lytButtons.setObjectName("lytButtons")
        self.btnPatientList = QtWidgets.QPushButton(self.layoutWidget)
        self.btnPatientList.setMinimumSize(QtCore.QSize(0, 30))
        self.btnPatientList.setObjectName("btnPatientList")
        self.lytButtons.addWidget(self.btnPatientList)
        self.btnPDF = QtWidgets.QPushButton(self.layoutWidget)
        self.btnPDF.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPDF.setIcon(icon)
        self.btnPDF.setObjectName("btnPDF")
        self.lytButtons.addWidget(self.btnPDF)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExit.setMinimumSize(QtCore.QSize(0, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytButtons.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytButtons)

        self.retranslateUi(DlgReport)
        QtCore.QMetaObject.connectSlotsByName(DlgReport)

    def retranslateUi(self, DlgReport):
        _translate = QtCore.QCoreApplication.translate
        DlgReport.setWindowTitle(_translate("DlgReport", "Clinic Report"))
        self.lblHeader.setText(_translate("DlgReport", "Clinic Report"))
        self.rbtnAllPatients.setText(_translate("DlgReport", "All"))
        self.rbtnActivePatients.setText(_translate("DlgReport", "Active"))
        self.rbtnInactivePatients.setText(_translate("DlgReport", "Inactive"))
        self.btnPatientList.setText(_translate("DlgReport", "Patient List"))
        self.btnPDF.setText(_translate("DlgReport", "Export to PDF"))
        self.btnExit.setText(_translate("DlgReport", "Exit"))
import resource.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgReport = QtWidgets.QDialog()
    ui = Ui_DlgReport()
    ui.setupUi(DlgReport)
    DlgReport.show()
    sys.exit(app.exec_())
