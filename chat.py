#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os

#SERVER_IP="51.75.126.222"
SERVER_IP ="0.0.0.0"
class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(("0.0.0.0", 10000))
        self.sock.listen(1)

    def handler(self, c, a, username):
        while True:
            try:
                data = c.recv(1024)
            except:
                break
            if not data or [c,username] not in self.connections:
                try:
                    self.connections.remove([c,username])
                    for connection in self.connections:
                        connection[0].send(username+b' disconnected\n')
                    c.close()
                    print(str(a[0]) + ":" + str(a[1]),"("+str(username,"utf-8")+")", "disconnected")
                except:
                    pass
                finally:
                    break
            data=str(data,"utf-8")
            msg=data.split(maxsplit=2)
            if len(msg)==3 and msg[0]=="/msg":
                for connection in self.connections:
                    if connection[1]==bytes(msg[1],"utf-8") or connection[1]==username:
                        connection[0].send(username+b' (pm): '+bytes(msg[2],"utf-8"))
            elif len(msg)==1 and msg[0] == "/online":
                    users = [str(connection[1],"utf-8") for connection in self.connections]
                    c.send(bytes("Users connected:\n"+("\n".join(users) if len(users)>0 else "None"),"utf-8"))
            elif len(msg)==2 and msg[0] == "/online":
                    users = [str(connection[1],"utf-8") for connection in self.connections]
                    c.send(bytes(msg[1]+(" online" if msg[1] in users else " offline"),"utf-8"))
            else:
                for connection in self.connections:
                    connection[0].send(username+b': '+bytes(data,"utf-8"))

    def commandHandler(self):
        while True:
            cmd=input("").split(maxsplit=1)
            if len(cmd)>0:
                if cmd[0]=="msgall" and len(cmd)>1:
                    for connection in self.connections:
                        connection[0].send(b'[SERVER]: '+bytes(cmd[1],"utf-8"))
                elif cmd[0]=="msg" and len(cmd)>1:
                    msg=cmd[1].split(maxsplit=1)
                    if len(msg)>1:
                        for connection in self.connections:
                            if connection[1]==bytes(msg[0],"utf-8"):
                                connection[0].send(b'[SERVER (pm)]: '+bytes(msg[1],"utf-8"))
                elif cmd[0]=="kick" and len(cmd)>1:
                    closeCons=[]
                    for connection in self.connections:
                        if str(connection[1],"utf-8") in cmd[1].split():
                            closeCons.append(connection)
                            connection[0].send(b"You have been kicked ! Press enter to continue.")
                    for closeCon in closeCons:
                        print(str(closeCon[1],"utf-8"), "kicked")
                        for connection in self.connections:
                            if connection[0] not in cmd[1].split():
                                connection[0].send(closeCon[1]+b' kicked\n')
                        self.connections.remove(closeCon)
                        closeCon[0].close()
                elif cmd[0]=="reboot":
                    i = 10
                    while i > 0:
                        for connection in self.connections:
                            connection[0].send(b'[SERVER]: Server will reboot in '+bytes(i)+b"\n")
                        time.sleep(1)
                        i -= 1
                        if i == 0:
                            for connection in self.connections:
                                connection[0].send(b"[SERVER]: Rebooting.....")
                            sys.exit()
                            raise SystemExit
                            raise KeyboardInterrupt

    def run(self):
        cmdThread = threading.Thread(target=self.commandHandler)
        cmdThread.daemon = True
        cmdThread.start()
        while True:
            c, a = self.sock.accept()
            username=c.recv(1024)
            print(str(a[0]) + ":" + str(a[1]),"("+str(username,"utf-8")+")", "connected")
            for connection in self.connections:
                connection[0].send(username+b' connected')
            users=[str(connection[1],"utf-8") for connection in self.connections]
            c.send(bytes("Users connected:\n"+("\n".join(users) if len(users)>0 else "None"),"utf-8"))
            self.connections.append([c,username])
            cThread = threading.Thread(target=self.handler, args=(c, a, username))
            cThread.daemon = True
            cThread.start()

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
    if (len(sys.argv) <= 1):
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
    else:
        server = Server()
        server.run()
