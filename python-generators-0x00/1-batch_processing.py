import mysql.connector

def stream_users_in_batches(batch_size):
    offset = 0
    while True:
        users = fetch_batch(batch_size, offset)
        if not users:
            break
        yield users
        offset += batch_size

def fetch_batch(batch_size, offset):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="moha123",  # Replace with your actual MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
