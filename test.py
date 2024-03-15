from hashlib import sha256
import csv

//Modified version of code taken from Daniel Afriyie, https://stackoverflow.com/questions/69301274/how-to-make-sign-up-and-login-program-in-python

//String of information, will be put into .csv with hashing later on
usernames = []
passwords = []
names = []

//Register function
def register():
    names.append(input("Enter your name:"))
    usernames.append(input("Enter your username:"))
    passwords.append(input("Enter your password:"))

//Logging in function
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")
    if username in usernames and password in passwords:
        print("Logged in successfully!")
    else:
        print("Invalid Login. Try again")

//Menu
while True:
    account_ans = input("1. Sign up        2. Login        3. Quit\ns")
    if account_ans == "1":
        register()
    if account_ans == "2":
        login()
    if account_ans == "3":
        break
