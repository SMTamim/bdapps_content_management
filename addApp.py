
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddAnApp(object):
    def setupUi(self, AddAnApp):
        AddAnApp.setObjectName("AddAnApp")
        AddAnApp.setWindowModality(QtCore.Qt.ApplicationModal)
        AddAnApp.resize(322, 220)
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(14)
        font.setItalic(True)
        AddAnApp.setFont(font)
        AddAnApp.setModal(True)
        self.widget = QtWidgets.QWidget(AddAnApp)
        self.widget.setGeometry(QtCore.QRect(20, 40, 275, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.appNameLabel = QtWidgets.QLabel(self.widget)
        self.appNameLabel.setObjectName("appNameLabel")
        self.horizontalLayout.addWidget(self.appNameLabel)
        self.appNameLineEdit = QtWidgets.QLineEdit(self.widget)
        self.appNameLineEdit.setObjectName("appNameLineEdit")
        self.horizontalLayout.addWidget(self.appNameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.addApp = QtWidgets.QPushButton(self.widget)
        self.addApp.setObjectName("addApp")
        self.verticalLayout.addWidget(self.addApp)

        self.retranslateUi(AddAnApp)
        QtCore.QMetaObject.connectSlotsByName(AddAnApp)

    def retranslateUi(self, AddAnApp):
        _translate = QtCore.QCoreApplication.translate
        AddAnApp.setWindowTitle(_translate("AddAnApp", "Add an app"))
        self.appNameLabel.setText(_translate("AddAnApp", "App Name: "))
        self.addApp.setText(_translate("AddAnApp", "Add App"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddAnApp = QtWidgets.QDialog()
    ui = Ui_AddAnApp()
    ui.setupUi(AddAnApp)
    AddAnApp.show()
    sys.exit(app.exec_())
