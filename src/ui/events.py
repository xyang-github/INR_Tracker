# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'events.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgEvents(object):
    def setupUi(self, DlgEvents):
        DlgEvents.setObjectName("DlgEvents")
        DlgEvents.resize(385, 456)
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
        DlgEvents.setPalette(palette)
        DlgEvents.setStyleSheet("QPushButton {\n"
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
"    border: 2px  solid gray;\n"
"    border-radius: 20px;\n"
"    padding: 10px;\n"
"    font-family:  \"Raleway\";\n"
"    font: 12px;\n"
"\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #00b4d8;\n"
"    font-family: \"Source Sans Pro\";\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    border: 2px solid #00b4d8;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.layoutWidget = QtWidgets.QWidget(DlgEvents)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 431))
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
        self.lytNewEvent = QtWidgets.QHBoxLayout()
        self.lytNewEvent.setObjectName("lytNewEvent")
        self.ledNewEvent = QtWidgets.QLineEdit(self.layoutWidget)
        self.ledNewEvent.setObjectName("ledNewEvent")
        self.lytNewEvent.addWidget(self.ledNewEvent)
        self.btnAddEvent = QtWidgets.QPushButton(self.layoutWidget)
        self.btnAddEvent.setMinimumSize(QtCore.QSize(60, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddEvent.setIcon(icon)
        self.btnAddEvent.setObjectName("btnAddEvent")
        self.lytNewEvent.addWidget(self.btnAddEvent)
        self.lytMain.addLayout(self.lytNewEvent)
        self.lstEvents = QtWidgets.QListWidget(self.layoutWidget)
        self.lstEvents.setObjectName("lstEvents")
        self.lytMain.addWidget(self.lstEvents)
        self.lytBottomButtons = QtWidgets.QHBoxLayout()
        self.lytBottomButtons.setObjectName("lytBottomButtons")
        self.btnEditEvent = QtWidgets.QPushButton(self.layoutWidget)
        self.btnEditEvent.setMinimumSize(QtCore.QSize(0, 30))
        self.btnEditEvent.setFocusPolicy(QtCore.Qt.NoFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/icon/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEditEvent.setIcon(icon1)
        self.btnEditEvent.setObjectName("btnEditEvent")
        self.lytBottomButtons.addWidget(self.btnEditEvent)
        self.btnDeleteEvent = QtWidgets.QPushButton(self.layoutWidget)
        self.btnDeleteEvent.setMinimumSize(QtCore.QSize(0, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDeleteEvent.setIcon(icon2)
        self.btnDeleteEvent.setObjectName("btnDeleteEvent")
        self.lytBottomButtons.addWidget(self.btnDeleteEvent)
        self.btnExit = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExit.setMinimumSize(QtCore.QSize(0, 30))
        self.btnExit.setObjectName("btnExit")
        self.lytBottomButtons.addWidget(self.btnExit)
        self.lytMain.addLayout(self.lytBottomButtons)

        self.retranslateUi(DlgEvents)
        QtCore.QMetaObject.connectSlotsByName(DlgEvents)

    def retranslateUi(self, DlgEvents):
        _translate = QtCore.QCoreApplication.translate
        DlgEvents.setWindowTitle(_translate("DlgEvents", "Event List"))
        self.lblHeader.setText(_translate("DlgEvents", "Event List"))
        self.ledNewEvent.setPlaceholderText(_translate("DlgEvents", "Type the name of the new event here."))
        self.btnAddEvent.setText(_translate("DlgEvents", "Add"))
        self.btnEditEvent.setText(_translate("DlgEvents", "Edit"))
        self.btnDeleteEvent.setText(_translate("DlgEvents", "Delete"))
        self.btnExit.setText(_translate("DlgEvents", "Exit"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgEvents = QtWidgets.QDialog()
    ui = Ui_DlgEvents()
    ui.setupUi(DlgEvents)
    DlgEvents.show()
    sys.exit(app.exec_())
