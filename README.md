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


Current alerts are sent to the creator's custom email and phone number. These items can be adjusted through the send_mail functions, phone and carrier variables.

For the send_email function, the send_to=None. The None value sends back to the team email. To setup another email user to receive the alerts, change the value from none to a string within a list. Example : send_to=['user@email.com']

For the text function, replace the phone variable with another number. The carriers supported are "att", "tmobile", "verizon", and"sprint". These strings reference a list with the appropite handle. As of now, this system gets flagged somehow, and limits our text alert functionality to once every couple hours. We believe  this is due to testing this function, using the phrase "test". We believe it triggered a spam filter that restricts our ability to send multiple texts.
