from socket import *
from threading import Thread

hostSocket = socket(AF_INET,SOCK_DGRAM)
hostPort = 12000
hostName = 'localhost'
hostSocket.bind(('127.0.0.2',hostPort))
hostSocket.settimeout(0.2)
print("Ready to recieve: ")
username2 = input("Register your contact's name please: ")

def Recieve():
    while True:
        try:
            message, addr = hostSocket.recvfrom(12000)
            hostSocket.sendto("ACK2".encode(),(hostName,hostPort)) # Maybe here there is an issue
            print(message.decode())
        except:
            pass

def Send():
    while True:
        message = input()
        if message == 'exit':
            break
        acknowledged = False
        try:
            while not acknowledged :
                try:
                    ACK, addr = hostSocket.recvfrom(12000)
                    acknowledged  = True
                except:
                    hostSocket.sendto((username2 + ": " +message).encode(),(hostName,hostPort))
        except:
            pass

t1 = Thread(target=Recieve)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()