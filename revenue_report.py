import sys
import time
import os
import selenium.common.exceptions
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from PyQt5.QtWidgets import QAction, QMessageBox, QListWidget
from PyQt5 import QtCore, QtGui, QtWidgets
BASE_URL = 'https://user.bdapps.com'


class RevenueReport:
    def __init__(self, username, password):
        self.driver = None
        self.username = username
        self.password = password
        self.user_name_field = "username"
        self.pass_word_field = "password"
        self.default_name = "sdp_monthly_revenue_and_traffic_report.xls"
        self.file_name = f"{self.username}.xml"
        self.is_done = False
        self.is_driver_initialized = False

        self.driver_options = options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("disable-infobars")
        options.add_argument("--disable-logging")
        options.add_argument("--silent")
        options.add_argument("--log-level=3")
        options.add_argument('--headless')

        self.path = path = os.path.join(os.path.abspath(os.getcwd()), "files", "revenue_reports")
        prefs = {"download.default_directory": path}
        options.add_experimental_option("prefs", prefs)
        
    def initialize_wd(self):
        self.driver = driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.driver_options)
        self.is_driver_initialized = True
        driver.get(BASE_URL)
    
    def enter_login_info(self):
        driver = self.driver
        while driver.title != 'Login':
            time.sleep(1)
        time.sleep(1)
        user_name = driver.find_element(By.NAME, self.user_name_field)
        user_name.clear()
        user_name.send_keys(self.username)
        pass_word = driver.find_element(By.NAME, self.pass_word_field)
        pass_word.clear()
        pass_word.send_keys(self.password)

    def click_login_btn(self):
        driver = self.driver
        login_button = "button[type='submit']"

        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, login_button))
        )
        driver.find_element(By.CSS_SELECTOR, login_button).click()
        time.sleep(1)

    def is_login_ok(self):
        self.initialize_wd()
        self.enter_login_info()
        self.click_login_btn()
        try:
            WebDriverWait(self.driver, 2).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'notification-section__body'))
            )
            self.close_wd()
            return False
        except selenium.common.exceptions.TimeoutException:
            self.driver.get("https://user.bdapps.com/cas/logout")
            self.close_wd()
            return True

    def download_report(self):
        driver = self.driver
        driver.get("https://user.bdapps.com/viewer/spring/sdpMonthlyRevenue.jsp")
        time.sleep(2)
        driver.get("https://user.bdapps.com/viewer/spring/sdpMonthlyRevenue.jsp")

        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "checkmark"))
        )
        driver.find_element(By.CLASS_NAME, "checkmark").click()
        driver.execute_script('document.querySelector("form").removeAttribute("target")')

        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[alt="submit"]'))
        )
        driver.find_element(By.CSS_SELECTOR, 'button[alt="submit"]').click()

        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[title="Export Excel Document"]'))
        )
        driver.find_element(By.CSS_SELECTOR, 'input[title="Export Excel Document"]').click()

        os.chdir(self.path)
        if self.file_name in os.listdir():
            os.remove(self.file_name)

        time.sleep(2)
        os.rename(self.default_name, self.file_name)
        os.chdir("..")
        print("Downloaded")

    def close_wd(self):
        print("\nClosing WebDriver")
        self.driver.close()
        print("WebDriver Closed\n")
        self.is_done = True
        self.is_driver_initialized = False


class GetRevenueReport(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    path_signal = QtCore.pyqtSignal(str)
    
    def __init__(self, username, password, parent=None, index=0):
        super(GetRevenueReport, self).__init__(parent)
        self.report = RevenueReport(username, password)
        self.index = index
        self.isRunning = True
        self.isPaused = False
        self.isDone = False
        self.path = ""
        
    def run(self):
        print("Starting thread", self.index)
        report = self.report
        terminated = 0
        progress = 1
        try:
            while progress <= 5:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.05)
            report.initialize_wd()
            while progress <= 20:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.05)
            report.enter_login_info()
            while progress <= 40:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.05)
            report.click_login_btn()
            while progress <= 60:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.05)
            report.download_report()
            while progress <= 85:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.01)
            while progress <= 99:
                self.any_signal.emit(progress)
                progress += 1
                time.sleep(.01)
            self.path = os.path.abspath(os.path.join(report.path, report.file_name))
            self.path_signal.emit(self.path)
            self.any_signal.emit(100)
            
        except Exception as e:
            print("Some problem occurred!", e)
            self.any_signal.emit(0)

    def pause(self):
        self.isPaused = True

    def resume(self):
        self.isPaused = False

    def stop(self):
        self.isRunning = False
        if self.report.is_driver_initialized:
            self.report.close_wd()
        print("Stopping Thread", self.index)
        self.terminate()


class LoadingScreenThreadCredential(QtCore.QThread):
    stop_signal = QtCore.pyqtSignal(bool)
    check_signal = QtCore.pyqtSignal(bool)

    def __init__(self, username, password):
        super(LoadingScreenThreadCredential, self).__init__()
        self.siteObj = RevenueReport(username, password)

    def run(self):
        self.stop_signal.emit(False)
        self.check_signal.emit(self.siteObj.is_login_ok())
        self.stop_signal.emit(True)

    def stop(self):
        self.terminate()


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self, title: str, username, password):
        try:
            super().__init__()
            self.setWindowTitle(title)
            self.setWindowIcon(QtGui.QIcon('icon.png'))
            self.setFixedSize(400, 250)
            self.setWindowModality(QtCore.Qt.ApplicationModal)
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.is_credential_ok = False
            self.animation = QtGui.QMovie(os.path.join(os.path.abspath(os.getcwd()), 'resources', 'loading.gif'))
            self.label_loading = QtWidgets.QLabel(self)
            self.label_loading.setMovie(self.animation)
            hBox = QtWidgets.QHBoxLayout()
            hBox.addWidget(self.label_loading)
            self.setLayout(hBox)
            self.thread = LoadingScreenThreadCredential(username, password)
            self.thread.start()
            self.thread.stop_signal.connect(self.runFunction)
            self.thread.check_signal.connect(self.setCredentialCheck)
        except Exception as e:
            print(e)

    def runFunction(self, stop_run):
        if stop_run:
            self.thread.stop()
            self.animation.stop()
            self.close()
        else:
            self.animation.start()
            self.show()

    def setCredentialCheck(self, check_is_ok):
        if check_is_ok:
            self.is_credential_ok = True


class MainApp(QtWidgets.QWidget):
    def __init__(self, username, password):
        QtWidgets.QWidget.__init__(self)
        self.path = None
        self.workingDirectory = os.path.abspath(os.getcwd())
        self.setWindowTitle('Getting Report')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setGeometry(200, 200, 300, 250)
        font = QtGui.QFont('Calibri')
        font.setPointSize(15)
        self.setFont(font)
        self.vBox = vBox = QtWidgets.QVBoxLayout()
        self.progressBar = QtWidgets.QProgressBar()

        self.status = QtWidgets.QLabel("Getting your revenue report!")
        self.btn = QtWidgets.QPushButton("Open Report")
        self.btn.clicked.connect(self.open_report)

        vBox.addWidget(self.status)
        vBox.addWidget(self.progressBar)

        self.setLayout(vBox)
        self.thread = GetRevenueReport(username, password, parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(self.myFunc)
        self.thread.path_signal.connect(self.getPath)

    def myFunc(self, counter):
        try:
            cnt = counter
            index = self.thread.sender().index
            if index == 1:
                if cnt == 100:
                    self.thread.stop()
                    self.progressBar.setValue(cnt)
                    self.progressBar.close()
                    self.status.setText("Hurrah! We've got your report.")
                    self.vBox.addWidget(self.btn)
                    self.vBox.addWidget(QtWidgets.QLabel(''))

                    # self.setLayout(vBox)

                elif cnt == 0:
                    self.thread.stop()
                else:
                    self.progressBar.setValue(cnt)
        except Exception as e:
            print(e)

    def getPath(self, path):
        self.path = path

    def open_report(self):
        print(self.path)
        os.startfile(self.path)

    def closeEvent(self, event):
        try:
            print("Closing WD\n")
            self.thread.stop()
            os.chdir(self.workingDirectory)
            event.accept()  # let the window close
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoadingScreen("Checking Credentials", "darkslave0", "Tamim@646")
    window.show()
    sys.exit(app.exec_())
