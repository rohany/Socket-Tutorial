import socket
import sys
from _thread import *
def servGet():
    while True:
        msg = s.recv(1024).decode()
        if msg != "":
            print(msg, "\n")

s = socket.socket()

host = socket.gethostname()

port = int(sys.argv[1])
name = sys.argv[2]
s.connect((host, port))
s.send(name.encode())
thread = start_new_thread(servGet,())

while True:
  
  msg = input()
  if msg == "exit":
      s.close()
      sys.exit()
  s.send(msg.encode())


