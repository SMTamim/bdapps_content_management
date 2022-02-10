from PyQt5.QtWidgets import QAction, QMessageBox

from db import DB
from PyQt5 import QtCore, QtGui, QtWidgets
from addAcc import Ui_addAccountDialog
from addApp import Ui_AddAnApp
from deleteApp import UiRemoveAppDialog
import resources

database = DB()
username_global = ''
status_text_global = ''


class FlashingText(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(FlashingText, self).__init__(*args, **kwargs)
        effect = QtWidgets.QGraphicsColorizeEffect(self)
        self.setGraphicsEffect(effect)
        self.animation = QtCore.QPropertyAnimation(effect, b"color")

        self.animation.setStartValue(QtGui.QColor(0, 255, 255))
        self.animation.setEndValue(QtGui.QColor(255, 0, 0))

        self.animation.setLoopCount(3)
        self.animation.setDuration(333)


class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


class MainWindow(object):
    def __init__(self, mainWindow):
        self.username = ''
        self.pass_word = ''
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(612, 480)
        mainWindow.setFixedSize(612, 480)
        mainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.central_widget = QtWidgets.QWidget(mainWindow)
        self.central_widget.setObjectName("central_widget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 250, 521, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.buttonsLayout = QtWidgets.QVBoxLayout(self.gridLayoutWidget)
        # self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setObjectName("buttonsLayout")

        # INFO:Font Setup

        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        buttonsLayout_hBox = QtWidgets.QHBoxLayout()
        # INFO:Create Add New Account Button

        self.addNewAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.addNewAccount.clicked.connect(self.openAddAccount)
        self.addNewAccount.setFont(font)
        self.addNewAccount.setObjectName("addNewAccount")
        buttonsLayout_hBox.addWidget(self.addNewAccount)

        # INFO:Create Edit Current Account Button

        self.editCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.editCurrentAccount.setObjectName("editCurrentAccount")
        self.editCurrentAccount.setFont(font)
        self.editCurrentAccount.clicked.connect(self.DeleteCurrentAccountFunc)
        buttonsLayout_hBox.addWidget(self.editCurrentAccount)

        self.buttonsLayout.addLayout(buttonsLayout_hBox)

        buttonsLayout_hBox2 = QtWidgets.QHBoxLayout()
        # INFO:Create Get App List Button

        self.getAppListOfCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.getAppListOfCurrentAccount.setFont(font)
        self.getAppListOfCurrentAccount.setObjectName("getAppListOfCurrentAccount")
        self.getAppListOfCurrentAccount.clicked.connect(self.getAppListOfCurrentAccountFunc)
        buttonsLayout_hBox2.addWidget(self.getAppListOfCurrentAccount)

        # INFO:Create Open App List Button

        self.openAppListOfCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.openAppListOfCurrentAccount.setFont(font)
        self.openAppListOfCurrentAccount.setObjectName("openAppListOfCurrentAccount")
        self.openAppListOfCurrentAccount.clicked.connect(self.openAppListOfCurrentAccountFunc)
        buttonsLayout_hBox2.addWidget(self.openAppListOfCurrentAccount)

        # INFO:Create Manually add an app button

        self.manuallyAddAnApp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.manuallyAddAnApp.setFont(font)
        self.manuallyAddAnApp.setObjectName("manuallyAddAnApp")
        self.manuallyAddAnApp.clicked.connect(self.manuallyAddAnAppFunc)
        buttonsLayout_hBox2.addWidget(self.manuallyAddAnApp)

        self.buttonsLayout.addLayout(buttonsLayout_hBox2)

        # INFO: Adds the Remove an app button

        self.removeAnApp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.removeAnApp.setFont(font)
        self.removeAnApp.setObjectName("removeAnApp")
        self.removeAnApp.clicked.connect(self.removeAnAppFunc)
        self.buttonsLayout.addWidget(self.removeAnApp)

        # INFO:Creates Status Text Label

        self.status = QtWidgets.QLabel(self.central_widget)
        self.status.setGeometry(QtCore.QRect(50, 140, 101, 31))
        self.status.setFont(font)
        self.status.setObjectName("status")

        # INFO:Setup the font for status text
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        font.setItalic(True)

        # INFO:Creates Welcome text of the top

        self.statusLabel = FlashingText(self.central_widget)
        self.statusLabel.setGeometry(QtCore.QRect(80, 180, 461, 21))
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet("QLabel{color:red; font-size:15px;}")
        self.statusLabel.setObjectName("statusLabel")

        # INFO:Setup the font for welcome text

        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(16)

        self.welcomeText = QtWidgets.QLabel(self.central_widget)
        self.welcomeText.setGeometry(QtCore.QRect(100, 20, 411, 24))
        self.welcomeText.setFont(font)
        self.welcomeText.setObjectName("welcomeText")

        self.widget = QtWidgets.QWidget(self.central_widget)
        self.widget.setGeometry(QtCore.QRect(40, 70, 531, 40))
        self.widget.setObjectName("widget")
        self.selectAccountLayout = QtWidgets.QHBoxLayout(self.widget)
        self.selectAccountLayout.setContentsMargins(0, 0, 0, 0)
        self.selectAccountLayout.setObjectName("selectAccountLayout")

        # INFO:Setup the font for Select Account Label
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)

        # INFO:Creates the Select Account Label

        self.selectAccount = QtWidgets.QLabel(self.widget)
        self.selectAccount.setFont(font)
        self.selectAccount.setObjectName("selectAccount")
        self.selectAccountLayout.addWidget(self.selectAccount)

        # INFO:Setup the font for the Select Account combo box

        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(18)

        # INFO:Creates the combo box

        self.comboBox = ComboBox()
        self.comboBox.setEnabled(True)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem('Select an account')

        # INFO:Connect the functions to retrieve data from DB
        self.comboBox.popupAboutToBeShown.connect(self.populateCombo)
        self.comboBox.currentTextChanged.connect(self.select_account_name)
        # Info: Add the combo box to layout
        self.selectAccountLayout.addWidget(self.comboBox)

        mainWindow.setCentralWidget(self.central_widget)

        # INFO:Creates the menu bar

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

        # INFO:Menu Bar ends

        self.translate_Ui(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        # INFO:Adds the add account window to main window

        self.addAccountDialog = QtWidgets.QDialog()
        self.ui = Ui_addAccountDialog()
        self.ui.setupUi(self.addAccountDialog)

        # INFO: Adds the add app window to main window
        self.addAppDialog = QtWidgets.QDialog()
        self.ui_addApp = Ui_AddAnApp()
        self.ui_addApp.setupUi(self.addAppDialog)
        self.ui_addApp.addApp.clicked.connect(self.addAppToAccount)

        # INFO: Adds the remove app window to main window
        self.removeAppDialog = QtWidgets.QDialog()
        self.ui_removeApp = UiRemoveAppDialog(self.removeAppDialog)
        self.ui_removeApp.pushButton.clicked.connect(self.removeTheAppReally)

    # INFO:Method that retrieves all accounts from DB and place them in the combo box
    def populateCombo(self):
        self.comboBox.clear()
        accounts = database.fetch_data('accounts')
        for account in accounts:
            self.comboBox.addItem(account[0])
        if len(accounts) > 0:
            self.statusLabel.setText(f"Fetched {len(accounts)} account(s) successfully!")
            self.username = self.comboBox.currentText()
        else:
            self.statusLabel.setText("No account to fetch!")
            self.statusLabel.animation.start()

    # INFO:Method that fetches the password for selected account
    def select_account_name(self):
        self.username = self.comboBox.currentText()
        accountInfo = database.fetch_account_password(self.username)
        if accountInfo is not None:
            self.username = accountInfo[0]
            self.pass_word = accountInfo[1]
        else:
            self.username = ''
            self.pass_word = ''

        print(self.username, self.pass_word)

    # INFO:Method to open the Add account window
    def receive_account_method_return(self):
        result = self.ui.add_account_clicked()
        if result == 0:
            self.statusLabel.setText("Account added successfully!")
        elif result == -1:
            self.statusLabel.setText("Couldn't add duplicate account!")
        else:
            self.statusLabel.setText("Some problem occurred while adding the account!")

    def openAddAccount(self):
        try:
            self.ui.pushButton.clicked.connect(self.receive_account_method_return)
            self.populateCombo()
        except Exception as err:
            print(err)
        self.addAccountDialog.show()

    # INFO: Method to DELETE current selected account
    def DeleteCurrentAccountFunc(self):
        currentAccount = self.comboBox.currentText()
        currentAccountIndex = self.comboBox.currentIndex()

        if not self.isUserSelected():
            return 0
        else:
            newWindow = QtWidgets.QWidget()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            newWindow.setWindowIcon(icon)
            newWindow.setGeometry(200, 200, 340, 200)
            choice = QMessageBox.question(newWindow, 'Confirm Deletion', f"Do you want to delete '{currentAccount}'?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

            if choice == QMessageBox.Yes:
                database.delete_data_from_accounts(currentAccount)
                self.comboBox.removeItem(currentAccountIndex)
                self.statusLabel.setText(f'Account "{currentAccount}" Deleted Successfully!')
            else:
                self.statusLabel.setText(f'Account "{currentAccount}" was not deleted!')

    # INFO: Method to add the app in DB manually with selected account/username
    def addAppToAccount(self):
        app_name = self.ui_addApp.appNameLineEdit.text()
        print(app_name)
        if app_name == "":
            return "Invalid app name!"
        result = database.insert_data('apps', [(app_name, self.username)])
        print(result)
        if result == 0:
            self.statusLabel.setText("App added successfully!")
        elif result == 1:
            self.statusLabel.setText("Duplicate app name found!")
        else:
            self.statusLabel.setText("Some problem occurred while adding the app!")
        self.addAppDialog.close()

    # INFO: Method to connect  manually add an app button to open the addApp window
    def manuallyAddAnAppFunc(self):
        if not self.isUserSelected():
            return 0
        self.ui_addApp.appNameLineEdit.setText('')
        self.addAppDialog.show()

    # Info: Method to remove app from account
    def removeTheAppReally(self):
        app_name = self.ui_removeApp.appComboBox.currentText()
        result_ok = database.delete_data_from_apps(self.username, app_name)
        if result_ok:
            self.statusLabel.setText(f'Successfully removed "{app_name}" form "{self.username}" account!')
        else:
            self.statusLabel.setText(f'Some problem occurred while removing "{app_name}"!')
        self.populate_removeAppDialog_comboBox()

    # Info: method to populate the combobox of the remove app dialog
    def populate_removeAppDialog_comboBox(self):
        self.ui_removeApp.appComboBox.clear()
        apps = database.fetch_all_apps(self.username)
        if len(apps) > 0:
            self.statusLabel.setText(f"Total '{len(apps)}' apps found for '{self.username}'!")
            for app_ in apps:
                self.ui_removeApp.appComboBox.addItem(app_[0])

    # INFO: Connect remove app button of main window to removeAppDialog
    def removeAnAppFunc(self):
        if not self.isUserSelected():
            return 0
        self.populate_removeAppDialog_comboBox()
        self.removeAppDialog.show()

    # INFO: Method to check if user is selected
    def isUserSelected(self):
        if self.username.lower() == "Select an account".lower() or self.username.lower() == '':
            self.statusLabel.setText("Select an account to proceed!")
            self.statusLabel.animation.start()
            return False
        return True

    # INFO:Automatically get all the app list from selected account
    def getAppListOfCurrentAccountFunc(self):
        if self.isUserSelected():
            self.statusLabel.setText(f"Getting app list of '{self.username}' account!")
            self.statusLabel.animation.start()

    # INFO: Open the app list from selected account
    def openAppListOfCurrentAccountFunc(self):
        if self.isUserSelected():
            self.statusLabel.setText(f"Opening the app list for '{self.username}' account!")
            self.statusLabel.animation.start()

    # INFO:Close window when Exit or ALT+F4 clicked
    def close_window(self):
        self.statusLabel.setText("Exited the app!")
        exit(0)

    # INFO: Show about dialog on click of ALT+A or About
    def about_dialog(self):
        self.statusLabel.setText("Shown About of the app!")
        self.statusLabel.animation.start()
        newWindow = QtWidgets.QWidget()
        newWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        newWindow.setGeometry(200, 200, 340, 200)
        QMessageBox.about(newWindow, "About bdapps content uploader ", "Version: 1.0\nDeveloper: SM Tamim Mahmud!")

    def translate_Ui(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "BDApps Content Uploader"))
        self.addNewAccount.setText(_translate("mainWindow", "Add New Account"))
        self.editCurrentAccount.setText(_translate("mainWindow", "Delete Current Account"))
        self.getAppListOfCurrentAccount.setText(_translate("mainWindow", "Get App List"))
        self.openAppListOfCurrentAccount.setText(_translate("mainWindow", "Open App List"))
        self.manuallyAddAnApp.setText(_translate("mainWindow", "Manually Add An App"))
        self.removeAnApp.setText(_translate("mainWindow", "Remove App"))
        self.status.setText(_translate("mainWindow", "STATUS:"))
        self.statusLabel.setText(_translate("mainWindow", ""))
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
    