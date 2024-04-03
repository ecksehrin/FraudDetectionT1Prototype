pip install pymysql
import pymysql

events = pymysql.connect(
    host='frauddetectiont1.database.windows.net',
    user='team1',
    password='T1frauddetection',
    db='FraudDetectionDatabase',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

  try:
    with events.cursor() as cursor:
        # Read data from database
        sql = "SELECT * FROM `Events`"
        cursor.execute(sql)

        # Fetch all rows
        rows = cursor.fetchall()

        # Print results
        for row in rows:
            print(row)
finally:
    events.close()
