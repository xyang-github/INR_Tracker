# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgHelp(object):
    def setupUi(self, DlgHelp):
        DlgHelp.setObjectName("DlgHelp")
        DlgHelp.resize(853, 853)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DlgHelp.sizePolicy().hasHeightForWidth())
        DlgHelp.setSizePolicy(sizePolicy)
        DlgHelp.setMinimumSize(QtCore.QSize(853, 853))
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
        DlgHelp.setPalette(palette)
        DlgHelp.setStyleSheet("QDialog {\n"
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
"QTextBrowser {\n"
"    border: 2px  solid gray;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    font-family:  \"Raleway\";\n"
"    font: 12px;\n"
"\n"
"}\n"
"\n"
"\n"
"QLabel#lblHeader {\n"
"    color: #00b4d8;\n"
"    font-size: 24px;    \n"
"    font-weight: bold;\n"
"    font-family: \"Source Sans Pro\";\n"
"    border: 2px solid #00b4d8;\n"
"    border-radius: 10px;\n"
"}")
        self.layoutWidget = QtWidgets.QWidget(DlgHelp)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 831, 821))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.layoutWidget)
        self.lblHeader.setMinimumSize(QtCore.QSize(0, 0))
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.tbrDocument = QtWidgets.QTextBrowser(self.layoutWidget)
        self.tbrDocument.setObjectName("tbrDocument")
        self.lytMain.addWidget(self.tbrDocument)
        self.lytButton = QtWidgets.QHBoxLayout()
        self.lytButton.setObjectName("lytButton")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytButton.addItem(spacerItem)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExit.setMinimumSize(QtCore.QSize(60, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytButton.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytButton)

        self.retranslateUi(DlgHelp)
        QtCore.QMetaObject.connectSlotsByName(DlgHelp)

    def retranslateUi(self, DlgHelp):
        _translate = QtCore.QCoreApplication.translate
        DlgHelp.setWindowTitle(_translate("DlgHelp", "Help"))
        self.lblHeader.setText(_translate("DlgHelp", "Help"))
        self.btnExit.setText(_translate("DlgHelp", "Exit"))
import resource.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgHelp = QtWidgets.QDialog()
    ui = Ui_DlgHelp()
    ui.setupUi(DlgHelp)
    DlgHelp.show()
    sys.exit(app.exec_())
