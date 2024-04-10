from socket import *
from threading import Thread

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverPort = 12000
serverName = 'localhost'
clientSocket.bind(('127.0.0.2',serverPort))
print("Ready to recieve: ")
username2 = input("Register your contact's name please: ")

def Recieve():
    while True:
        try:
            message, addr = clientSocket.recvfrom(12000)
            print(username2 + ': ' + message.decode())
        except:
            pass

def Send():
    while True:
        message = input("Enter Your Message: ")
        if message=='exit':
            break
        try:
            clientSocket.sendto(message.encode(),(serverName,serverPort))
        except:
            pass

t1 = Thread(target=Recieve)
t2 = Thread(target=Send)

t1.start()
t2.start()
