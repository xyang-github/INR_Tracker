# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'indications.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgIndications(object):
    def setupUi(self, DlgIndications):
        DlgIndications.setObjectName("DlgIndications")
        DlgIndications.resize(385, 456)
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
        DlgIndications.setPalette(palette)
        DlgIndications.setStyleSheet("QPushButton {\n"
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
"QLabel {\n"
"    color: #5E60CE;\n"
"    font-family: \"Raleway\";\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    margin-top: 10px;\n"
"}\n"
"")
        self.layoutWidget = QtWidgets.QWidget(DlgIndications)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 431))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Raleway")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.lblHeader.setFont(font)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytNewIndication = QtWidgets.QHBoxLayout()
        self.lytNewIndication.setObjectName("lytNewIndication")
        self.ledNewIndication = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledNewIndication.setObjectName("ledNewIndication")
        self.lytNewIndication.addWidget(self.ledNewIndication)
        self.btnAdd = QtWidgets.QPushButton(self.layoutWidget)
        self.btnAdd.setMinimumSize(QtCore.QSize(60, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName("btnAdd")
        self.lytNewIndication.addWidget(self.btnAdd)
        self.lytMain.addLayout(self.lytNewIndication)
        self.lstIndications = QtWidgets.QListWidget(self.layoutWidget)
        self.lstIndications.setObjectName("lstIndications")
        self.lytMain.addWidget(self.lstIndications)
        self.lytBottomButtons = QtWidgets.QHBoxLayout()
        self.lytBottomButtons.setObjectName("lytBottomButtons")
        self.btnEdit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.btnEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEdit.setIcon(icon1)
        self.btnEdit.setObjectName("btnEdit")
        self.lytBottomButtons.addWidget(self.btnEdit)
        self.btnDelete = QtWidgets.QPushButton(self.layoutWidget)
        self.btnDelete.setMinimumSize(QtCore.QSize(0, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon2)
        self.btnDelete.setObjectName("btnDelete")
        self.lytBottomButtons.addWidget(self.btnDelete)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExit.setMinimumSize(QtCore.QSize(0, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytBottomButtons.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytBottomButtons)

        self.retranslateUi(DlgIndications)
        QtCore.QMetaObject.connectSlotsByName(DlgIndications)

    def retranslateUi(self, DlgIndications):
        _translate = QtCore.QCoreApplication.translate
        DlgIndications.setWindowTitle(_translate("DlgIndications", "Indication List"))
        self.lblHeader.setText(_translate("DlgIndications", "Indication List"))
        self.ledNewIndication.setPlaceholderText(_translate("DlgIndications", "Type the name of the new indication here."))
        self.btnAdd.setText(_translate("DlgIndications", "Add"))
        self.btnEdit.setText(_translate("DlgIndications", "Edit"))
        self.btnDelete.setText(_translate("DlgIndications", "Delete"))
        self.btnExit.setText(_translate("DlgIndications", "Exit"))
import gui.resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgIndications = QtWidgets.QDialog()
    ui = Ui_DlgIndications()
    ui.setupUi(DlgIndications)
    DlgIndications.show()
    sys.exit(app.exec_())
