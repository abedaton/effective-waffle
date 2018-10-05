#!/usr/bin/env python3

import socket
import threading
import sys
import os

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(("0.0.0.0", 10000))
        self.sock.listen(1)

    def handler(self, c, a, username):
        while True:
            data = c.recv(1024)
            if not data:
                print(str(a[0]) + ":" + str(a[1]), "disconnected")
                self.connections.remove([c,username])
                for connection in self.connections:
                    connection[0].send(username+b' disconnected\n')
                c.close()
                break
            data=str(data,"utf-8")
            msg=data.split(maxsplit=2)
            if msg[0]=="/msg":
                for connection in self.connections:
                    if connection[1]==msg[1]:
                        connection[0].send(username+b': '+bytes(msg[2],"utf-8"))
            else:
                for connection in self.connections:
                    connection[0].send(username+b': '+bytes(data,"utf-8"))

    def run(self):
        while True:
            c, a = self.sock.accept()
            username=c.recv(1024)
            for connection in self.connections:
                connection[0].send(username+b' connected')
            users=[str(connection[1],"utf-8") for connection in self.connections]
            c.send(bytes("Users connected:\n"+("\n".join(users) if len(users)>0 else "None"),"utf-8"))
            self.connections.append([c,username])
            cThread = threading.Thread(target=self.handler, args=(c, a, username))
            cThread.daemon = True
            cThread.start()
            print(str(a[0]) + ":" + str(a[1]), "connected")



class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.sock.connect((address, 10000))
        self.username = input("Entrez votre pseudo: ")
        self.iThread = threading.Thread(target = self.sendMsg)
        self.iThread.daemon = True
        self.iThread.start()


        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            msg=str(data,"utf-8")
            color="yellow" if ":" not in msg else "green" if msg[:msg.index(":")]==self.username else "cyan"
            if color=="green":
                msg="message sent"
            cprint(msg,color)

    def sendMsg(self):
        self.sock.send(bytes(self.username, "utf-8"))
        while True:
            msg=input("")
            if msg[0]=="!":
                os.system(msg[1:])
            else:
                self.sock.send(bytes(msg, "utf-8"))


if (len(sys.argv) > 1):
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
                os.system(os.system("python3 -m pip install --user Xlib > /dev/null"))
                print("Download des couleurs......")
                time.sleep(10)
                from termcolor import cprint
                print("success 3")
            except:
                cprint=(lambda msg,color:print(msg))
                print("ben no color for you bah voila")
    try:
        Client = Client(sys.argv[1])
    except KeyboardInterrupt:
        cprint("\nGoodbye :-)","magenta")
else:
    server = Server()
    server.run()
