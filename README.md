# EECE350-Chatting-App
This is a Network chatting application developed for the EECE350 course. The application allows two users to communicate with each other over a network connection. UDP was used to send and receiev messages after adding some reliability on top of it, while TCP was used in order to send all type of files.

# Simple test of the application:
Add network traffic
```bash
sudo tc qdisc add dev lo root netem delay 100ms 1000ms distribution normal loss 10% 25% reorder 25% 50% (delay, loss and reorder)
```
Run the following commands in two different terminals to start the chatting application:
```bash
cd Phase4
python Host1.py
```
```bash
cd Phase4
python Host2.py
```
Remove network traffic
```bash
sudo tc qdisc del dev lo root
```
You first need to enter your name, then you can start sending messages and files. 

# Specifications:
Python 3.10 is required to run the application and corrsponding library are listed below.
To install the required libraries, run the following command:
```
pip install socket tkinter threading os time tk sys
```

# Running the Application:
To run the chatting application, follow these steps:

1. Clone or download the project repository to your local machine.
2. Navigate to the directory containing the project files (Phase4 contains the final version with GUI and Phase3 contains the terminal version).:
3. Open two terminal window.
4. Run the following command to execute the Python script:
python Host1.py
5. In the second terminal window, run the following command to execute the Python script:
python Host2.py

This commands will start the application, and the GUI will be displayed on your screen.

# Using the Application GUI (Phase4):
Once the application is running, you will first enter your name and then you can use the GUI to send and receive messages and files. Here are some key features:

- Sending Messages: Type your message in the text entry field at the bottom of the GUI and press the "Send" button to send it.
- Sending Files: Click the "Attach File" button to select a file from your local machine and send it to the other peer.
- Receiving Messages and Files: Incoming messages will be displayed in the text area at the top of the GUI. Incoming files will be saved with the name Received1/2FileName.extension.

# Using the Application Terminal (Phase3):
Once the application is running, you will first enter your name and then you can use the terminal to send and receive messages and files. Here are some key features:

- Sending Messages: Type your message in the terminal and press the "Enter" key to send it.
- Sending Files: Type 'File' and the the file name in the terminal and press the "Enter" key to send it to the other peer.
- Receiving Messages and Files: Incoming messages and files will be displayed in the terminal.

# Project Structure:
The project is organized into the following directories and files:

- `Phase4/`: Contains the final version of the project with the GUI.
- `Phase3/`: Contains the terminal version of the project.
- `Phase2/`: Contains the second phase of the project.
- `Host1.py`: The Python script for the first host.
- `Host2.py`: The Python script for the second host.
- `README.md`: The project's main documentation file.

# Authors:
Roni Bou Saab, Bahaa Ammoury, and Samah Ghoussaimy