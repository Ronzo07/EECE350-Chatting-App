from socket import *

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
userName = input("Enter your name: ")
clientSocket.sendto(userName.encode(), (serverName, serverPort))

while True:
    message = input('Message (type "exit" to stop): ')
    if message.lower() == 'exit':
        break
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(100000)
    print(modifiedMessage.decode())

clientSocket.close()