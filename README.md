# FraudDetectionT1Prototype
This prototype allows the user to test the functions and prevent possible fraudulent attacks. 

The code can directly connect to a database set up in SQL Server hosted on Azure, and can send API calls to email and text systems.

# Interactions
The prototype launches a menu that includes multiple functions.

    1) Print the Current Event Table
    
    2) Insert an Event Manually
    
    3) Simulate 5 Incorrect Logins
    
    4) Check for Login Activity
    
    5) Check for Transactions Activicty
    
    6) Check TOR Nodes
    
    7) Email Test
    
    8) Text Test
    
    

Data, including suspicious activity, is already included in the database. More data does not need to be added to make alerts trigger.

# Rules
The 3 possibilities for activity scanning: incorrect logins, large transactions, blacklisted TOR nodes, are as follows:

5 or more incorrect logins from the same IP address.

Any payment transaction that is $500.00 USD or more.

Any IP address that matches a blacklisted TOR node.
