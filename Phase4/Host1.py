import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from threading import Thread
import socket
import sys
import os

# Host IPs
localHost = '127.0.0.1'
destHost = '127.0.0.2'

chatPortSend = 12000
chatPortRecv = 12001
filePort = 12002

# Socket setup, first for sending messages and receiving ACK, second for receiving messages and sending ACK
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind((localHost, chatPortRecv))
send_socket.bind((localHost, chatPortSend))

username = simpledialog.askstring("Username", "Register your contact's name please:")

nbFile = '1'
cntFile = 0
ack_num = 0 # Sequence number for the messages


# Networking functions
def fileReceive(fileName, update_chat_window):
    """ Function to receive a file from the sender connected to the filePort over TCP 
    receive the file as chunks of 1024 bytes """
    global cntFile
    cntFile += 1
    recieverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recieverSocket.bind((destHost, filePort))
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
    print("File received by Host2!")

def fileSend(fileName):
    """ Function to send a file to the receiver connected to the filePort over TCP"""
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((destHost, filePort))
    fi = open(fileName, "rb")
    data = fi.read(1024)
    while data:
        senderSocket.send(data)
        data = fi.read(1024)
    fi.close()
    senderSocket.close()
    print("File sent!")

def Receive(update_chat_window):
    """ Function to receive messages from the sender"""
    seq_num = 0 # Sequence number for the messages expected to be received
    while True:
        try:
            message, addr = recv_socket.recvfrom(1024)
            msg_seq_num, msg_content = message.decode().split(":", 1)
            if int(msg_seq_num) == seq_num:
                seq_num += 1
                recv_socket.sendto(f"ACK:{msg_seq_num}".encode(), addr)
                if msg_content == 'exit':
                    update_chat_window(f"{msg_content} received")
                    sys.exit()
                elif msg_content.endswith('FILE'):
                    update_chat_window("File received")
                else:
                    update_chat_window(msg_content)
            else:
                # I always send an ACK, even if the message is out of order 
                # so the sender knows it was received and can move on
                recv_socket.sendto(f"ACK:{msg_seq_num}".encode(), addr)
                print(f"Received out of order: {msg_content}")

        except Exception as e:
            print("Error1: " + str(e))

def Send(message):
    global ack_num
    if message == 'exit':
        send_socket.sendto((username + " has left the chat room").encode(), (destHost, chatPortSend))
        sys.exit()        

    CHUNK_SIZE = 1024 # Chunk size for the messages
    message_chunks = [message[i:i+CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]

    for chunk in message_chunks:
        acknowledged = False
        # Keep sending the message until an ACK is received
        while not acknowledged:
            send_socket.settimeout(5)  # Timeout after 5 seconds
            send_socket.sendto(f"{ack_num}:{username}: {chunk}".encode(), (destHost, chatPortSend))
            try:
                ack_msg, addr = send_socket.recvfrom(1024)  # Wait for ACK
                ack_seq_num = ack_msg.decode().split(':')[1]
                # If the ACK sequence number matches the message sequence number, the message was received
                if int(ack_seq_num) == ack_num:
                    acknowledged = True
                    ack_num += 1
            except socket.timeout:
                print("No ACK received for chunk. Resending chunk.")
            except Exception as e:
                print("Error2:", e)
            finally:
                send_socket.settimeout(None)
# GUI part
class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("UDP/TCP Chat App1")
        # GUI elements for the chat window and message entry
        self.text_area = tk.Text(master, state='disabled', height=15, width=50)
        self.text_area.pack(padx=20, pady=10)
        # Entry field for the message to be sent
        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.pack(padx=20, pady=10)
        # Buttons for sending messages and attaching files
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        # Button to attach a file
        self.file_button = tk.Button(master, text="Attach File", command=self.attach_file)
        self.file_button.pack(side=tk.RIGHT, padx=(10, 20), pady=10)
        # Start the receive thread
        self.recv_thread = Thread(target=self.receive)
        self.recv_thread.daemon = True
        self.recv_thread.start()

    def send_message(self):
        """ Function to send a message to the receiver"""
        message = self.msg_entry.get()
        if message:
            self.update_chat_window(f"You: {message}")
            self.msg_entry.delete(0, tk.END)
            Send(message)

    def attach_file(self):
        """ Function to attach a file to the chat window"""
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)  # Extract the filename from the full path
            f1 = Thread(target=fileReceive, args=(filename, self.update_chat_window))
            f2 = Thread(target=fileSend, args=(filename,))
            f1.start()
            # add a small delay to ensure the receiver is ready to receive the file
            for i in range(100):
                pass
            f2.start()
            self.update_chat_window(f"File sent: {filename}")
            Send("FILE")
            print("File sent!")            

    def update_chat_window(self, message):
        # Function to update the chat window with the messages
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def receive(self):
        # Function to receive messages from the sender
        Receive(self.update_chat_window)

    def on_closing(self):
        # Function to handle the closing of the chat window
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            send_socket.sendto((username + " has left the chat room").encode(), (destHost, chatPortSend))
            self.master.destroy()

# Running the GUI
root = tk.Tk()
app = ChatApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
