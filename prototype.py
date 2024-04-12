#Importing ODBC for SQL intergration
import pyodbc

#Pandas packages for table printing
import pandas as pd

#Tkinter package for GUI
import tkinter as tk

from datetime import  datetime

#Gmail SMTP config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

#OS for file management
import os

#Text config
import sys

#ODBC Code partially taken from Tech with Hitch, https://www.youtube.com/watch?v=BgkcKCvuCMM
#Connection string including server information
cnxn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=frauddetectiont1.database.windows.net;'
    'DATABASE=FraudDetectionDatabase;'
    'UID=team1;'
    'PWD=T1frauddetection'
)

#pyodbc connect function to connect to SQL Database
conn = pyodbc.connect(cnxn_str)

#Create cursor to interact with database
cursor = conn.cursor()


# Execute SQL to read all items from Events
def print_events():
    cursor.execute("SELECT * FROM Events")
    #Fetchall to include all rows from table
    rows = cursor.fetchall()
    #Prints Rows
    print(rows)
    #Pandas function to read all rows from Events
    df = pd.read_sql("SELECT * FROM Events", conn)

    #Removed section that expanded on pandas printing options, changed to just use to_string
    #with pd.option_context('display.max_rows', None,
                           #'display.max_columns', None,
                           #'display.precision', 3,
                           #):

    # Prints Pandas version of table
    print(df.to_string())

    cursor.close()
    conn.close()

# Function to insert event into SQL Server table
def insert_event(username=None):
    try:
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()
        current_time = datetime.now()
        if username and username in valid_users:
            customer_id = valid_users[username]["customer_id"]
        else:
            #Sets default values to NULL if not used
            customer_id = None
            amt = None
            transtype = None
            rule = None
            action = input("Enter the number for the type of event: \n1) Successful Login\n2) Incorrect Login\n3) Transaction - Deposit\n4) Transaction - Withdraw/Payment\n")
            if '1' in action:
                event_description = 'Login_Correct'
                customer_id = int(input("Enter Customer ID, Ex. 1\n"))
            elif '2' in action:
                event_description = 'Login_Incorrect'
                rule = 2
            elif '3' in action:
                event_description = 'Transaction'
                transtype = 'Deposit'
                customer_id = int(input("Enter Customer ID, Ex. 1\n"))
                amt = float(input('Enter the amount of Deposit, in $\n$'))
                rule = 4
            elif '4' in action:
                event_description = 'Transaction'
                transtype = 'Withdrawal'
                customer_id = int(input("Enter Customer ID, Ex. 1\n"))
                amt = float(input('Enter the amount of Withdrawal or Payment, in $\n$'))
                rule = 3
            ip = input("Enter IP Address, Ex. 63.117.211.165\n")
            #Can enter NULL to get a NULL result
            if 'NULL' in ip:
                ip = None
            mac = input("Enter MAC Address, Ex. 08:00:27:9E:36:FB\n")
            if 'NULL' in mac:
                mac = None
            device_id = int(input("Enter Device ID, Ex. 1\n"))
            cursor.execute("INSERT INTO Events (Event_Description, Customer_ID, Date_Time, IP_Address, Mac_Address, Device_ID, Amount, Transaction_Type, Rule_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (event_description, customer_id, current_time, ip, mac, device_id, amt, transtype, rule))
            conn.commit()
    except pyodbc.Error as e:
        print(f"Error inserting event: {e}")
    finally:
        conn.close()

def login():
    username = username_entry.get()
    password = password_entry.get()
    # Check if username and password are correct
    if username in valid_users and valid_users[username]["password"] == password:
        result_label.config(text="Login successful")
        # Insert event into SQL Server table for successful login
        insert_event("Successful login", username)
    else:
        result_label.config(text="Invalid username or password")
        # Insert event into SQL Server table for failed login
        insert_event("Failed login attempt")

# Function to check any occurrences of rule 2
def check_incorrect_logins():
    df = pd.read_sql("SELECT IP_Address, COUNT(*) AS c FROM Events GROUP BY IP_Address, Rule_ID HAVING Rule_ID = '2' AND COUNT(*) >= 5;", conn)
    print(df.to_string())
    if len(df) != 0:
        print("Suspicious Activity Detected. Alerting Email, Security, AI Machine Learning System")
        send_mail(send_from=username,
                  subject="[Banking System] Alert - Suspicious Activity - Large Transaction",
                  text="Banking System Detected Large Transfer of Funds.",
                  send_to=None,
                  # File directory
                  files=[r"./large_transactions.csv"])
    else:
        print("No Suspicious Behavior Detected")

# Function to check any occurrences of rule 3
def check_large_transactions():
    df = pd.read_sql("SELECT * FROM Events WHERE Rule_ID = '3' AND Amount >= 500.00;", conn)
    #print(df.to_string())
    df.to_csv("large_transactions.csv")
    if len(df) != 0:
        print("Suspicious Activity Detected. Alerting Email, Security, AI Machine Learning System")
        send_mail(send_from=username,
                  subject="[Banking System] Alert - Suspicious Activity - Large Transaction",
                  text="Banking System Detected Large Transfer of Funds.",
                  send_to=None,
                  # File directory
                  files=[r"./large_transactions.csv"])
    else:
        print("No Suspicious Behavior Detected")


# Function to use SMTP to send an email to a device, code from https://stackoverflow.com/questions/3362600/how-to-send-email-attachments by Ferrarezi
def send_mail(send_from: str, subject: str, text: str,
send_to: list, files= None):

    send_to= default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(f) )
        msg.attach(attachedfile)


    smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

# Function to send text messages, Code from https://medium.com/testingonprod/how-to-send-text-messages-with-python-for-free-a7c92816e1a4
def send_text(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (username, password)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)

#send_mail and send_text connections
username = 't1frauddetection.17@gmail.com'
password = 'zyro pugd jncl tcqt'
default_address = ['t1frauddetection.17@gmail.com']

#send_text carriers handle
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}



#Menu for operation
ans=True
while ans:
    ans=input("""
    1) Print Event Table
    2) Insert an Event
    3) Simulate Incorrect Logins
    4) Check for Login
    5) Check for Transactions
    6) Quit
    7) Email Test
    8) Text Test
    9) File Check
    """)
    if '1' in ans:
        print_events()
    elif '2' in ans:
        insert_event()
    elif '3' in ans:
        #Needs to be implemented
    elif '4' in ans:
        check_incorrect_logins()
    elif '5' in ans:
        check_large_transactions()
    elif '6' in ans:
        ans = False
    elif '7' in ans:
        # Email test-Sends email from t1frauddetection.17 to itself with subject and text, optional file
        send_mail(send_from=username,
                  subject="[Banking System] Alert - Message",
                  text="Message system",
                  send_to=None,
                  #File directory
                  files=None)
    elif '8' in ans:
        send_text('6786002292', 'tmobile', 'Subject: Banking System\n\nSuspicious Activity Detected')
    elif '9' in ans:
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
    elif ans !="":
      print("\n Not Valid Choice Try again")
