from socket import *
from datetime import datetime
from threading import Thread

serverName = '127.0.0.2'
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('localhost',serverPort))
print("Server is ready")
username1 = input("Register your contact's name please: ")

def Recieve():
    while True:
        try:
            message, addr = serverSocket.recvfrom(12000)
            print(username1 + ': ' + message.decode())
        except:
            pass

def Send():
    while True:
        message = input("Enter Your Message: ")
        if message == 'exit':
            break
        try:
            serverSocket.sendto(message.encode(),(serverName,serverPort))
        except:
            pass

t1 = Thread(target=Recieve)
t2 = Thread(target=Send)

t1.start()
t2.start()

