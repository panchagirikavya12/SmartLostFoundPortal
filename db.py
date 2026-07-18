import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="lost_found"
)

cursor = db.cursor(buffered=True)
