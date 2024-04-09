from hashlib import sha256
import csv

//Modified version of code taken from Daniel Afriyie, https://stackoverflow.com/questions/69301274/how-to-make-sign-up-and-login-program-in-python

//String of information will be put into .csv with hashing later on
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

def check_large_fund_transfers(transactions):
    large_transfers = []
    for transaction in transactions:
        if transaction['amount'] >= 500:
            large_transfers.append(transaction)
    return large_transfers

# Example usage:
transactions = [
    {'id': 1, 'amount': 300},
    {'id': 2, 'amount': 750},
    {'id': 3, 'amount': 200},
    {'id': 4, 'amount': 600}
]

large_transfers = check_large_fund_transfers(transactions)
print("Large fund transfers:")
for transaction in large_transfers:
    print(f"Transaction ID: {transaction['id']}, Amount: ${transaction['amount']}")
