from socket import *
from threading import Thread
import sys
destHost = '127.0.0.2'
localHost = '127.0.0.1'
chatPort = 12000
filePort = 12001
hostSocket = socket(AF_INET, SOCK_DGRAM)
hostSocket.bind((localHost, chatPort))
fcount = 0
username = input("Register your contact's name please: ")
print()
print("welcome to the chat room, " + username + "!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room")
print()

def fileReceive():
    global fcount
    serverSocket1 = socket(AF_INET,SOCK_STREAM)
    serverSocket1.bind((destHost,filePort))
    serverSocket1.listen(5)

    file, clientAddr = serverSocket1.accept()
    data = file.recv(2048).decode()
    filename = 'received_file' + str(fcount) + '.txt'
    fcount += 1
    fo = open(filename, "w") 
    fo.write(data)  
    fo.close() 
    serverSocket1.close()
    return
    

def fileSend():
    filename = input('Input filename you want to send: ') 
    serverSocket2 = socket(AF_INET, SOCK_STREAM)
    serverSocket2.connect((destHost, filePort))
    # Reading file and sending data to server 
    fi = open(filename, "r") 
    data = fi.read() 
    # while data: 
    serverSocket2.send(str(data).encode()) 
    data = fi.read() 
    # File is closed after data is sent 
    fi.close() 
    serverSocket2.close()
    return

def Receive():
    while True:
        try:
            message, addr = hostSocket.recvfrom(12000)
            if message.decode() != "ACK" and message.decode() != "FILE":  # Don't print ACK messages
                print(message.decode())
            hostSocket.sendto("ACK".encode(), addr)  # Send ACK for all received messages
            if message.decode() == "FILE":
                print("File received!")
        except Exception as e:
            print("Error:", e)

def Send():
    while True:
        message = input()
        if message == 'exit':
            hostSocket.sendto((username + " has left the chat room").encode(), (destHost, chatPort))
            sys.exit()
        elif message == 'FILE':
            f1 = Thread(target=fileReceive)
            f2 = Thread(target=fileSend)
            f1.start()
            f2.start()
            f1.join()
            f2.join()
            print("File sent!")


        acknowledged = False
        try:
            # we need to also check for ack and timeout
            while not acknowledged:
                hostSocket.sendto((username + ": " + message).encode(), (destHost, chatPort))
                ACK, addr = hostSocket.recvfrom(chatPort)  # Wait for ACK
                if ACK.decode() == "ACK":
                    acknowledged = True
        except Exception as e:
            print("Error:", e)

t1 = Thread(target=Receive)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()
