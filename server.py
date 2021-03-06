#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
#from ctypes import cdll
#lib = cdll.LoadLibrary("./database.so")

#SERVER_IP="51.75.126.222"
#SERVER_IP = "0.0.0.0"

SERVER_PORT=10002

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(("0.0.0.0", SERVER_PORT))
        self.sock.listen(1)
        print("success")
        #lib.callMain()
        print("call main success !!")

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
                        cprint(str(closeCon[1],"utf-8")+" kicked","yellow")
                        for connection in self.connections:
                            if connection[0] not in cmd[1].split():
                                connection[0].send(closeCon[1]+b' kicked\n')
                        self.connections.remove(closeCon)
                        closeCon[0].close()
                elif cmd[0]=="online":
                    cprint("Users online:","cyan")
                    for connection in self.connections:
                        cprint(str(connection[1],"utf-8"),"cyan")
                elif cmd[0]=="reboot":
                    for connection in self.connections:
                        connection[0].send(b'[SERVER]: Server will reboot in '+bytes(i)+b"\n")

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


if __name__=="__main__":
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        print("byeee")
