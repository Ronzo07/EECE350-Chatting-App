from socket import *
from threading import Thread

hostName = 'localhost'
hostPort = 12000
hostSocket = socket(AF_INET, SOCK_DGRAM)
hostSocket.bind(('127.0.0.2', hostPort))
print("Ready to receive")
username2 = input("Register your contact's name please: ")

def Receive():
    while True:
        try:
            message, addr = hostSocket.recvfrom(12000)
            if message.decode() != "ACK":  # Don't print ACK messages
                print(message.decode())
            hostSocket.sendto("ACK".encode(), addr)  # Send ACK for all received messages
        except Exception as e:
            print("Error:", e)

def Send():
    while True:
        message = input()
        if message == 'exit':
            break
        acknowledged = False
        try:
            while not acknowledged:
                hostSocket.sendto((username2 + ": " + message).encode(), (hostName, hostPort))
                ACK, addr = hostSocket.recvfrom(12000)  # Wait for ACK
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
