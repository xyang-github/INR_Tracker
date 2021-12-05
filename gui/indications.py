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
        DlgIndications.resize(355, 455)
        self.widget = QtWidgets.QWidget(DlgIndications)
        self.widget.setGeometry(QtCore.QRect(10, 10, 331, 431))
        self.widget.setObjectName("widget")
        self.lytMain = QtWidgets.QVBoxLayout(self.widget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.lblHeader = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblHeader.setFont(font)
        self.lblHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHeader.setObjectName("lblHeader")
        self.lytMain.addWidget(self.lblHeader)
        self.lytNewIndication = QtWidgets.QHBoxLayout()
        self.lytNewIndication.setObjectName("lytNewIndication")
        self.ledNewIndication = QtWidgets.QLineEdit(self.widget)
        self.ledNewIndication.setObjectName("ledNewIndication")
        self.lytNewIndication.addWidget(self.ledNewIndication)
        self.btnAdd = QtWidgets.QPushButton(self.widget)
        self.btnAdd.setObjectName("btnAdd")
        self.lytNewIndication.addWidget(self.btnAdd)
        self.lytMain.addLayout(self.lytNewIndication)
        self.lstIndications = QtWidgets.QListWidget(self.widget)
        self.lstIndications.setObjectName("lstIndications")
        self.lytMain.addWidget(self.lstIndications)
        self.lytBottomButtons = QtWidgets.QHBoxLayout()
        self.lytBottomButtons.setObjectName("lytBottomButtons")
        self.btnEdit = QtWidgets.QPushButton(self.widget)
        self.btnEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnEdit.setObjectName("btnEdit")
        self.lytBottomButtons.addWidget(self.btnEdit)
        self.btnDelete = QtWidgets.QPushButton(self.widget)
        self.btnDelete.setObjectName("btnDelete")
        self.lytBottomButtons.addWidget(self.btnDelete)
        self.btnExit = QtWidgets.QPushButton(self.widget)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgIndications = QtWidgets.QDialog()
    ui = Ui_DlgIndications()
    ui.setupUi(DlgIndications)
    DlgIndications.show()
    sys.exit(app.exec_())
