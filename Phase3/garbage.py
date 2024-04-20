from socket import *
from threading import Thread
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Fixed secret key for AES encryption/decryption
# It should be 16, 24, or 32 bytes long (AES-128, AES-192, or AES-256)
secret_key = b'your_16_byte_key'

# Fixed IV for AES encryption/decryption
fixed_iv = b'your_16_byte_iv_'

def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

def decrypt_message(encrypted_message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode().strip()
    return decrypted_message

localHost = '127.0.0.1'
destHost = '127.0.0.2'
chatPort = 12000
filePort = 12001

hostSocket = socket(AF_INET, SOCK_DGRAM)
hostSocket.bind((localHost, chatPort))

username = input("Register your contact's name please: ")

nbFile = '_1_'

def fileReceive(fileName):
    recieverSocket = socket(AF_INET,SOCK_STREAM)
    recieverSocket.bind((destHost,filePort))
    recieverSocket.listen(5)

    file, clientAddr = recieverSocket.accept()
    filename = "received" + nbFile+fileName
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

print(f"\nWelcome to the chat room, {username}!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room\n")

def Receive():
    while True:
        try:
            encrypted_message, addr = hostSocket.recvfrom(chatPort)
            if encrypted_message:
                decrypted_message = decrypt_message(encrypted_message, secret_key, fixed_iv)
                
                # Process message
                if decrypted_message != "ACK" and not decrypted_message.endswith("FILE"):
                    print(decrypted_message)
                hostSocket.sendto("ACK".encode(), addr)
                if decrypted_message.endswith("FILE"):
                    print("File received!")
        except Exception as e:
            print("Error:", e)

def Send():
    while True:
        message = input()
        if message == 'exit':
            encrypted_message = encrypt_message(username + " has left the chat room", secret_key, fixed_iv)
            hostSocket.sendto(encrypted_message, (destHost, chatPort))
            sys.exit()
        elif message == 'FILE':
            # File sending logic here
            pass

        CHUNK_SIZE = 1024 - AES.block_size  # Adjusted for the IV
        message_chunks = [message[i:i+CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]

        for chunk in message_chunks:
            print("Sending chunk:", chunk)
            encrypted_chunk = encrypt_message(username + ": " + chunk, secret_key, fixed_iv)
            hostSocket.sendto(encrypted_chunk, (destHost, chatPort))
            acknowledged = False

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


from socket import *
from threading import Thread
import sys

localHost = '127.0.0.1'
destHost = '127.0.0.2'

chatPortSend = 12000
chatPortRecv = 12001
filePort = 12002

send_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket.bind((localHost, chatPortRecv))
send_socket.bind((localHost, chatPortSend))

username = input("Register your contact's name please: ")

nbFile = '1'
cntFile = 0

print()
print("Welcome to the chat room, " + username + "!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room")
print()

def fileReceive(fileName):
    global cntFile
    cntFile += 1
    recieverSocket = socket(AF_INET,SOCK_STREAM)
    recieverSocket.bind((destHost,filePort))
    recieverSocket.listen(5)

    file, clientAddr = recieverSocket.accept()
    filename = f'received{nbFile}({cntFile})_{fileName}'
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
    fi.close() 
    senderSocket.close()
    return

def Receive():
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
                print(f"Received out of order: {msg_content}") # I can neglect it as it will be resend

            # if message.decode() != "ACK" and (len(message.decode()) >= 4 and message.decode()[-4:] != "FILE"):  # Don't print ACK messages
            #     print(message.decode())

            # recv_socket.sendto("ACK".encode(), addr)  # Send ACK for all received messages
            # if len(message.decode()) >= 4 and message.decode()[-4:] == "FILE":
            #     print("File received!")

        except Exception as e:
            print(message.decode())
            print("Error1:", e)

def Send():
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

        
        CHUNK_SIZE = 1024  # 1KB per chunk
        message_chunks = [message[i:i+CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]

        for chunk in message_chunks:
            print(f"Sending chunk with seq_num {ack_num}: {chunk}")
            acknowledged = False
            print(ack_num)
            while not acknowledged:
                send_socket.settimeout(5)  # Timeout after 5 seconds
                send_socket.sendto(f"{ack_num}:{username}: {chunk}".encode(), (destHost, chatPortSend))                
                try:
                    ack_msg, addr = send_socket.recvfrom(1024)  # Wait for ACK
                    ack_seq_num = ack_msg.decode().split(':')[1]
                    if int(ack_seq_num) == ack_num:
                        acknowledged = True
                        ack_num += 1
                except socket.timeout:
                    print("No ACK received for chunk. Resending chunk.")
                except Exception as e:
                    print("Error2:", e)
                finally:
                    send_socket.settimeout(None)
                    if acknowledged:
                            print(f"Chunk with seq_num {ack_num} acknowledged.")
                    else:
                        print(f"Resending chunk with seq_num {ack_num} due to timeout.")        # hostSocket.settimeout(None)


t1 = Thread(target=Receive)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()


from socket import *
from threading import Thread
import sys

localHost = '127.0.0.1'
destHost = '127.0.0.2'

chatPortSend = 12000
chatPortRecv = 12001
filePort = 12002

send_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket.bind((localHost, chatPortRecv))
send_socket.bind((localHost, chatPortSend))

username = input("Register your contact's name please: ")

nbFile = '1'
cntFile = 0

print()
print("Welcome to the chat room, " + username + "!")
print("Type 'FILE' to send a file")
print("Type 'exit' to leave the chat room")
print()

def fileReceive(fileName):
    global cntFile
    cntFile += 1
    recieverSocket = socket(AF_INET,SOCK_STREAM)
    recieverSocket.bind((destHost,filePort))
    recieverSocket.listen(5)

    file, clientAddr = recieverSocket.accept()
    filename = f'received{nbFile}({cntFile})_{fileName}'
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
    fi.close() 
    senderSocket.close()
    return

def Receive():
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
                print(f"Received out of order: {msg_content}") 

        except Exception as e:
            print(message.decode())
            print("Error1:", e)

def Send():
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
            print(ack_num)
            while not acknowledged:
                send_socket.settimeout(5)  # Timeout after 5 seconds
                send_socket.sendto(f"{ack_num}:{username}: {chunk}".encode(), (destHost, chatPortSend))                
                try:
                    ack_msg, addr = send_socket.recvfrom(1024)  # Wait for ACK
                    ack_seq_num = ack_msg.decode().split(':')[1]
                    if int(ack_seq_num) == ack_num:
                        acknowledged = True
                        ack_num += 1
                except socket.timeout:
                    print("No ACK received for chunk. Resending chunk.")
                except Exception as e:
                    print("Error2:", e)
                finally:
                    send_socket.settimeout(None)
                    if acknowledged:
                            print(f"Chunk with seq_num {ack_num} acknowledged.")
                    else:
                        print(f"Resending chunk with seq_num {ack_num} due to timeout.")        # hostSocket.settimeout(None)


t1 = Thread(target=Receive)
t2 = Thread(target=Send)

t1.start()
t2.start()

t1.join()
t2.join()
