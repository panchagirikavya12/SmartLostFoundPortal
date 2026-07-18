import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_MySql_Password",
    database="lost_found"
)

cursor = db.cursor(buffered=True)
