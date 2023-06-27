import sys
import subprocess
import json
import requests
import ctypes
import psutil
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("alquimy")
        self.layout = QVBoxLayout()
        self.setGeometry(100, 100, 500, 50)

        ###############################--TİMERS--################################
    
        self.alquimyRemainingSecondsTimer = QTimer()
        self.alquimyRemainingSecondsTimer.timeout.connect(self.updateAlquimyTimer)

        self.closeClientRemainingSecondsTimer = QTimer()
        self.closeClientRemainingSecondsTimer.timeout.connect(self.updateCloseClientTimer)

        self.timerAlquimy = QTimer()
        self.timerAlquimy.timeout.connect(self.runAlquimy)

        self.timerCloseClient = QTimer()
        self.timerCloseClient.timeout.connect(self.runCloseClient)

        self.timerCheckLogs = QTimer()
        self.timerCheckLogs.timeout.connect(self.runCheckLogsControl)

        ###############################--BUTTONS--###############################

        self.alquimyStartButton = QPushButton("Auto Start", self)
        self.alquimyStartButton.clicked.connect(self.startAlquimy)

        self.alquimyMinutes = QLineEdit(self)
        self.alquimyMinutes.setPlaceholderText("Enter minutes")

        self.alquimyStopButton = QPushButton("Stop", self)
        self.alquimyStopButton.clicked.connect(self.stopAlquimy)

        self.closeClientStartButton = QPushButton("Close Client", self)
        self.closeClientStartButton.clicked.connect(self.startCloseClient)

        self.closeClientMinutes = QLineEdit(self)
        self.closeClientMinutes.setPlaceholderText("Enter minutes")

        self.closeClientStopButton = QPushButton("Stop", self)
        self.closeClientStopButton.clicked.connect(self.stopCloseClient)

        self.shuffleCharacterStartButton = QPushButton("Shuffle Characters", self)
        self.shuffleCharacterStartButton.clicked.connect(self.startShuffleCharacters)

        self.eventRandomSetupStartButton = QPushButton("Event Random Setup", self)
        self.eventRandomSetupStartButton.clicked.connect(self.startEventRandomSetup)

        self.checkLogsStartButton = QPushButton("Check Logs", self)
        self.checkLogsStartButton.clicked.connect(self.startCheckLogs)
        
        self.corNamesStartButton = QPushButton("Cor Names", self)
        self.corNamesStartButton.clicked.connect(self.startCorNames)

        ###############################--LAYOUTS--###############################

        alquimyButtonLayout = QHBoxLayout()
        alquimyButtonLayout.addWidget(self.alquimyStartButton)
        alquimyButtonLayout.addWidget(self.alquimyMinutes)
        alquimyButtonLayout.addWidget(self.alquimyStopButton)

        closeClientLayout = QHBoxLayout()
        closeClientLayout.addWidget(self.closeClientStartButton)
        closeClientLayout.addWidget(self.closeClientMinutes)
        closeClientLayout.addWidget(self.closeClientStopButton)

        otherProgramsLayout = QHBoxLayout()
        otherProgramsLayout.addWidget(self.shuffleCharacterStartButton)
        otherProgramsLayout.addWidget(self.eventRandomSetupStartButton)
        otherProgramsLayout.addWidget(self.checkLogsStartButton)
        otherProgramsLayout.addWidget(self.corNamesStartButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(alquimyButtonLayout)
        mainLayout.addLayout(closeClientLayout)
        mainLayout.addLayout(otherProgramsLayout)

        ##########################################################################

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.alquimyStopButton.setDisabled(True)
        self.closeClientStopButton.setDisabled(True)

        ###########################################################################

    def updateAlquimyTimer(self):
        minutes = self.alquimyRemainingSecondsTemp // 60
        seconds = self.alquimyRemainingSecondsTemp % 60

        self.alquimyStartButton.setText(f"Auto Start ({minutes:02d}:{seconds:02d})")

        if self.alquimyRemainingSecondsTemp == 0:
            self.alquimyRemainingSecondsTemp = self.alquimyRemainingSeconds
        else:
            self.alquimyRemainingSecondsTemp -= 1

    def updateCloseClientTimer(self):
        minutes = self.closeClientRemainingSecondsTemp // 60
        seconds = self.closeClientRemainingSecondsTemp % 60

        self.closeClientStartButton.setText(f"Close Client ({minutes:02d}:{seconds:02d})")

        if self.closeClientRemainingSecondsTemp == 0:
            self.closeClientRemainingSecondsTemp = self.closeClientRemainingSeconds
        else:
            self.closeClientRemainingSecondsTemp -= 1

    def startAlquimy(self):
        self.minutesText = self.alquimyMinutes.text()
        if self.minutesText.isdigit():
            minutes = int(self.minutesText)
            if minutes > 0:
                self.alquimyStartButton.setDisabled(True)
                self.alquimyStopButton.setEnabled(True)
                self.alquimyMinutes.setText(f'{self.minutesText} minute repeat')
                self.alquimyMinutes.setDisabled(True)
                self.alquimyStartButton.setStyleSheet("color: green;")
                self.startTimerAlquimy(minutes)
                self.runAlquimy()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer value for minutes.")

    def stopAlquimy(self):
        self.stopTimerAlquimy()
        self.alquimyStartButton.setEnabled(True)
        self.alquimyStopButton.setDisabled(True)
        self.alquimyMinutes.setText(f'{self.minutesText}')
        self.alquimyMinutes.setEnabled(True)
        self.alquimyStartButton.setText(f"Auto Start")
        self.alquimyStartButton.setStyleSheet("")

    def startCloseClient(self):
        self.minutesText = self.closeClientMinutes.text()
        if self.minutesText.isdigit():
            minutes = int(self.minutesText)
            if minutes > 0:
                self.closeClientStartButton.setDisabled(True)
                self.closeClientStopButton.setEnabled(True)
                self.closeClientMinutes.setText(f'{self.minutesText} minute repeat')
                self.closeClientMinutes.setDisabled(True)
                self.closeClientStartButton.setStyleSheet("color: green;")
                self.startTimerCloseClient(minutes)
                self.runCloseClient()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer value for minutes.")

    def stopCloseClient(self):
        self.stopTimerCloseClient()
        self.closeClientStartButton.setEnabled(True)
        self.closeClientStopButton.setDisabled(True)
        self.closeClientMinutes.setText(f'{self.minutesText}')
        self.closeClientMinutes.setEnabled(True)
        self.closeClientStartButton.setText(f"Close Client")
        self.closeClientStartButton.setStyleSheet("")

    def startShuffleCharacters(self):
        self.runShuffleCharacters()

    def startEventRandomSetup(self):
        self.runEventRandomSetup()
    
    def startCheckLogs(self):
        self.checkLogsStartButton.setDisabled(True)
        self.checkLogsStartButton.setText('Check Logs (Running)')
        self.checkLogsStartButton.setStyleSheet("color: green;")
        self.runStartCheckLogs()
        QTimer.singleShot(10000, lambda: self.startTimerCheckLogs(3000))

    def startCorNames(self):
        self.runCorNames()

    def stopCheckLogs(self):
        self.stopTimerCheckLogs()
        self.checkLogsStartButton.setEnabled(True)
        self.checkLogsStartButton.setText('Check Logs')
        self.checkLogsStartButton.setStyleSheet("")

    def startTimerAlquimy(self, minutes):
        self.timerAlquimy.start(minutes * 60 * 1000)
        self.alquimyRemainingSeconds = minutes * 60
        self.alquimyRemainingSecondsTemp = minutes * 60
        self.alquimyRemainingSecondsTimer.start(1000)

    def stopTimerAlquimy(self):
        self.timerAlquimy.stop()
        self.alquimyRemainingSecondsTimer.stop()

    def startTimerCloseClient(self, minutes):
        self.timerCloseClient.start(minutes * 60 * 1000)
        self.closeClientRemainingSeconds = minutes * 60
        self.closeClientRemainingSecondsTemp = minutes * 60
        self.closeClientRemainingSecondsTimer.start(1000)

    def stopTimerCloseClient(self):
        self.timerCloseClient.stop()
        self.closeClientRemainingSecondsTimer.stop()

    def startTimerCheckLogs(self, ms):
        self.timerCheckLogs.start(ms)

    def stopTimerCheckLogs(self):
        self.timerCheckLogs.stop()

    def runAlquimy(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["alquimyAutoStart.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "alquimyAutoStart.exe", None, None, 1)

    def runCloseClient(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["closeClient.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "closeClient.exe", None, None, 1)

    def runShuffleCharacters(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["shuffleCharacters.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "shuffleCharacters.exe", None, None, 1)

    def runEventRandomSetup(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["randomSetupEvent.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "randomSetupEvent.exe", None, None, 1)
    
    def runStartCheckLogs(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["checkLogs.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "checkLogs.exe", None, None, 1)

    def runCorNames(self):
        shell = ctypes.windll.shell32.IsUserAnAdmin()
        if shell:
            subprocess.Popen(["corNames.exe"], shell=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "corNames.exe", None, None, 1)

    def runCheckLogsControl(self):
        allProcesses = psutil.process_iter(attrs=['pid', 'name', 'create_time', 'memory_info'])

        runStatus = 0

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'checkLogs.exe'.lower():
                try:
                    runStatus = 1
                except psutil.NoSuchProcess:
                    pass
        if runStatus == 0:
            self.stopCheckLogs()

    def closeEvent(self, event):
        allProcesses = psutil.process_iter(attrs=['pid', 'name', 'create_time', 'memory_info'])

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'checkLogs.exe'.lower():
                processPid = process.info['pid']
                try:
                    psutil.Process(processPid).terminate()
                except psutil.NoSuchProcess:
                    pass
        super().closeEvent(event)

if __name__ == "__main__":
    headers = {'Content-type': 'application/json'}

    data = {
        'username': 'xxxxx',
        'password': 'xxxxx',
        'version': '1.0'
    }

    jsonData = json.dumps(data)
    response = requests.post('http://xxx.xxx.xxx.xxx:2424/login', data=jsonData, headers=headers, timeout = 10).json()
    if response['status'] == 200:
        app = QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        app = QApplication([])
        QMessageBox.warning(None, "Server error", "Server error.")
        sys.exit()
