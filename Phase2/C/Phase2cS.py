from socket import * 
from threading import Thread

serverName = '127.0.0.1'
print("Connecting...")

def fileReceive():
    serverSocket1 = socket(AF_INET,SOCK_STREAM)
    serverSocket1.bind((serverName,12000))
    serverSocket1.listen(5)

    file, clientAddr = serverSocket1.accept()
    data = file.recv(2048).decode()
    print("Here")   
    filename = 'output.txt'
    fo = open(filename, "w") 
    fo.write(data) 
    
    print() 
    print('Receiving file from client') 
    print() 
    print('Received successfully! New filename is:', filename) 
    fo.close() 
    serverSocket1.close()

def fileSend():
    filename = input('Input filename you want to send: ') 
    serverSocket2 = socket(AF_INET,SOCK_STREAM)
    serverSocket2.connect(('127.0.0.2',12000))
   
    # Reading file and sending data to server 
    fi = open(filename, "r") 
    data = fi.read() 
    while data: 
        serverSocket2.send(str(data).encode()) 
        data = fi.read() 
    # File is closed after data is sent 
    fi.close() 

fileReceive()
# fileSend()
