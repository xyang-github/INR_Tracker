from main_ui import Ui_MainWindow
import sys
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

connection = QSqlDatabase.addDatabase("QSQLITE")
connection.setDatabaseName("inr_database.db")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Buttons(Ui_MainWindow):
    def __init__(self):
        self.search_button = main_ui.pushEnter
        self.search_button.clicked.connect("search_patient")

    def search_patient(self):
        print("works")


if __name__ == "__main__":
    if not connection.open():
        QMessageBox.critical(
            None,
            "Error!",
            "Database Error: {}".format(connection.lastError().databaseText(), ))
        print("Unable to connect to the database")
        sys.exit(1)
    else:
        myapp = QApplication(sys.argv)
        main = MainWindow()
        main.show()
        sys.exit(myapp.exec_())