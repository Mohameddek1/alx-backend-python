import mysql.connector

def stream_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="moha123",  # Replace with your MySQL root password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
