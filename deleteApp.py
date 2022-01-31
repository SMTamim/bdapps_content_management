from PyQt5 import QtCore, QtGui, QtWidgets


class UiRemoveAppDialog(object):
    def __init__(self, removeAppDialog):
        removeAppDialog.setObjectName("removeAppDialog")
        removeAppDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        removeAppDialog.setFixedSize(352, 280)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        removeAppDialog.setFont(font)
        removeAppDialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        removeAppDialog.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(removeAppDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 40, 331, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(removeAppDialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(19, 99, 321, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.appComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.appComboBox.setObjectName("appComboBox")
        self.verticalLayout_2.addWidget(self.appComboBox)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(30, 25))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)

        self.translateUi(removeAppDialog)
        QtCore.QMetaObject.connectSlotsByName(removeAppDialog)

    def translateUi(self, removeAppDialog):
        _translate = QtCore.QCoreApplication.translate
        removeAppDialog.setWindowTitle(_translate("removeAppDialog", "Remove App"))
        self.label.setText(_translate("removeAppDialog", "Select an app to remove from account \'"))
        self.pushButton.setText(_translate("removeAppDialog", "Delete App"))


import resources


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    removeAppDialog_ = QtWidgets.QDialog()
    ui = UiRemoveAppDialog(removeAppDialog_)
    removeAppDialog_.show()
    sys.exit(app.exec_())
