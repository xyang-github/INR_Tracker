# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editevent.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgEditEvent(object):
    def setupUi(self, DlgEditEvent):
        DlgEditEvent.setObjectName("DlgEditEvent")
        DlgEditEvent.setWindowModality(QtCore.Qt.ApplicationModal)
        DlgEditEvent.setFixedSize(341, 102)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 242, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        DlgEditEvent.setPalette(palette)
        DlgEditEvent.setStyleSheet(
            """
            QDialog {
                background-color: #f5f5f5;}
                
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
                border: none;
                border-bottom: 2px solid #00b4d8;
                padding: 10px;
                font-family:  \"Raleway\";
                font: 12px;
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;}                       
            """
        )
        self.layoutWidget = QtWidgets.QWidget(DlgEditEvent)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 78))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.ledEvent = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledEvent.setObjectName("ledEvent")
        self.lytMain.addWidget(self.ledEvent)
        self.lytButtons = QtWidgets.QHBoxLayout()
        self.lytButtons.setObjectName("lytButtons")
        self.btnOk = QtWidgets.QPushButton(self.layoutWidget)
        self.btnOk.setMinimumSize(QtCore.QSize(0, 25))
        self.btnOk.setObjectName("btnOk")
        self.lytButtons.addWidget(self.btnOk)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExit.setMinimumSize(QtCore.QSize(0, 25))
        self.btnExit.setObjectName("btnExit")
        self.lytButtons.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytButtons)

        self.retranslateUi(DlgEditEvent)
        QtCore.QMetaObject.connectSlotsByName(DlgEditEvent)

    def retranslateUi(self, DlgEditEvent):
        _translate = QtCore.QCoreApplication.translate
        DlgEditEvent.setWindowTitle(_translate("DlgEditEvent", "Edit Event"))
        self.btnOk.setText(_translate("DlgEditEvent", "OK"))
        self.btnExit.setText(_translate("DlgEditEvent", "Exit"))
import resource.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgEditEvent = QtWidgets.QDialog()
    ui = Ui_DlgEditEvent()
    ui.setupUi(DlgEditEvent)
    DlgEditEvent.show()
    sys.exit(app.exec_())
