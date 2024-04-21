from socket import *
from threading import Thread
import sys

localHost = '127.0.0.2'
destHost = '127.0.0.1'

chatPortSend = 12001
chatPortRecv = 12000
filePort = 12002

send_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket.bind((localHost, chatPortRecv))
send_socket.bind((localHost, chatPortSend))

username = input("Register your contact's name please: ")

nbFile = '2'
cntFile = 0

print()
print("Welcome to the chat room, " + username + "!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room")
print()

def fileReceive(fileName):
    """
    Function to receive a file from the sender
    connected to the filePort over TCP
    receive the file as chunks of 1024 bytes
    """
    global cntFile
    cntFile += 1
    recieverSocket = socket(AF_INET,SOCK_STREAM)
    recieverSocket.bind((destHost,filePort))
    recieverSocket.listen(5)

    file, clientAddr = recieverSocket.accept()
    filename = f'received{nbFile}({cntFile})_{fileName}'
    fo = open(filename, "wb") 
    data = file.recv(1024)
    while data:
        fo.write(data)
        data = file.recv(1024)
    fo.close() 
    recieverSocket.close()
    

def fileSend(fileName):
    """
        Function to send a file to the receiver
        connected to the filePort over TCP
        send the file as chunks of 1024 bytes
    """
    senderSocket = socket(AF_INET, SOCK_STREAM)
    senderSocket.connect((destHost, filePort))
    fi = open(fileName, "rb") 
    data = fi.read(1024) 
    while data: 
        senderSocket.send(data) 
        data = fi.read(1024) 
    fi.close() 
    senderSocket.close()
    return

def Receive():
    """
        Function to receive messages from the sender
        connected to the chatPortRecv over UDP
        receive the message as chunks of 1024 bytes
        extract the sequence number and message content
        send an ACK with the sequence number
        print the message content
    """
    seq_num = 0
    while True:
        try:
            message, addr = recv_socket.recvfrom(1024)
            msg_seq_num, msg_content = message.decode().split(":", 1)
            if int(msg_seq_num) == seq_num:
                seq_num += 1
                recv_socket.sendto(f"ACK:{msg_seq_num}".encode(), addr)
                if msg_content == 'exit':
                    print(f"{msg_content} received")
                    sys.exit()
                elif msg_content.endswith('FILE'):
                    print("a file is being received")
                else :
                    print(msg_content)
            else:
                recv_socket.sendto(f"ACK:{msg_seq_num}".encode(), addr)
                print(f"Received out of order: {msg_content}") 

        except Exception as e:
            print(message.decode())
            print("Error1:", e, file=sys.stderr)

def Send():
    """
        Function to send messages to the receiver
        connected to the chatPortSend over UDP
        send the message as chunks of 1024 bytes
        extract the sequence number and message content
        wait for an ACK with the sequence number
        print the message content
        To send a file, the user must type 'FILE'
        the user will be prompted to input the filename
        the file will be sent using the fileSend function
    """
    ack_num = 0
    while True:
        message = input()
        if message == 'exit':
            send_socket.sendto((username + " has left the chat room").encode(), (destHost, chatPortSend))
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

        CHUNK_SIZE = 1024 
        message_chunks = [message[i:i+CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]

        for chunk in message_chunks:
            print(f"Sending chunk with seq_num {ack_num}: {chunk}")
            acknowledged = False
            while not acknowledged:
                send_socket.settimeout(5)  # Timeout after 5 seconds
                send_socket.sendto(f"{ack_num}:{username}: {chunk}".encode(), (destHost, chatPortSend))                
                try:
                    ack_msg, addr = send_socket.recvfrom(1024)  # Wait for ACK
                    ack_seq_num = ack_msg.decode().split(':')[1]
                    if int(ack_seq_num) == ack_num:
                        acknowledged = True
                        ack_num += 1
                except timeout:
                    print("No ACK received for chunk. Resending chunk.", file=sys.stderr)
                except Exception as e:
                    print("Error2:", e, file=sys.stderr)
                finally:
                    send_socket.settimeout(None)
                    if acknowledged:
                            print(f"Chunk with seq_num {ack_num} acknowledged.")
                    else:
                        print(f"Resending chunk with seq_num {ack_num} due to timeout.")

t1 = Thread(target=Receive)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()
