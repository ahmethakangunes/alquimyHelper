import os
import requests
import threading
import subprocess


class ProgramCompiler:
    def __init__(self):
        self.errorCommand = []
        self.commands = [
            "python -m nuitka --onefile --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\shuffleCharacters.py",
            "python -m nuitka --onefile --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\corNames.py",
            "python -m nuitka --onefile --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\randomSetupEvent.py",
            "python -m nuitka --onefile --disable-console --standalone --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\alquimyAutoStart\\newAutoStart.py",
            "python -m nuitka --onefile --disable-console --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\closeClient.py",
            "python -m nuitka --onefile --disable-console --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\checkLogs.py",
            "python -m nuitka --onefile --disable-console --output-dir=C:\\Users\\Ahmet\\Desktop\\compiler C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\characterCreate.py"
        ]
        self.threads = []
        self.lock = threading.Lock()

    def executeCommand(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            with self.lock:
                self.errorCommand.append(command)

    def compileUtilsProgram(self):
        for cmd in self.commands:
            thread = threading.Thread(target=self.executeCommand, args=(cmd,))
            self.threads.append(thread)
            thread.start()

        for thread in self.threads:
            thread.join()

        if self.errorCommand:
            os.system('cls')
            for errorCommand in self.errorCommand:
                print(errorCommand)
        else:
            self.compileMainProgram()

    def compileMainProgram(self):
        exeFiles = [
            "shuffleCharacters.exe",
            "corNames.exe",
            "randomSetupEvent.exe",
            "newAutoStart.exe",
            "closeClient.exe",
            "checkLogs.exe",
            "characterCreate.exe"
        ]

        mainProgram = "C:\\Users\\Ahmet\\Desktop\\alquimyExe\\sourceCodes\\newProgram.py"
        outputDir = "C:\\Users\\Ahmet\\Desktop\\alquimyExe"

        includeDataFiles = [f"{exe}={exe}" for exe in exeFiles]

        command = [
            "python",
            "-m",
            "nuitka",
            "--onefile",
            "--enable-plugin=pyqt6",
            "-oAlquimy Helper",
            "--include-data-file=C:\\Users\\Ahmet\\Desktop\\compiler\\alchi.ico=alchi.ico",
            "--disable-console",
            "--windows-icon-from-ico=alchi.ico",
            "--standalone",
            *["--include-data-file=" + file for file in includeDataFiles],
            "--output-dir=" + outputDir,
            mainProgram
        ]

        try:
            subprocess.run(command, check=True)
            self.uploadProgram()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during program compilation: {e}")

    def uploadProgram(self):
        os.system('cls')
        print('Uploading...')
        uploadSha = 'xxxxxxxxxxxxxxxxxx'
        url = 'http://xxxxxx:xxxxxxxx/upload'
        filePath = 'C:\\Users\\Ahmet\\Desktop\\alquimyExe\\Alquimy Helper.exe'

        headers = {'uploadSha': uploadSha}

        with open(filePath, 'rb') as dosya:
            fileData = {'file': dosya}
            response = requests.post(url, files=fileData, headers=headers)

        print(response.text)

if __name__ == "__main__":
    executor = ProgramCompiler()
    executor.compileUtilsProgram()
