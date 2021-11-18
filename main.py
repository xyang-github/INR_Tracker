import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from gui.main_ui import *


class DlgMain(QMainWindow, Ui_dlgMain):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        # event handlers
        self.actionExit.triggered.connect(self.evt_actionExit_triggered)  # exit signal
        self.btnSearch.clicked.connect(self.evt_btnSearch_clicked)


    def evt_btnSearch_clicked(self):
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("database.db")
        if database.open():
            pass
        else:
            QMessageBox.critical(self, "Database Error", "Could not connect with the database.")

    def evt_actionExit_triggered(self):
        """
        Exit the program when user clicks on File > Exit
        """
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
