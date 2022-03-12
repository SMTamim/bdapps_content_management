import os
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from revenue_report import LoadingScreenThreadCredential
from uploadContent import raiseException


class Ui_addAccountDialog(object):
    def __init__(self):
        self.result = ''

    def setupUi(self, addAccountDialog):
        addAccountDialog.setObjectName("addAccountDialog")
        addAccountDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        addAccountDialog.resize(390, 304)
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(11)
        addAccountDialog.setFont(font)
        addAccountDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        addAccountDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        addAccountDialog.setModal(True)
        self.horizontalLayoutWidget = QtWidgets.QWidget(addAccountDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 341, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.accountNameLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.accountNameLayout.setContentsMargins(0, 0, 0, 0)
        self.accountNameLayout.setObjectName("accountNameLayout")

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(addAccountDialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 10, 341, 80))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.infoOfAccAddLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.infoOfAccAddLayout.setObjectName("infoOfAccAddLayout")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/addAccount.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addAccountDialog.setWindowIcon(icon)

        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(11)
        self.infoOfAccAdd = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.infoOfAccAdd.setFont(font)
        self.infoOfAccAdd.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.infoOfAccAdd.setObjectName("infoOfAccAdd")
        self.infoOfAccAddLayout.addWidget(self.infoOfAccAdd)

        self.accountName = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.accountName.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.accountName.setObjectName("accountName")
        self.accountNameLayout.addWidget(self.accountName)
        self.accountNameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.accountNameLineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.accountNameLineEdit.setToolTipDuration(3)
        self.accountNameLineEdit.setObjectName("accountNameLineEdit")
        self.accountNameLayout.addWidget(self.accountNameLineEdit)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(addAccountDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 130, 341, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.passwordLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.passwordLayout.setContentsMargins(0, 0, 0, 0)
        self.passwordLayout.setObjectName("passwordLayout")
        self.accountPassword = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.accountPassword.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.accountPassword.setObjectName("accountPassword")
        self.passwordLayout.addWidget(self.accountPassword)
        self.accountPasswordLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.accountPasswordLineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.accountPasswordLineEdit.setToolTipDuration(3)
        self.accountPasswordLineEdit.setObjectName("accountPasswordLineEdit")
        self.passwordLayout.addWidget(self.accountPasswordLineEdit)
        self.verticalLayoutWidget = QtWidgets.QWidget(addAccountDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 220, 160, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pushButton.setToolTipDuration(3)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_account_clicked)
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(addAccountDialog)
        QtCore.QMetaObject.connectSlotsByName(addAccountDialog)

    def retranslateUi(self, addAccountDialog):
        _translate = QtCore.QCoreApplication.translate
        addAccountDialog.setWindowTitle(_translate("addAccountDialog", "Add/Delete Account"))
        self.accountName.setText(_translate("addAccountDialog", "Account Name:"))
        self.infoOfAccAdd.setText(_translate("addAccountDialog", ""))
        self.accountNameLineEdit.setToolTip(_translate("addAccountDialog", "Enter Account Name"))
        self.accountPassword.setText(_translate("addAccountDialog", "Password:         "))
        self.accountPasswordLineEdit.setToolTip(_translate("addAccountDialog", "Enter account password"))
        self.pushButton.setToolTip(_translate("addAccountDialog", "Click this button to add this account to the app."))
        self.pushButton.setText(_translate("addAccountDialog", "Add this account"))

    # INFO: Method to add new account in accounts.db.
    def add_account_clicked(self):
        self.acc_name = self.accountNameLineEdit.text().lower().strip()
        self.acc_pass = self.accountPasswordLineEdit.text().strip()
        self.infoOfAccAdd.setStyleSheet('color:red')

        if self.acc_pass != '' and self.acc_name != '':
            self.new_dialog = QtWidgets.QDialog()
            try:
                font = QtGui.QFont()
                font.setFamily("Calibri")
                font.setPointSize(14)

                self.new_dialog.setWindowTitle("Checking Credential")
                self.new_dialog.setWindowIcon(QtGui.QIcon('icon.png'))
                self.new_dialog.setFixedSize(400, 250)
                self.new_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
                self.new_dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                self.new_dialog.setFont(font)
                self.new_dialog.animation = QtGui.QMovie(os.path.join(os.path.abspath(os.getcwd()), 'resources', 'loading.gif'))
                self.new_dialog.title = QtWidgets.QLabel("Checking if credentials are valid!")
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
                self.thread = LoadingScreenThreadCredential(self.acc_name, self.acc_pass)
                self.thread.start()
                self.thread.stop_signal.connect(self.runFunction)
                self.thread.check_signal.connect(self.check_credentials)
            except Exception as e:
                raiseException(e)
        else:
            self.result = -1

    def runFunction(self, stop_run):
        if stop_run:
            self.thread.stop()
            self.new_dialog.animation.stop()
            self.new_dialog.close()
        else:
            self.new_dialog.animation.start()
            self.new_dialog.show()

    def check_credentials(self, is_credential_ok):
        if is_credential_ok:
            list_data = [(self.acc_name, self.acc_pass)]
            from main import database
            print(list_data)
            is_ok = database.insert_data('accounts', list_data)
            self.result = is_ok
            if is_ok == 0:
                self.infoOfAccAdd.setText(f"Account successfully added.")
                self.infoOfAccAdd.setStyleSheet('color:green')
                self.accountNameLineEdit.setText('')
                self.accountPasswordLineEdit.setText('')

            elif is_ok == 1:
                self.infoOfAccAdd.setText(f"Duplicate Account Name Found!.")
                self.infoOfAccAdd.setStyleSheet('color:red')
                self.accountNameLineEdit.setText('')
                self.accountPasswordLineEdit.setText('')
        else:
            self.infoOfAccAdd.setText(f"Invalid Username or Password!.")
            self.infoOfAccAdd.setStyleSheet('color:red')
            self.accountPasswordLineEdit.setText('')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addAccountDialog = QtWidgets.QDialog()
    ui = Ui_addAccountDialog()
    ui.setupUi(addAccountDialog)
    addAccountDialog.show()
    sys.exit(app.exec_())
