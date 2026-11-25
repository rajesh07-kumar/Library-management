import mysql.connector

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD"
    )

    print("Connected Successfully!")
    con.close()

except mysql.connector.Error as e:
    print("Error:", e)