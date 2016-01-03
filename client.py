import socket
import sys
from _thread import *

#look at this function later
def servGet():
    #as we started this function in a thread, it is going at the same time as the rest of the code
    #we start a while true loop here to constantly read from the server
    while True:
        #we get the message from the server with the recv function
        #the argument is the size of the message that is being recieved
        #and since we encoded the message when we sent it, we must decode it when we recieve it
        #recv is a blocking function, meaning the code will not go past this function
        #until some message is recieved
        msg = s.recv(1024).decode()
        #we only want to print out actual messages, so we filter out any empty strings
        if msg != "":
            print(msg, "\n")
        #now go back down past the thread creation

#Here we create the socket for the client
s = socket.socket()

#As this code is running on the local host, we get the host socket, or the server as such
host = socket.gethostname()

#Here we let the user enter the port they are using when they run this file
#we must check that there are enough arguments
#sys.argv is the command line argument list
if len(sys.argv) == 3:
    #Get the port as an integer from the arguments
    port = int(sys.argv[1])
    #Get the users name from the arguments
    name = sys.argv[2]
else:
    print("Usage: client.py port name")

#now connect the client socket to the host socket
s.connect((host, port))

#send the user's name to the server first
#note you must encode the string for the socket to send it in Python 3
s.send(name.encode())

#Now to recieve data from the server we must start a new thread
#A thread is a seperate process that the program runs at the same time
#We start a thread so that we can read from the server, and send to the server at the same time
#The usage is start_new_thread(FunctionName, argument tuple)
#check out the servGet function now
thread = start_new_thread(servGet,())

#Here we start the sending from the client to the server
while True:
    #get the typed input from the user
    msg = input()
    #I decided to add if the user types exit, we end this client socket
    if msg == "exit":
        #first we must close the socket so no more communication occurs
        s.close()
        #then we exit from the program
        #the thread we created exits as well
        sys.exit()
    #assuming the message is not "exit", we send the message to the server
    s.send(msg.encode())


