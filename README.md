# Project Description

The Simple Chat / Messaging Simulator is a Python desktop application built using Tkinter. It simulates a multi-session chat system where users can create and manage chat sessions. The project demonstrates essential software engineering principles through the use of design patterns.

The system uses:

Observer Pattern to update the GUI in real time.

Factory Pattern to dynamically create different types of messages.

Decorator Pattern to add timestamps and formatting to messages.

Singleton Pattern to ensure only one Chat Engine instance exists.

## Key Features:

Multi-session chat simulation

Auto-reply bot messages

Typing indicator animation

Search bar for sessions/messages

Notification badges (WhatsApp-like)

Online/last-seen status

Dark mode GUI

### How to Run the System
1. Clone the repository
git clone <your-repo-url>
cd Simple-Chat-Messaging-Simulator

2. Install dependencies
pip install -r requirements.txt


(Tkinter comes preinstalled with standard Python.)

3. Run the application
python ui/app.py

4. Usage

Click New to create a new chat session

Select a session to open the chat window

Type and send messages

Auto-reply bot responds automatically

Search bar filters messages and sessions

## Dependencies
This project requires the following software and libraries:

1. Python Version

Python 3.8 or higher
The system is developed and tested using modern Python versions.
You can verify your version using:

python --version

2. Tkinter (GUI Library)

Tkinter is included by default with most Python installations.

It is used for building the graphical user interface (GUI).

If Tkinter is missing, install it using:

Windows: Already included
Linux (Ubuntu):

sudo apt-get install python3-tk


Mac: Included by default

3. Standard Python Libraries

These libraries are built-in and require no installation:

datetime — handles timestamps for messages

threading — manages background tasks like typing indicators

time — used for delays (e.g., bot message delay)

You do not need to install these separately.

### Folder Structure


Simple_Chat_Messaging_Simulator/
- engine/  __init__.py ,builder.py, chat_engine.py ,session.py             
- messages/ __init__.py,base_message.py ,text_message.py, system_message.py, decorators.py ,factory.py         
- patterns/, __init__.py ,observer.py, singleton.py          
- ui/ __init__.py, gui.py ,app.py                
 README.md
 requirements.txt


## Known Issues

Auto-reply bot delay is fixed and not customizable

Search works only for text messages

Notification badges may update slowly with many sessions

Sessions and messages are not saved when the application closes
