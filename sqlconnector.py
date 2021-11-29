import mysql.connector
from mysql.connector import Error

# ignore
# mydb = mysql.connector.connect(
#     user="root",
#     password="password",
#     host="127.0.0.1",
#     database="user_info"
#
# )

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password
        )
        print("MySQL Database Connection Successful")
    except Error as er:
        print(f"Error: '{er}'")
    return connection

# please change this to whatever the password is for your SQL workbench for it to work
pw = "password"

db_name = "user_info"

connection = create_server_connection("localhost", "root", pw)

# create database

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database has been created successfully")
    except Error as er:
        print(f"Error: '{er}'")

create_database_query = "Create database user_info"
create_database(connection, create_database_query)

# connect to database

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
        )
        print("MySQL Database Connection is Successful")
    except Error as er:
        print(f"Error: '{er}'")
    return connection

# sql query execution

def execute_sql_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query was successfully executed")
    except Error as er:
        print(f"Erorr: '{er}'")


create_user_info_table = """
CREATE TABLE IF NOT EXISTS `user_info`(
`user_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
`username` varchar(30) NOT NULL UNIQUE,
`first_name` varchar(50) NOT NULL,
`last_name` varchar(50) NOT NULL, 
`email` varchar(50) NOT NULL,
`password` varchar(50) NOT NULL);
"""

#  connect to the db

connection = create_db_connection("localhost", "root", pw, db_name)
execute_sql_query(connection, create_user_info_table)

# insert dummy data

user_data = """
INSERT INTO user_info values(
1, 'cosmogirl', 'nikita', 'patel', 'n.patel@somemail.com', 'makeup123');"""

connection = create_db_connection("localhost", "root", pw, db_name)
execute_sql_query(connection, user_data)

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as er:
        print(f"Error: '{er}'")

# using select to show records

query1 = """
select * from user_info;"""
connection = create_db_connection("localhost", "root", pw, db_name)
results = read_query(connection, query1)
for result in results:
    print(result)

# can add additional queries to display names/ usernames/ emails etc here - happy to add if needed