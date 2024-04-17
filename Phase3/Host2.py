from socket import *
from threading import Thread
import sys
localHost = '127.0.0.2'
destHost = '127.0.0.1'
chatPort = 12000
filePort = 12001
hostSocket = socket(AF_INET, SOCK_DGRAM)
hostSocket.bind((localHost, chatPort))
username = input("Register your contact's name please: ")
nbFile = '_2_'
print()
print("Welcome to the chat room, " + username + "!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room")
print()

def fileReceive(fileName):
    recieverSocket = socket(AF_INET,SOCK_STREAM)
    recieverSocket.bind((destHost,filePort))
    recieverSocket.listen(5)

    file, clientAddr = recieverSocket.accept()
    filename = "received" + nbFile + fileName
    fo = open(filename, "wb") 
    data = file.recv(1024)
    while data: # While data is being received, write it to the file
        fo.write(data)
        data = file.recv(1024)
    fo.close() 
    recieverSocket.close()
    

def fileSend(fileName):
    senderSocket = socket(AF_INET, SOCK_STREAM)
    senderSocket.connect((destHost, filePort))
    # Reading file and sending data to server 
    fi = open(fileName, "rb") 
    data = fi.read(1024) 
    while data: 
        senderSocket.send(data) 
        data = fi.read(1024) 
    # File is closed after data is sent 
    fi.close() 
    senderSocket.close()
    return

def Receive():
    while True:
        try:
            message, addr = hostSocket.recvfrom(chatPort)
            if message.decode() != "ACK" and (len(message.decode()) >= 4 and message.decode()[-4:] != "FILE"):  # Don't print ACK messages
                print(message.decode())
            hostSocket.sendto("ACK".encode(), addr)  # Send ACK for all received messages
            if len(message.decode()) >= 4 and message.decode()[-4:] == "FILE":
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
            fileName = input('Input filename you want to send: ') 
            f1 = Thread(target=fileReceive, args=(fileName,))
            f2 = Thread(target=fileSend, args=(fileName,))
            f1.start()
            f2.start()
            f1.join()
            f2.join()
            print("File sent!")


        CHUNK_SIZE = 1024  # 1KB per chunk
        message_chunks = [message[i:i+CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]

        for chunk in message_chunks:
            print("Sending chunk:", chunk)
            acknowledged = False
            while not acknowledged:
                hostSocket.settimeout(5)  # Timeout after 5 seconds
                hostSocket.sendto((username + ": " + chunk).encode(), (destHost, chatPort))
                try:
                    ACK, addr = hostSocket.recvfrom(chatPort)  # Wait for ACK
                    if ACK.decode() == "ACK":
                        acknowledged = True
                except timeout:
                    print("No ACK received for chunk. Resending chunk.")
                except Exception as e:
                    print("Error:", e)
                finally:
                    hostSocket.settimeout(None)
                    if acknowledged:
                        print("Chunk acknowledged.")
                    else:
                        print("Resending chunk due to timeout.")


t1 = Thread(target=Receive)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()
