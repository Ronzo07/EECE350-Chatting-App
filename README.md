# EECE350-Chatting-App
This is a Network chatting application developed for the EECE350 course at the American University of Beirut. The application allows two users to communicate with each other over a network connection. UDP was used to send and receiv messages after adding some reliability on top of it, while TCP was used in order to send any type of files. Users can send text messages and files to each other using the graphical user interface (GUI).

# Running the Application:
To run the chatting application, follow these steps:

1. Clone or download the project repository to your local machine.
2. Navigate to the directory containing the project files (Phase4 contains the final version with GUI and Phase3 contains the terminal version). (cd Phase4 OR cd Phase3)
3. Open two terminal window.
4. Run the following command to execute the Python script:
python Host1.py
5. In the second terminal window, run the following command to execute the Python script:
python Host2.py

This commands will start the application, and the GUI will be displayed on your screen.

# Using the Application (Phase4):
Once the application is running, you will first enter your name and then you can use the GUI to send and receive messages and files. Here are some key features:

- Sending Messages: Type your message in the text entry field at the bottom of the GUI and press the "Send" button to send it.
- Sending Files: Click the "Attach File" button to select a file from your local machine and send it to the other peer.
- Receiving Messages and Files: Incoming messages and files will be displayed in the text area at the top of the GUI.

# Using the Application (Phase3):
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

# Specifications:
The project was developed using Python 3.10 and the following libraries:

- `socket`: Used to create the network connection between the two hosts.
- `tkinter`: Used to create the graphical user interface (GUI) for the chatting application.
- `threading`: Used to create multiple threads for sending and receiving messages and files.
- `os`: Used to interact with the operating system and send files.
- `time`: Used to add delays in the sending and receiving of messages and files.

# Authors:
This project was developed by a team of students at the American University of Beirut in the EECE350 course. The team members are:
Bahaa Ammoury,
Roni Bou Saab, and
Samah Ghoussaimy
