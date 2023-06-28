import os
import sys
import json
import time
import psutil
import hashlib
import requests
from colorama import init, Fore, Style

init()

class Patcher:
    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
        self.data = {
            'username': 'xxx',
            'password': 'xxx',
            'version': '2.3',
        }

    def calculateHash(self, filePath):
        hashAlgorithm = hashlib.sha256()
        with open(filePath, 'rb') as file:
            chunk = file.read(4096)
            while len(chunk) > 0:
                hashAlgorithm.update(chunk)
                chunk = file.read(4096)
        programHash = hashAlgorithm.hexdigest()
        return programHash
    
    def closeProgram(self, programName):
        allProcesses = psutil.process_iter(attrs=['name', 'pid'])

        for process in allProcesses:
            processName = process.info['name']
            processPid = process.info['pid']

            if processName.lower() == f'{programName}.exe'.lower():
                psutil.Process(processPid).terminate()


    def downloadFile(self, programName):
        self.closeProgram(programName)
    
        self.data['downloadProgramName'] = programName
        response = requests.post('http://xxx.xxx.xxx.xxx:2425/patcher', data=json.dumps(self.data), headers=self.headers, timeout=60, stream=True)

        if response.status_code == 200:
            totalSize = int(response.headers.get('Content-Length', 0))
            downloadedSize = 0
            startTime = time.time()

            with open(programName, 'wb') as file:
                for chunk in response.iter_content(chunk_size = 8192):
                    file.write(chunk)
                    downloadedSize += len(chunk)
                    self.printProgress(downloadedSize, totalSize, startTime)

            print(f'\n{Fore.GREEN}{programName} - Download completed.{Style.RESET_ALL}\n')
        else:
            print(f'\n{Fore.RED}Failed to download {programName}.{Style.RESET_ALL}\n')

    def printProgress(self, downloadedSize, totalSize, startTime):
        elapsedTime = max(time.time() - startTime, 0.01)
        progress = min(float(downloadedSize) / totalSize * 100, 100)
        downloadedMb = downloadedSize / (1024 * 1024)
        totalMb = totalSize / (1024 * 1024)
        downloadSpeed = downloadedSize / elapsedTime / (1024 * 1024)
        remainingTime = (totalSize - downloadedSize) / (downloadSpeed * 1024 * 1024) if downloadSpeed > 0 else 0

        print(f'\rDownloading... {progress:.2f}% complete ({downloadedMb:.2f}/{totalMb:.2f} MB) Speed: {downloadSpeed:.2f} MB/s Remaining Time: {remainingTime:.2f} seconds', end='', flush=True)

    def run(self):
        response = requests.post('http://xxx.xxx.xxx.xxx:2425/patcher', data=json.dumps(self.data), headers=self.headers, timeout=10).json()
        if response.get('status') == 200:
            programInfos = response.get('programInfos', [])

            if programInfos:
                for programInfo in programInfos:
                    serverProgramName = programInfo.get('programName')
                    serverProgramHash = programInfo.get('programHash')

                    if os.path.exists(serverProgramName):
                        localProgramHash = self.calculateHash(serverProgramName)
                        if serverProgramHash != localProgramHash:
                            print(f'{Fore.RED}{serverProgramName} - Update available. Downloading...{Style.RESET_ALL}')
                            self.downloadFile(serverProgramName)
                        else:
                            print(f'{Fore.GREEN}{serverProgramName} - Current version is up to date.{Style.RESET_ALL}')
                    else:
                        self.downloadFile(serverProgramName)
            else:
                print(f'{Fore.YELLOW}No files found to download.{Style.RESET_ALL}')
        else:
            print(response['message'])

        key = input('Please press enter to exit.')
        if key == "":
            sys.exit()


if __name__ == "__main__":
    patcher = Patcher()
    patcher.run()
