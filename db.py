import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kavya@123",
    database="lost_found"
)

cursor = db.cursor(buffered=True)