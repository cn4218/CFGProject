import mysql.connector
from mysql.connector import Error
from config import USER, PASSWORD, HOST


# not sure if we need to turn this a class and use OOP - just leaving here for now, do this later!
# #
# class _dbconnectionerror():
#     pass

def _create_db_connection(db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host= HOST,
            user= USER,
            password= PASSWORD,
            auth_plugin='my_sql_native_password',
            database=db_name
        )
        print("MySQL Database Connection is Successful")
    except Error as er:
        print(f"Error: '{er}'")
    return connection


    # should add the values a user enters into our db
    # don't know if this is needed tbh ? - followed lesson 20
def _add_values(user_account):
    mapped = []
    for item in user_account:
        mapped.append({
            "User_ID" : item[0],
            "Name_User" : item[1],
            "Email_Address" : item[2]
        })
    return mapped


    # return info for one user using their name  - can change to user ID if better?
def _get_user(name_user):
    user = {}
    try:
        db_name = "user_info"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """ SELECT * FROM user_info 
         WHERE name_user = '{}'""".format(name_user)

        cur.execute(query)

        result = (cur.fetchall())
        user = _add_values(result)
        cur.close()
    except Exception:
        raise Error("Failed to get data from Database")
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return user


    # insert user info into sql table
def add_user(User_ID, Name_User, Email_Address):
    try:
        db_name = "user_info"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            INSERT INTO user_info (User_ID, Name_User, Email_Address) VALUES (%s, %s, %s) """
        record = (User_ID, Name_User, Email_Address)
        cur.execute(query, record)
        db_connection.commit()
        print("User has been successfully inserted to user_info table")

    except db_connection.Error as err:
        print("Failed to insert data into MySQL table {}".format(err))

    finally:
        if db_connection:
            db_connection.close()
            print("MySQL connection is closed")

# also added except errors but i've done them in 3 different ways
# - wanted advise on what the best way to handle the error is?








