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