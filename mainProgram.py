import sys
import os
import json
import time
import ctypes
import psutil
import winreg
import requests
import threading
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alquimy Helper")
        self.layout = QVBoxLayout()
        self.setGeometry(100, 100, 500, 50)

        icon = QIcon(os.path.join(os.path.dirname(__file__), 'alchi.ico'))
        self.setWindowIcon(icon)

        self.reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        self.autoStartRunStatus = False

        self.pcIps = {
            'x': 'x'
        }

        ipAddress = requests.get('https://icanhazip.com/', timeout=30).text.strip()
        self.pc = next((key for key, value in self.pcIps.items() if value == ipAddress), None)

        ###############################--TİMERS--################################
    
        self.alquimyRemainingSecondsTimer = QTimer()
        self.alquimyRemainingSecondsTimer.timeout.connect(self.updateAlquimyTimer)

        self.timerAlquimyRunStatus = QTimer()
        self.timerAlquimyRunStatus.timeout.connect(self.alquimyRunStatus)

        self.closeClientRemainingSecondsTimer = QTimer()
        self.closeClientRemainingSecondsTimer.timeout.connect(self.updateCloseClientTimer)

        self.closeClientRemainingSecondsTimer = QTimer()
        self.closeClientRemainingSecondsTimer.timeout.connect(self.updateCloseClientTimer)

        self.characterCreateRemainingSecondsTimer = QTimer()
        self.characterCreateRemainingSecondsTimer.timeout.connect(self.updateCharacterCreateTimer)

        self.timerAlquimy = QTimer()
        self.timerAlquimy.timeout.connect(lambda: self.runExe('newAutoStart.exe'))

        self.timerCloseClient = QTimer()
        self.timerCloseClient.timeout.connect(lambda: self.runExe('closeClient.exe'))

        self.timerCharacterCreate = QTimer()
        self.timerCharacterCreate.timeout.connect(lambda: self.runExe('characterCreate.exe'))

        self.timerCheckLogs = QTimer()
        self.timerCheckLogs.timeout.connect(self.runCheckLogsControl)

        ###############################--BUTTONS--###############################

        self.resetAllSlotsButton = QPushButton("RESET ALL SLOTS RUN STATUS", self)
        self.resetAllSlotsButton.clicked.connect(lambda: self.resetAllSlotsButtonClicked(True))

        self.alquimyStartButton = QPushButton("Auto Start", self)
        self.alquimyStartButton.clicked.connect(self.startAlquimy)

        self.alquimyMinutes = QLineEdit(self)
        self.alquimyMinutes.setPlaceholderText("1 minute repeat")

        self.alquimyStopButton = QPushButton("Stop", self)
        self.alquimyStopButton.clicked.connect(self.stopAlquimy)

        self.closeClientStartButton = QPushButton("Close Client", self)
        self.closeClientStartButton.clicked.connect(self.startCloseClient)

        self.closeClientMinutes = QLineEdit(self)
        self.closeClientMinutes.setPlaceholderText("Enter minutes")

        self.closeClientStopButton = QPushButton("Stop", self)
        self.closeClientStopButton.clicked.connect(self.stopCloseClient)

        self.characterCreateStartButton = QPushButton("Character Create", self)
        self.characterCreateStartButton.clicked.connect(self.startCharacterCreate)

        self.characterCreateMinutes = QLineEdit(self)
        self.characterCreateMinutes.setPlaceholderText("Enter minutes")

        self.characterCreateStopButton = QPushButton("Stop", self)
        self.characterCreateStopButton.clicked.connect(self.stopCharacterCreate)

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

        characterCreateLayout = QHBoxLayout()
        characterCreateLayout.addWidget(self.characterCreateStartButton)
        characterCreateLayout.addWidget(self.characterCreateMinutes)
        characterCreateLayout.addWidget(self.characterCreateStopButton)

        otherProgramsLayout = QHBoxLayout()
        otherProgramsLayout.addWidget(self.shuffleCharacterStartButton)
        otherProgramsLayout.addWidget(self.eventRandomSetupStartButton)
        otherProgramsLayout.addWidget(self.checkLogsStartButton)
        otherProgramsLayout.addWidget(self.corNamesStartButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(resetAllSlotButtonLayout)
        mainLayout.addLayout(alquimyButtonLayout)
        mainLayout.addLayout(closeClientLayout)
        mainLayout.addLayout(characterCreateLayout)
        mainLayout.addLayout(otherProgramsLayout)

        ##########################################################################

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        if not self.pc:
            self.alquimyStartButton.setDisabled(True)

        self.alquimyMinutes.setDisabled(True)
        self.alquimyStopButton.setDisabled(True)
        self.closeClientStopButton.setDisabled(True)
        self.characterCreateStopButton.setDisabled(True)

        ###########################################################################


    ###############################--FUNCTİONS--#######################################


    ## RESET ALL SLOT RUN STATUS ##

    def resetAllSlotsButtonClicked(self, buttonStatus):
        if buttonStatus:
            self.resetAllSlotsButton.setDisabled(True)
            self.resetAllSlotsButton.setText("Working...")

            thread = threading.Thread(target = self.resetAllSlotStatus)
            thread.start()
        else:
            self.resetAllSlotsButton.setText("RESET ALL SLOTS RUN STATUS")
            self.resetAllSlotsButton.setEnabled(True)

    def resetAllSlotStatus(self):
        requests.put('http://xxxxxxxxx:xxxxxxx/resetAllSlot', data=jsonData, headers=headers, timeout=30).json()
        for slotNumber in range(1, 61):
            logFile = f'C:\\SageBot\\userdata\\logs\\slot_log_{slotNumber}.txt'
            regPath = f"SOFTWARE\WOW6432Node\SageUserData\slot_run_states\slot{slotNumber}"

            if os.path.exists(logFile):
                os.remove(logFile)

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

    #--------------------------------------------------#

    ## AUTO START ##
    def startAlquimy(self):
        self.alquimyStartButton.setDisabled(True)
        self.alquimyStopButton.setEnabled(True)
        self.alquimyStartButton.setStyleSheet("color: green;")
        self.runExe('newAutoStart.exe')
        self.startTimerAlquimy(1)

    def stopAlquimy(self):
        self.stopTimerAlquimy()
        self.alquimyStartButton.setEnabled(True)
        self.alquimyStopButton.setDisabled(True)
        self.alquimyStartButton.setText(f"Auto Start")
        self.alquimyStartButton.setStyleSheet("")
    
    def startTimerAlquimy(self, minutes):
        self.timerAlquimy.start(minutes * 60 * 1000)
        self.timerAlquimyRunStatus.start(100)
        self.alquimyRemainingSecondsTimer.start(1000)
        self.alquimyRemainingSeconds = minutes * 60
        self.alquimyRemainingSecondsTemp = minutes * 60
    
    def stopTimerAlquimy(self):
        self.timerAlquimy.stop()
        self.timerAlquimyRunStatus.stop()
        self.autoStartRunStatus = False
        self.alquimyStopButton.setEnabled(True)
        self.alquimyRemainingSecondsTimer.stop()

    def updateAlquimyTimer(self):
        minutes = self.alquimyRemainingSecondsTemp // 60
        seconds = self.alquimyRemainingSecondsTemp % 60

        self.alquimyStartButton.setText(f"Auto Start ({minutes:02d}:{seconds:02d})")

        if self.alquimyRemainingSecondsTemp == 0:
            self.alquimyRemainingSecondsTemp = self.alquimyRemainingSeconds
        else:
            self.alquimyRemainingSecondsTemp -= 1
    
    def alquimyRunStatus(self):
        allProcesses = psutil.process_iter(attrs=['name'])

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'newAutoStart.exe'.lower():
                self.autoStartRunStatus = True
                self.alquimyStopButton.setDisabled(True)
                return

        self.alquimyStopButton.setEnabled(True)
        self.autoStartRunStatus = False

    #--------------------------------------------------#

    ## CLOSE CLIENT ##
    def startCloseClient(self):
        minutesText = self.closeClientMinutes.text()
        if minutesText.isdigit():
            minutes = int(minutesText)
            if minutes > 0:
                self.closeClientStartButton.setDisabled(True)
                self.closeClientStopButton.setEnabled(True)
                self.closeClientMinutes.setText(f'{minutesText} minute repeat')
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
    
    def startTimerCloseClient(self, minutes):
        self.timerCloseClient.start(minutes * 60 * 1000)
        self.closeClientRemainingSecondsTimer.start(1000)
        self.closeClientRemainingSeconds = minutes * 60
        self.closeClientRemainingSecondsTemp = minutes * 60
    
    def stopTimerCloseClient(self):
        self.timerCloseClient.stop()
        self.closeClientRemainingSecondsTimer.stop()
    
    def updateCloseClientTimer(self):
        minutes = self.closeClientRemainingSecondsTemp // 60
        seconds = self.closeClientRemainingSecondsTemp % 60

        self.closeClientStartButton.setText(f"Close Client ({minutes:02d}:{seconds:02d})")

        if self.closeClientRemainingSecondsTemp == 0:
            self.closeClientRemainingSecondsTemp = self.closeClientRemainingSeconds
        else:
            self.closeClientRemainingSecondsTemp -= 1

    #--------------------------------------------------#

    ## CHARACTER CREATE ##
    def startCharacterCreate(self):
        self.minutesText = self.characterCreateMinutes.text()
        if self.minutesText.isdigit():
            minutes = int(self.minutesText)
            if minutes > 0:
                self.characterCreateStartButton.setDisabled(True)
                self.characterCreateStopButton.setEnabled(True)
                self.characterCreateMinutes.setText(f'{self.minutesText} minute repeat')
                self.characterCreateMinutes.setDisabled(True)
                self.characterCreateStartButton.setStyleSheet("color: green;")
                self.runExe('characterCreate.exe')
                self.startTimerCharacterCreate(minutes)
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer value for minutes.")

    def stopCharacterCreate(self):
        self.stopTimeCharacterCreate()
        self.characterCreateStartButton.setEnabled(True)
        self.characterCreateStopButton.setDisabled(True)
        self.characterCreateMinutes.setText(f'{self.minutesText}')
        self.characterCreateMinutes.setEnabled(True)
        self.characterCreateStartButton.setText(f"Character Create")
        self.characterCreateStartButton.setStyleSheet("")

    def startTimerCharacterCreate(self, minutes):
        self.timerCharacterCreate.start(minutes * 60 * 1000)
        self.characterCreateRemainingSecondsTimer.start(1000)
        self.characterCreateRemainingSeconds = minutes * 60
        self.characterCreateRemainingSecondsTemp = minutes * 60

    def stopTimeCharacterCreate(self):
        self.timerCharacterCreate.stop()
        self.characterCreateRemainingSecondsTimer.stop()
    
    def updateCharacterCreateTimer(self):
        minutes = self.characterCreateRemainingSecondsTemp // 60
        seconds = self.characterCreateRemainingSecondsTemp % 60

        self.characterCreateStartButton.setText(f"Character Create ({minutes:02d}:{seconds:02d})")

        if self.characterCreateRemainingSecondsTemp == 0:
            self.characterCreateRemainingSecondsTemp = self.characterCreateRemainingSeconds
        else:
            self.characterCreateRemainingSecondsTemp -= 1

    #--------------------------------------------------#

    ## CHECK LOGS ##
    def startCheckLogs(self):
        self.checkLogsStartButton.setDisabled(True)
        self.checkLogsStartButton.setText('Check Logs (Running)')
        self.checkLogsStartButton.setStyleSheet("color: green;")
        self.runExe('checkLogs.exe')
        QTimer.singleShot(10000, lambda: self.startTimerCheckLogs(3000))

    def stopCheckLogsTimer(self):
        self.stopTimerCheckLogs()
        self.checkLogsStartButton.setEnabled(True)
        self.checkLogsStartButton.setText('Check Logs')
        self.checkLogsStartButton.setStyleSheet("")

    def startTimerCheckLogs(self, ms):
        self.timerCheckLogs.start(ms)

    def stopTimerCheckLogs(self):
        self.timerCheckLogs.stop()

    def runCheckLogsControl(self):
        allProcesses = psutil.process_iter(attrs=['name'])

        for process in allProcesses:
            processName = process.info['name']

            if processName.lower() == 'checkLogs.exe'.lower():
                return
    
        self.stopCheckLogsTimer()

    #--------------------------------------------------#

    ## EVENT RANDOM SETUP ##
    def startEventRandomSetup(self):
        self.runExe('randomSetupEvent.exe')

    #--------------------------------------------------#

    ## SHUFFLE CHARACTERS ##
    def startShuffleCharacters(self):
        self.runExe('shuffleCharacters.exe')

    #--------------------------------------------------#

    ## COR NAMES ##
    def startCorNames(self):
        self.runExe('corNames.exe')

    #--------------------------------------------------#

    ## RUN ##
    def runExe(self, programName):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", f"{programName}", None, None, 1)

    #--------------------------------------------------#

    ## HANDLE CLOSE EVENT ##
    def closeEvent(self, event):
        if self.autoStartRunStatus:
            event.ignore()
        else:
            event.accept()

            allProcesses = psutil.process_iter(attrs=['pid', 'name'])

            for process in allProcesses:
                processName = process.info['name']

                if processName.lower() == 'checkLogs.exe'.lower():
                    processPid = process.info['pid']
                    psutil.Process(processPid).terminate()

            super().closeEvent(event)

    ###############################--FUNCTİONS--#######################################

if __name__ == "__main__":
    headers = {'Content-type': 'application/json'}

    data = {
        'username': 'JonySales',
        'password': 'JonySales'
    }

    jsonData = json.dumps(data)
    response = requests.post('http://xxxxxxx:xxxxxx/login', data=jsonData, headers=headers, timeout = 10).json()
    if response['status'] == 200:
        app = QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        app = QApplication([])
        QMessageBox.warning(None, "Server error", "Server error.")
        sys.exit()
