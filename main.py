import os
from PyQt5.QtWidgets import QAction, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from db import DB
from addAcc import Ui_addAccountDialog
from addApp import Ui_AddAnApp
from deleteApp import UiRemoveAppDialog
from revenue_report import MainApp
from uploadContent import UploadWindow, raiseException, RefreshTableThread, UploadThread
import resources
import time

database = DB()
username_global = ''
password_global = ''
status_text_global = ''


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    got_all_app_signal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.isRunning = True
        self.isPaused = False
        self.isDone = False

    def run(self):
        print("Starting thread", self.index)
        user = UploadWindow(username_global, password_global)

        for i in range(1, 20):
            self.any_signal.emit(int(i))
            time.sleep(.1)

        json_data = dict(user.get_user_app_name())
        terminated = 0
        progress = 20
        got_all_apps = False
        try:
            apps = json_data.get('result').get('results')
            database_ = DB()
            for app in apps:
                if app['appStatus'] != 'terminate':
                    app_name = app['appName']
                    app_type = app['appType']
                    if app_type == "soltura":
                        app_type = "Lite"
                    elif app_type == "sdp":
                        app_type = "Pro"
                    else:
                        app_type = 'Lite Videos'
                    user_name = app['spName']
                    app_link = ''
                    app = (app_name, app_type, app_link, user_name, '0', '0')
                    print(f"Inserting {app}")
                    result = database_.insert_data('apps', [app])
                    print(result)
                    progress += (90/len(apps))
                    for n in range(0, 10):
                        self.any_signal.emit(int(progress))
                        time.sleep(.05)
                else:
                    terminated += 1
                self.isDone = True

            does_all_app_has_link = user.get_content_add_link()

            apps = database.fetch_all_apps(username_global)
            self.any_signal.emit(100)

            if not does_all_app_has_link:
                self.got_all_app_signal.emit(apps)

        except Exception as e:
            print("Some problem occurred!", e)
            self.any_signal.emit(0)

    def pause(self):
        self.isPaused = True

    def resume(self):
        self.isPaused = False

    def stop(self):
        self.isRunning = False
        print("Stopping Thread", self.index)
        self.terminate()


class AppListWindow(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('App List')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(200, 200, 500, 500)
        font = QtGui.QFont('Calibri')
        font.setPointSize(15)
        self.setFont(font)


class WidgetWindow(QtWidgets.QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(200, 200, 440, 500)
        font = QtGui.QFont('Calibri')
        font.setPointSize(15)
        self.setFont(font)


class LoadingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Getting Apps')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(200, 200, 500, 100)
        self.setFixedSize(500, 100)

        # info: For Centering the window
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        font = QtGui.QFont('Calibri')
        font.setPointSize(15)
        self.setFont(font)
        hBox = QtWidgets.QHBoxLayout()
        self.progressBar = QtWidgets.QProgressBar()
        hBox.addWidget(self.progressBar)
        self.setLayout(hBox)


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
        self.thread = {}
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
        self.addNewAccount.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/addAccount.png")))
        self.addNewAccount.clicked.connect(self.openAddAccount)
        self.addNewAccount.setFont(font)
        self.addNewAccount.setObjectName("addNewAccount")
        buttonsLayout_hBox.addWidget(self.addNewAccount)

        # INFO:Create Edit Current Account Button

        self.deleteCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.deleteCurrentAccount.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/delete.png")))
        self.deleteCurrentAccount.setObjectName("deleteCurrentAccount")
        self.deleteCurrentAccount.setFont(font)
        self.deleteCurrentAccount.clicked.connect(self.DeleteCurrentAccountFunc)
        buttonsLayout_hBox.addWidget(self.deleteCurrentAccount)

        self.buttonsLayout.addLayout(buttonsLayout_hBox)

        buttonsLayout_hBox2 = QtWidgets.QHBoxLayout()
        # INFO:Create Get App List Button

        self.getAppListOfCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.getAppListOfCurrentAccount.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/download.png")))
        self.getAppListOfCurrentAccount.setFont(font)
        self.getAppListOfCurrentAccount.setObjectName("getAppListOfCurrentAccount")
        self.getAppListOfCurrentAccount.clicked.connect(self.getAppListOfCurrentAccountFunc)
        buttonsLayout_hBox2.addWidget(self.getAppListOfCurrentAccount)

        # INFO:Create Open App List Button

        self.openAppListOfCurrentAccount = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.openAppListOfCurrentAccount.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/list.png")))
        self.openAppListOfCurrentAccount.setFont(font)
        self.openAppListOfCurrentAccount.setObjectName("openAppListOfCurrentAccount")
        self.openAppListOfCurrentAccount.clicked.connect(self.openAppListOfCurrentAccountFunc)
        buttonsLayout_hBox2.addWidget(self.openAppListOfCurrentAccount)

        # INFO:Create Manually add an app button

        self.manuallyAddAnApp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.manuallyAddAnApp.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/add.png")))
        self.manuallyAddAnApp.setFont(font)
        self.manuallyAddAnApp.setObjectName("manuallyAddAnApp")
        self.manuallyAddAnApp.clicked.connect(self.manuallyAddAnAppFunc)
        buttonsLayout_hBox2.addWidget(self.manuallyAddAnApp)

        self.buttonsLayout.addLayout(buttonsLayout_hBox2)

        buttonsLayout_hBox3 = QtWidgets.QHBoxLayout()
        # INFO: Adds the Remove an app button

        self.removeAnApp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.removeAnApp.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/remove.png")))
        self.removeAnApp.setFont(font)
        self.removeAnApp.setObjectName("removeAnApp")
        self.removeAnApp.clicked.connect(self.removeAnAppFunc)
        buttonsLayout_hBox3.addWidget(self.removeAnApp)

        # Info: Revenue Report Button
        self.revenueReport = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.revenueReport.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/report.png")))
        self.revenueReport.setFont(font)
        self.revenueReport.setObjectName("revenueReport")
        self.revenueReport.clicked.connect(self.revenueReportFunc)
        buttonsLayout_hBox3.addWidget(self.revenueReport)

        # Info: Open Upload Window Button
        self.uploadWindow = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.uploadWindow.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/upload.png")))
        self.uploadWindow.setFont(font)
        self.uploadWindow.setObjectName("uploadWindow")
        self.uploadWindow.clicked.connect(self.uploadWindowFunc)
        buttonsLayout_hBox3.addWidget(self.uploadWindow)

        self.buttonsLayout.addLayout(buttonsLayout_hBox3)

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
        self.ui_addAcc = Ui_addAccountDialog()
        self.ui_addAcc.setupUi(self.addAccountDialog)

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
            global username_global
            username_global = self.username
        else:
            self.statusLabel.setText("No account to fetch!")
            self.statusLabel.animation.start()

    # INFO:Method that fetches the password for selected account
    def select_account_name(self):
        self.username = self.comboBox.currentText()
        accountInfo = database.fetch_account_password(self.username)
        global username_global, password_global
        if accountInfo is not None:
            self.username = accountInfo[0]
            username_global = self.username
            self.pass_word = accountInfo[1]
            password_global = self.pass_word
        else:
            self.username = ''
            self.pass_word = ''
            username_global = ''
            password_global = ''

        print(self.username, self.pass_word)

    # INFO:Method to open the Add account window
    def openAddAccount(self):
        self.addAccountDialog.show()
        try:
            self.populateCombo()
        except Exception as err:
            print(err)

    # INFO: Method to DELETE current selected account
    def DeleteCurrentAccountFunc(self):
        currentAccount = self.comboBox.currentText()
        currentAccountIndex = self.comboBox.currentIndex()

        if not self.isUserSelected():
            return 0
        else:
            self.confirmDeleteWindow = QtWidgets.QWidget()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.confirmDeleteWindow.setWindowIcon(icon)
            self.confirmDeleteWindow.setGeometry(200, 200, 400, 300)
            font = QtGui.QFont()
            font.setFamily('Calibri')
            font.setPointSize(15)
            self.confirmDeleteWindow.setFont(font)

            # Centering the window
            qr = self.confirmDeleteWindow.frameGeometry()
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.confirmDeleteWindow.move(qr.topLeft())

            choice = QMessageBox.question(self.confirmDeleteWindow, 'Confirm Deletion', f"Do you want to delete '{currentAccount}'?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

            if choice == QMessageBox.Yes:
                database.delete_data_from_accounts(currentAccount)
                database.delete_all_apps(currentAccount)
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
        result = database.insert_data('apps', [(app_name, "", "", self.username)])
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

    # info: Revenue Report Function
    def revenueReportFunc(self):
        if not self.isUserSelected():
            return
        self.reportWindow = MainApp(self.username, self.pass_word)
        self.reportWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.reportWindow.show()

    # # Info: Generate Excel Function
    # def generateExcelFunc(self):
    #     try:
    #         if not self.isUserSelected():
    #             return 0
    #         apps = database.fetch_all_apps(self.username)
    #         try:
    #             os.chdir('files')
    #         except FileNotFoundError:
    #             os.mkdir('files')
    #             os.chdir('files')
    #         wb = xlsxwriter.Workbook(self.username + '.xlsx')
    #         for app in apps:
    #             ds = wb.add_worksheet(app[0])
    #             ds.write(0, 0, 'end')
    #         wb.close()
    #         os.chdir('..')
    #         self.statusLabel.setText(f'Successfully generated Excel for "{self.username}"!')
    #         self.statusLabel.animation.start()
    #     except Exception as e:
    #         print(e)
    #
    # Info: Open Upload Window
    def uploadWindowFunc(self):
        if not self.isUserSelected():
            return 0
        else:
            try:
                self.upload_window = UploadWindow(self.username, self.pass_word)
                self.upload_window.setWindowModality(QtCore.Qt.ApplicationModal)

                qr = self.upload_window.frameGeometry()
                cp = QtWidgets.QDesktopWidget().availableGeometry().center()
                qr.moveCenter(cp)
                self.upload_window.move(qr.topLeft())
                self.upload_window.show()

            except Exception as e:
                raiseException(e)

    # INFO: Method to check if user is selected
    def isUserSelected(self):
        if self.username.lower() == "Select an account".lower() or self.username.lower() == '':
            self.statusLabel.setText("Select an account to proceed!")
            self.statusLabel.animation.start()
            return False
        return True

    def myFunction(self, counter):
        try:
            cnt = counter
            index = self.thread[1].sender().index
            if index == 1:
                if cnt == 100:
                    self.thread[1].stop()
                    self.loadingWindow.progressBar.setValue(cnt)
                    self.loadingWindow.close()
                    self.statusLabel.resize(self.statusLabel.width(), 50)
                    self.statusLabel.setText(f"Got all apps for '{self.username}' from BDApps!")
                    self.statusLabel.animation.start()

                elif cnt == 0:
                    self.loadingWindow.close()
                    self.thread[1].stop()
                else:
                    self.loadingWindow.progressBar.setValue(cnt)
        except Exception as e:
            print(e)

    # INFO:Automatically get all the app list from selected account
    def getAppListOfCurrentAccountFunc(self):
        if self.isUserSelected():
            try:
                self.loadingWindow = LoadingWindow()
                self.loadingWindow.setWindowModality(QtCore.Qt.ApplicationModal)
                self.loadingWindow.show()

                self.thread[1] = ThreadClass(parent=None, index=1)
                self.thread[1].start()
                self.thread[1].any_signal.connect(self.myFunction)
                self.thread[1].got_all_app_signal.connect(self.refresh_app_table_method)

            except Exception as e:
                print(e)

    # INFO: Open the app list from selected account
    def openAppListOfCurrentAccountFunc(self):
        if self.isUserSelected():
            self.statusLabel.setText(f"Opening the app list for '{self.username}' account!")
            self.statusLabel.animation.start()

            apps = database.fetch_all_apps(self.username)

            self.newWindow = WidgetWindow("App Details Table")
            self.newWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            vBox = QtWidgets.QVBoxLayout()

            if len(apps) > 0:
                AppTable = QTableWidget()
                AppTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                refreshAppTableBtn = QtWidgets.QPushButton("Refresh Table")
                refreshAppTableBtn.clicked.connect(lambda: self.refresh_app_table_method(apps))
                totalSubscribers = QtWidgets.QLabel("Total Subscribers: 0")
                vBox.addWidget(refreshAppTableBtn)
                vBox.addWidget(totalSubscribers)
                vBox.addWidget(AppTable)

                self.newWindow.setStyleSheet("QTableWidget::item {border-top: 2px solid black; padding: 5px; color:black; text-align:center;}QHeaderView::section {color: black;}")
                self.newWindow.setLayout(vBox)

                AppTable.setRowCount(len(apps))
                AppTable.setColumnCount(4)
                totalSubscriberCount = 0
                AppTable.setHorizontalHeaderLabels(["App Name", "App Type", "Last Content Date", "Subscriber\ncount"])
                for i, app_ in enumerate(apps):
                    AppTable.setItem(i, 0, QTableWidgetItem(app_[0]))
                    AppTable.setItem(i, 1, QTableWidgetItem(app_[1]))
                    AppTable.setItem(i, 2, QTableWidgetItem(app_[4]))
                    AppTable.setItem(i, 3, QTableWidgetItem(app_[5]))
                    if app_[1] != "Pro":
                        try:
                            totalSubscriberCount += int(app_[5])
                        except Exception:
                            continue
                totalSubscribers.setText(f"Total Subscribers: {totalSubscriberCount}")
                totalSubscribers.setAlignment(QtCore.Qt.AlignCenter)
                totalSubscribers.setStyleSheet("color:orange; border-bottom:2px solid black;")
            else:
                self.newWindow.setWindowTitle('Get Apps from bdapps')
                self.newWindow.setFixedSize(350, 200)
                self.newWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                # Centering the window
                qr = self.newWindow.frameGeometry()
                cp = QtWidgets.QDesktopWidget().availableGeometry().center()
                qr.moveCenter(cp)
                self.newWindow.move(qr.topLeft())

                vBox.addWidget(QtWidgets.QLabel(f"No app was found in '{self.username}'"))
                vBox.addWidget(QtWidgets.QLabel("Want to get app list from BDApps?"))
                btn = QtWidgets.QPushButton("Get App List Now")
                btn.clicked.connect(self.closeAppList)
                vBox.addWidget(btn)
                self.newWindow.setLayout(vBox)

            self.newWindow.show()

    def closeAppList(self):
        self.newWindow.close()
        self.getAppListOfCurrentAccountFunc()

    def refresh_app_table_method(self, apps):
        self.new_dialog = QtWidgets.QDialog()
        try:
            font = QtGui.QFont()
            font.setFamily("Calibri")
            font.setPointSize(14)

            self.new_dialog.setWindowTitle("Refreshing Table")
            self.new_dialog.setWindowIcon(QtGui.QIcon('icon.png'))
            self.new_dialog.setFixedSize(400, 250)
            self.new_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            self.new_dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.new_dialog.setFont(font)
            self.new_dialog.animation = QtGui.QMovie(
                os.path.join(os.path.abspath(os.getcwd()), 'resources', 'loading.gif'))
            self.new_dialog.title = QtWidgets.QLabel("Wait while I'm trying to refresh the table!")
            self.new_dialog.title.setAlignment(QtCore.Qt.AlignCenter)
            self.new_dialog.label_loading = QtWidgets.QLabel(self.new_dialog)
            self.new_dialog.label_loading.setStyleSheet("border: 0px;")
            self.new_dialog.label_loading.setMovie(self.new_dialog.animation)
            vBox = QtWidgets.QVBoxLayout()
            vBox.addWidget(self.new_dialog.title)
            hBox = QtWidgets.QHBoxLayout()
            hBox.addWidget(self.new_dialog.label_loading)
            vBox.addLayout(hBox)
            self.new_dialog.setLayout(vBox)
            self.new_dialog.animation.start()
            self.refreshThread = RefreshTableThread(self.username, self.pass_word, apps)
            self.refreshThread.start()
            self.refreshThread.stop_signal.connect(self.refreshTableRunFunction)
            self.refreshThread.current_working_app_signal.connect(self.set_refresh_wait_text)
        except Exception as e:
            raiseException(e)

    def set_refresh_wait_text(self, appName):
        self.new_dialog.title.setText(f"Getting subscriber count of app '{appName}'!")

    def refreshTableRunFunction(self, stop_signal):
        print("Signal: ", stop_signal)
        if not stop_signal:
            try:
                self.newWindow.close()
            except Exception as e:
                print("Skipping closing of app table as it it now opened.")
            self.new_dialog.show()
            self.new_dialog.animation.start()
        else:
            self.refreshThread.stop()
            self.new_dialog.animation.stop()
            self.new_dialog.close()
            self.openAppListOfCurrentAccountFunc()

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

        # Centering the window
        qr = newWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        newWindow.move(qr.topLeft())
        QMessageBox.about(newWindow, "About BDApps Content Uploader! ", "Version: 1.0.1\nDeveloper: SM Tamim Mahmud!\nComputer Science Engineer")

    def translate_Ui(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "BDApps Content Uploader"))
        self.addNewAccount.setText(_translate("mainWindow", "Add New Account"))
        self.deleteCurrentAccount.setText(_translate("mainWindow", "Delete Current Account"))
        self.getAppListOfCurrentAccount.setText(_translate("mainWindow", "Get App List"))
        self.openAppListOfCurrentAccount.setText(_translate("mainWindow", "Open App List"))
        self.manuallyAddAnApp.setText(_translate("mainWindow", "Manually Add An App"))
        self.removeAnApp.setText(_translate("mainWindow", "Remove App"))
        self.revenueReport.setText(_translate("mainWindow", "Revenue Report"))
        self.uploadWindow.setText(_translate("mainWindow", "Upload Content"))
        self.status.setText(_translate("mainWindow", "STATUS:"))
        self.statusLabel.setText(_translate("mainWindow", "Select an account to proceed."))
        self.statusLabel.animation.start()
        self.welcomeText.setText(_translate("mainWindow", "Welcome to BDApps Content Uploader"))
        self.selectAccount.setText(_translate("mainWindow", "Select an account:"))
        self.comboBox.setToolTip(_translate("mainWindow",
                                            "<html><head/><body><p><span style=\" font-size:10pt;\">Select the account for which you want to upload content.</span></p></body></html>"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuAbout.setTitle(_translate("mainWindow", "About"))
        self.actionExit_2.setText(_translate("mainWindow", "Exit"))
        self.actionExit_2.setShortcut(_translate("mainWindow", "Alt+Q"))
        self.actionAbout.setText(_translate("mainWindow", "About"))
        self.actionAbout.setShortcut(_translate("mainWindow", "Alt+A"))


class MyWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


stylesheet = """
    QWidget {
        background-image:url(:/bg-image/background.png);
        background-repeat: no-repeat;
        background-position: center;
    }
    QLabel{
        background-image:none;
    }
    QHBoxLayout{
        background-image:none;
    }
    QVBoxLayout{
        background-image:none;
    }
"""

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(stylesheet)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
