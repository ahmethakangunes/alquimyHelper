import sys
import json
import time
import ctypes
import psutil
import winreg
import requests
import threading
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("alquimy")
        self.layout = QVBoxLayout()
        self.setGeometry(100, 100, 500, 50)

        self.reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        ###############################--TİMERS--################################
    
        self.alquimyRemainingSecondsTimer = QTimer()
        self.alquimyRemainingSecondsTimer.timeout.connect(self.updateAlquimyTimer)

        self.closeClientRemainingSecondsTimer = QTimer()
        self.closeClientRemainingSecondsTimer.timeout.connect(self.updateCloseClientTimer)

        self.timerAlquimy = QTimer()
        self.timerAlquimy.timeout.connect(lambda: self.runExe('alquimyAutoStart.exe'))

        self.timerCloseClient = QTimer()
        self.timerCloseClient.timeout.connect(lambda: self.runExe('closeClient.exe'))

        self.timerCheckLogs = QTimer()
        self.timerCheckLogs.timeout.connect(self.runCheckLogsControl)

        ###############################--BUTTONS--###############################

        self.resetAllSlotsButton = QPushButton("RESET ALL SLOTS WORKING STATUS", self)
        self.resetAllSlotsButton.clicked.connect(lambda: self.resetAllSlotsButtonClicked(True))

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

        resetAllSlotButtonLayout = QHBoxLayout()
        resetAllSlotButtonLayout.addWidget(self.resetAllSlotsButton)

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
        mainLayout.addLayout(resetAllSlotButtonLayout)
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

    def resetAllSlotsButtonClicked(self, buttonStatus):
        if buttonStatus:
            self.resetAllSlotsButton.setDisabled(True)
            self.resetAllSlotsButton.setText("Working...")

            thread = threading.Thread(target = self.resetAllSlotStatus)
            thread.start()
        else:
            self.resetAllSlotsButton.setText("RESET ALL SLOTS WORKING STATUS")
            self.resetAllSlotsButton.setEnabled(True)

    def resetAllSlotStatus(self):
        for slotNumber in range(1, 61):
            regPath = f"SOFTWARE\WOW6432Node\SageUserData\slot_run_states\slot{slotNumber}"
            while True:
                try:
                    with winreg.OpenKey(self.reg, regPath, 0, winreg.KEY_SET_VALUE) as regKey:
                        winreg.SetValueEx(regKey, 'runStatus', 0, winreg.REG_SZ, '0')
                    break
                except:
                    time.sleep(3)

        self.resetAllSlotsButton.setText("DONE")
        time.sleep(2)
        self.resetAllSlotsButtonClicked(False)


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
                self.runExe('alquimyAutoStart.exe')
                self.startTimerAlquimy(minutes)
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
                self.runExe('closeClient.exe')
                self.startTimerCloseClient(minutes)
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
        self.runExe('shuffleCharacters.exe')

    def startEventRandomSetup(self):
        self.runExe('randomSetupEvent.exe')
    
    def startCheckLogs(self):
        self.checkLogsStartButton.setDisabled(True)
        self.checkLogsStartButton.setText('Check Logs (Running)')
        self.checkLogsStartButton.setStyleSheet("color: green;")
        self.runExe('checkLogs.exe')
        QTimer.singleShot(10000, lambda: self.startTimerCheckLogs(3000))

    def startCorNames(self):
        self.runExe('corNames.exe')

    def stopCheckLogsTimer(self):
        self.stopTimerCheckLogs()
        self.checkLogsStartButton.setEnabled(True)
        self.checkLogsStartButton.setText('Check Logs')
        self.checkLogsStartButton.setStyleSheet("")

    def startTimerAlquimy(self, minutes):
        self.timerAlquimy.start(minutes * 60 * 1000)
        self.alquimyRemainingSecondsTimer.start(1000)
        self.alquimyRemainingSeconds = minutes * 60
        self.alquimyRemainingSecondsTemp = minutes * 60

    def stopTimerAlquimy(self):
        self.timerAlquimy.stop()
        self.alquimyRemainingSecondsTimer.stop()

    def startTimerCloseClient(self, minutes):
        self.timerCloseClient.start(minutes * 60 * 1000)
        self.closeClientRemainingSecondsTimer.start(1000)
        self.closeClientRemainingSeconds = minutes * 60
        self.closeClientRemainingSecondsTemp = minutes * 60

    def stopTimerCloseClient(self):
        self.timerCloseClient.stop()
        self.closeClientRemainingSecondsTimer.stop()

    def startTimerCheckLogs(self, ms):
        self.timerCheckLogs.start(ms)

    def stopTimerCheckLogs(self):
        self.timerCheckLogs.stop()

    def runExe(self, programName):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", f"{programName}", None, None, 1)

    def runCheckLogsControl(self):
        allProcesses = psutil.process_iter(attrs=['name'])

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'checkLogs.exe'.lower():
                return
    
        self.stopCheckLogsTimer()

    def closeEvent(self, event):
        allProcesses = psutil.process_iter(attrs=['pid', 'name'])

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'checkLogs.exe'.lower():
                processPid = process.info['pid']
                psutil.Process(processPid).terminate()
  
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
