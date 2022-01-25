
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addAccountDialog(object):
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

    # Method to add new account in accounts.db.

    def add_account_clicked(self):
        acc_name = self.accountNameLineEdit.text()
        acc_pass = self.accountPasswordLineEdit.text()
        self.infoOfAccAdd.setStyleSheet('color:red')

        if acc_pass != '' and acc_name != '':
            list_data = [(acc_name, acc_pass)]
            from main import database

            is_ok = database.insert_data('accounts', list_data)
            if is_ok == 0:
                print(f"{acc_name} has been successfully added with given password!")
                self.infoOfAccAdd.setText(f"Account '{acc_name}' successfully added.")
                self.infoOfAccAdd.setStyleSheet('color:green')
                self.accountNameLineEdit.setText("")
                self.accountPasswordLineEdit.setText("")
                return 0
            elif is_ok == 1:
                self.infoOfAccAdd.setText("Duplicate Account Name")
                return -1
        else:
            self.infoOfAccAdd.setText("Invalid account name or password!")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addAccountDialog = QtWidgets.QDialog()
    ui = Ui_addAccountDialog()
    ui.setupUi(addAccountDialog)
    addAccountDialog.show()
    sys.exit(app.exec_())
