# Python Generators – Task 0: Database Setup with Seed Script

This task involves setting up a MySQL database and populating it using a Python script to simulate streaming data processing using generators later in the project.

## 🧩 Objective

* Create and connect to a MySQL database named `ALX_prodev`.
* Create a `user_data` table to store sample user information.
* Load user data from a CSV file (`user_data.csv`) into the database.
* Prepare the data infrastructure for later generator-based streaming tasks.

---

## 📁 Files

| File Name       | Description                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------- |
| `seed.py`       | Contains functions to connect to MySQL, create database and tables, and insert data from CSV |
| `user_data.csv` | Sample CSV file containing user records (UUID, name, email, age)                             |
| `0-main.py`     | Test script provided to validate the implementation                                          |

---

## ⚙️ Functions Implemented

### `connect_db()`

Connects to the MySQL server using root credentials.

### `create_database(connection)`

Creates a new database `ALX_prodev` if it doesn't already exist.

### `connect_to_prodev()`

Establishes connection specifically to the `ALX_prodev` database.

### `create_table(connection)`

Creates the `user_data` table with the following schema:

* `user_id` (UUID, Primary Key, Indexed)
* `name` (string)
* `email` (string)
* `age` (decimal)

### `insert_data(connection, csv_file)`

Reads from the `user_data.csv` file and inserts the data into the `user_data` table if not already present.

---

## ✅ Expected Output (via `0-main.py`)

```bash
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), 
 ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), 
 ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), 
 ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), 
 ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]
```

