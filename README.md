Project 12 - EpicEvents
-
As part of the OpenClassroom "Python Application Developer" training program, this project is a CLI (Command Line Interface) application that helps with the management of clients, contracts, and events

Prerequisites :
-
Ensure to have the following installed on your system :

* Python 3.10 or higher
* MySQL
* Sentry

Installation (windows)
-
In a terminal, clone this repository using :

    git clone https://github.com/Chillihache/Projet12v2.git

Create a database in MySQL and a project in Sentry.

Copy the ".env.sample" file.

Rename your copy ".env"

Complete the informations in ".env".

Create a virtual environnement:

    python -m venv env

Activate the virtual environment :

    env\Scripts\activate.bat

Install dependencies :

    pip install -r requirements.txt

To set up the data base and create a superuser :

    python init.py

Then, you can see all commands :

    python epicevents.py

To use a command :

    python epicevents.py [command_name]


