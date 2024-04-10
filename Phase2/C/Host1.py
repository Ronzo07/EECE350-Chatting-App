from socket import *
from threading import Thread

hostName = '127.0.0.2'
hostPort = 12000
hostSocket = socket(AF_INET,SOCK_DGRAM)
hostSocket.bind(('localhost',hostPort))
hostSocket.settimeout(0.2)
print("host is ready")
username1 = input("Register your contact's name please: ")

def Recieve():
    while True:
        try:
            message, addr = hostSocket.recvfrom(12000)
            hostSocket.sendto("ACK1".encode(),(hostName,hostPort)) # Maybe here there is an issue
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
                    hostSocket.sendto((username1 + ": " +message).encode(),(hostName,hostPort))
        except:
            pass

t1 = Thread(target=Recieve)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()