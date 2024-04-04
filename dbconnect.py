#Code taken from Tech with Hitch, https://www.youtube.com/watch?v=BgkcKCvuCMM

#Importing ODBC and Pandas packages, pip install pyodbc and pandas in Windows console
import pyodbc
import pandas as pd

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

#Execute SQL to read all items from Events
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

