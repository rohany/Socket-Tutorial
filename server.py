import socket
import sys
import os
from threading import Thread
from _thread import *


#look at this function later
def read(c, name, cliList, s, started):
    #for our read function, we want to know the client this thread is going to handle,
    #the name of the client
    #all the current clients, the host, and whether the program was started or not
    #we use a while true to continually recieve
    while True:
        #here we use recv to recieve any message sent from a client
        msg = c.recv(1024).decode()
        #an empty string sent by a client is what is sent when the client has closed the socket
        #so we need to catch this case as such
        if(msg == ""):
            #when the client has closed the socket on thier end, we must close it on the server 
            #end as well
            c.close()
            #then we remove this client from our list of active clients
            cliList.remove(c)
            #additionally, we want the server to close when it has no more clients
            #so if the client list is empty, we will end the server program
            if len(cliList) == 0 and started:
                #end the server program
                os._exit(0)
            break
        else:
            #assuming the message is not the empty string, we print the message out in the server
            print(name,":",msg)
            #and then send the message to each client
            for cli in cliList:
                #we iterate through all the clients, and send the message to every client
                #that is not the one who sent it
                if cli is not c:
                    msg = name + ": " + msg
                    cli.send(msg.encode())

#Here we create the socket for the server, or the host
s = socket.socket()
#As we are on the local host, we get the host name of the machine with the following command
host = socket.gethostname()
#set the port to get it from the command line
port = 0;
#We want to get arguments from the command line, so we need to check if the correct number is there
if len(sys.argv) == 2:
    #if we have the correct number, we get the port number we want to use as an integer
    port = int(sys.argv[1])
else:
    #handle when input is incorrect
    print("Usage: server.py port")

#now that we have the host and the port, we bind the socket to the host and port number
#letting it act as the server
s.bind((host,port))
#now we listen for clients
#the argument 5 is the maximum number of connect requests
s.listen(5)

#here we make some lists keeping track of the data we need to make a simple server
#a list of the names that the clients have
nameList = []
#a list of the clients
cliList = []
#and a variable keeping track of whether the program has started yet
started = False
#here is the body of the program, running the server
while True: 
    #to let a client connect, we use the accept() method to get the client and the address
    #like recv, this function also blocks, in that the code wont go on until a client connects
    c, addr = s.accept()
    #since we had the client send their name first, we recieve the name, and add it to our list
    nameList.append(c.recv(1024).decode())
    #then we add the new client to our list as well
    cliList.append(c)
    
    #as we have at least 1 client connected, we can set the started variable to true
    started = True
    #now since we want to read from all the clients, and send and recieve messages, we need a new thread
    #so now go up and look at the function read
    #we give the function the arguments it needs
    #the current client to handle, its name
    #we use nameList[-1] as -1 index is the last index, and since we just added it, the 
    #name we want is the last index
    thread = start_new_thread(read, (c, nameList[-1], cliList, s, started))



