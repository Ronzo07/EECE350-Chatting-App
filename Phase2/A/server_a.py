from socket import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('localhost',serverPort))
print("The UDP server is ready to receive")
userName, clientAddress = serverSocket.recvfrom(100000)
userName = userName.decode()
while True:
    message, clientAddress = serverSocket.recvfrom(100000)
    print(userName+': '+message.decode())
    response = "Message received"
    serverSocket.sendto(response.encode(), clientAddress)
