from PyQt5.QtWidgets import QAction

from db import DB
from PyQt5 import QtCore, QtGui, QtWidgets
from addAcc import Ui_addAccountDialog
from addApp import Ui_AddAnApp

database = DB()


class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#         self.combo = ComboBox(self)
#         self.combo.popupAboutToBeShown.connect(self.populateCombo)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.combo)
#
#     def populateCombo(self):
#         if not self.combo.count():
#             self.combo.addItems('One Two Three Four'.split())


class MainWindow(object):
    def __init__(self, mainWindow):
        self.username = ''
        self.pass_word = ''
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(612, 480)
        mainWindow.setFixedSize(612, 480)
        mainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 250, 521, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.buttonsLayout = QtWidgets.QVBoxLayout(self.gridLayoutWidget)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setObjectName("buttonsLayout")

        # Font Setup

        font = QtGui.QFont()
        font.setFamily("Myriad Pro Cond")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        # Create Add New Account Button

        self.addNewAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.addNewAccount.clicked.connect(self.openAddAccount)
        self.addNewAccount.setFont(font)
        self.addNewAccount.setObjectName("addNewAccount")
        self.buttonsLayout.addWidget(self.addNewAccount)

        # Create Edit Current Account Button

        self.editCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.editCurrentAccount.setObjectName("editCurrentAccount")
        self.editCurrentAccount.setFont(font)
        self.editCurrentAccount.clicked.connect(self.DeleteCurrentAccountFunc)
        self.buttonsLayout.addWidget(self.editCurrentAccount)

        # Create Get App List Button

        self.getAppListOfCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.getAppListOfCurrentAccount.setFont(font)
        self.getAppListOfCurrentAccount.setObjectName("getAppListOfCurrentAccount")
        self.getAppListOfCurrentAccount.clicked.connect(self.getAppListOfCurrentAccountFunc)
        self.buttonsLayout.addWidget(self.getAppListOfCurrentAccount)

        # Create Manually add an app button

        self.manuallyAddAnApp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.manuallyAddAnApp.setFont(font)
        self.manuallyAddAnApp.setObjectName("manuallyAddAnApp")
        self.manuallyAddAnApp.clicked.connect(self.manuallyAddAnAppFunc)
        self.buttonsLayout.addWidget(self.manuallyAddAnApp)

        # Creates Status Text Label

        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(50, 140, 101, 31))
        self.status.setFont(font)
        self.status.setObjectName("status")

        # Setup the font for status text
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        font.setItalic(True)

        # Creates Welcome text of the top

        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(80, 180, 461, 21))
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet("QLabel{color:red; font-size:15px;}")
        self.statusLabel.setObjectName("statusLabel")

        # Setup the font for welcome text

        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(16)

        self.welcomeText = QtWidgets.QLabel(self.centralwidget)
        self.welcomeText.setGeometry(QtCore.QRect(100, 20, 411, 24))
        self.welcomeText.setFont(font)
        self.welcomeText.setObjectName("welcomeText")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 70, 531, 40))
        self.widget.setObjectName("widget")
        self.selectAccountLayout = QtWidgets.QHBoxLayout(self.widget)
        self.selectAccountLayout.setContentsMargins(0, 0, 0, 0)
        self.selectAccountLayout.setObjectName("selectAccountLayout")

        # Setup the font for Select Account Label
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)

        # Creates the Select Account Label

        self.selectAccount = QtWidgets.QLabel(self.widget)
        self.selectAccount.setFont(font)
        self.selectAccount.setObjectName("selectAccount")
        self.selectAccountLayout.addWidget(self.selectAccount)

        # Setup the font for the Select Account combo box

        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(18)

        # Creates the combo box

        self.comboBox = ComboBox()
        self.comboBox.setEnabled(True)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem('Select an account')

        # Connect the functions to retrieve data from DB
        self.comboBox.popupAboutToBeShown.connect(self.populateCombo)
        self.comboBox.currentTextChanged.connect(self.select_account_name)
        # Add the combo box to layout
        self.selectAccountLayout.addWidget(self.comboBox)

        mainWindow.setCentralWidget(self.centralwidget)

        # Creates the menu bar

        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 612, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.actionExit_2 = QtWidgets.QAction(mainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        self.actionExit_2.triggered.connect(self.close_window)
        
        self.actionAbout = QAction(mainWindow)
        self.actionAbout.setObjectName('actionAbout')
        self.actionAbout.triggered.connect(self.about_dialog)
        
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuAbout.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        # Menu Bar ends

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        # Adds the add account window to main window

        self.addAccountDialog = QtWidgets.QDialog()
        self.ui = Ui_addAccountDialog()
        self.ui.setupUi(self.addAccountDialog)

    def populateCombo(self):    # Method that retrieves all accounts from DB and place them in the combo box
        self.comboBox.clear()
        accounts = database.fetch_data('accounts')
        for account in accounts:
            self.comboBox.addItem(account[0])

    def select_account_name(self):  # Method that fetches the password for selected account
        accountInfo = database.fetch_account_password(self.comboBox.currentText())
        if accountInfo is not None:
            self.username = accountInfo[0]
            self.pass_word = accountInfo[1]
        else:
            self.username = ''
            self.pass_word = ''

        print(self.username, self.pass_word)

    def openAddAccount(self):   # Method to open the Add account window
        try:
            self.ui.pushButton.clicked.connect(self.ui.add_account_clicked)
            self.populateCombo()
        except Exception as err:
            print(err)
        self.addAccountDialog.show()

    def DeleteCurrentAccountFunc(self):
        currentAccount = self.comboBox.currentText()
        currentAccountIndex = self.comboBox.currentIndex()
        self.addAccountDialog = QtWidgets.QDialog()
        self.ui = Ui_addAccountDialog()
        self.ui.setupUi(self.addAccountDialog)

        if currentAccount == "Select an account":
            self.ui.infoOfAccAdd.setText('Selected account is not a valid account')
            self.ui.infoOfAccAdd.setStyleSheet('color:red')
        else:
            database.delete_data_from_accounts(currentAccount)
            self.comboBox.removeItem(currentAccountIndex)
            self.ui.infoOfAccAdd.setText('Account Deleted Successfully')
            self.ui.infoOfAccAdd.setStyleSheet('color:green')

        self.ui.pushButton.setText('Delete This Account')
        self.addAccountDialog.show()

    def manuallyAddAnAppFunc(self):
        self.AddAnApp = QtWidgets.QDialog()
        self.ui = Ui_AddAnApp()
        self.ui.setupUi(self.AddAnApp)
        self.AddAnApp.show()

    def getAppListOfCurrentAccountFunc(self):
        print('dasd')

    def close_window(self):
        exit(0)

    def about_dialog(self):
        newWindow = QtWidgets.QWidget()
        newWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        newWindow.setGeometry(200, 200, 340, 200)
        QtWidgets.QMessageBox.about(newWindow, "About bdapps content uploader ", "Version: 1.0\nDeveloper: SM Tamim Mahmud!")

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "BDApps Content Uploader"))
        self.addNewAccount.setText(_translate("mainWindow", "Add New Account"))
        self.editCurrentAccount.setText(_translate("mainWindow", "Delete Current Account"))
        self.getAppListOfCurrentAccount.setText(_translate("mainWindow", "Get App List of Current Account"))
        self.manuallyAddAnApp.setText(_translate("mainWindow", "Manually Add An App To This Account"))
        self.status.setText(_translate("mainWindow", "STATUS:"))
        self.statusLabel.setText(_translate("mainWindow", "TextLabel"))
        self.welcomeText.setText(_translate("mainWindow", "Welcome to BDApps Content Uploader"))
        self.selectAccount.setText(_translate("mainWindow", "Select an account:"))
        self.comboBox.setToolTip(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Select the account for which you want to upload content.</span></p></body></html>"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuAbout.setTitle(_translate("mainWindow", "About"))
        self.actionExit_2.setText(_translate("mainWindow", "Exit"))
        self.actionExit_2.setShortcut(_translate("mainWindow", "Alt+Q"))
        self.actionAbout.setText(_translate("mainWindow", "About"))
        self.actionAbout.setShortcut(_translate("mainWindow", "Alt+A"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


