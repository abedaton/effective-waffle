#!/bin/python3

import socket
import threading
import time
import sys
import os
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


SERVER_IP="51.75.247.68"
#SERVER_IP = "0.0.0.0"
SERVER_PORT=10002
cprint=(lambda msg,color:print(msg))

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.sock.connect((address, SERVER_PORT))
        self.username = input("Entrez votre pseudo: ")
        self.iThread = threading.Thread(target = self.sendMsg)
        self.iThread.daemon = True
        self.iThread.start()


        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            msg=str(data,"utf-8")
            color="yellow" if ":" not in msg else "green" if msg[:msg.index(":")] in [self.username,self.username+" (pm)"] else "red" if msg[:7]=="[SERVER" else "cyan"
            if color=="green":
                msg="message sent"
            cprint(msg,color)

    def sendMsg(self):
        self.sock.send(bytes(self.username, "utf-8"))
        while True:
            msg=input("")
            if len(msg)>0 and msg[0]=="!":
                os.system(msg[1:])
            else:
                self.sock.send(bytes(msg, "utf-8"))

if __name__=="__main__":
    try:
        from termcolor import cprint
        print("success 1")
    except:
        try:
            os.system("pip3 install --user termcolor > /dev/null")
            print("Download des couleurs.....")
            time.sleep(10)
            from termcolor import cprint
            print("success 2")
        except:
            try:
                os.system("python3 -m pip install --user Xlib > /dev/null")
                print("Download des couleurs......")
                time.sleep(10)
                from termcolor import cprint
                print("success 3")
            except:
                cprint=(lambda msg,color:print(msg))
                print("ben no color for you bah voila")
    try:
        Client = Client(SERVER_IP)
    except KeyboardInterrupt:
        cprint("\nGoodbye :-)","magenta")
