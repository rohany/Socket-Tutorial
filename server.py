import select
import socket
import sys
import os
from threading import Thread
from _thread import *



def read(c, name, cliList, s, started):
    while True:
        msg = c.recv(1024).decode()
        if(msg == ""):
            c.close()
            cliList.remove(c)
            if len(cliList) == 0 and started:
                os._exit(0)
            break
        else:
            print(name,":",msg)
            for cli in cliList:
                if cli is not c:
                    msg = name + ": " + msg
                    cli.send(msg.encode())

s = socket.socket()
host = socket.gethostname()
port = int(sys.argv[1])

s.bind((host,port))

s.listen(5)
nameList = []
cliList = []
addrList = []
threadList = []
started = False
while True:
       
    c, addr = s.accept()
    nameList.append(c.recv(1024).decode())
    cliList.append(c)
    
    started = True
    thread = start_new_thread(read, (c, nameList[-1], cliList,s,started))
    threadList.append(thread)



