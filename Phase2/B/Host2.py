from socket import *
from threading import Thread

hostSocket = socket(AF_INET,SOCK_DGRAM)
serverPort = 12000
serverName = 'localhost'
hostSocket.bind(('127.0.0.2',serverPort))
print("Ready to recieve: ")
username2 = input("Register your contact's name please: ")

def Recieve():
    while True:
        try:
            message, addr = hostSocket.recvfrom(12000)
            print(message.decode())
        except:
            pass

def Send():
    while True:
        message = input()
        if message=='exit':
            break
        try:
            hostSocket.sendto((username2 + ": " +message).encode(),(serverName,serverPort))
        except:
            pass

t1 = Thread(target=Recieve)
t2 = Thread(target=Send)

t1.start()
t2.start()