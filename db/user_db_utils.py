import mysql.connector
from mysql.connector import Error
from config import user_name, user_password, host_name

### sql alchemy
## flask tutorial ; corey schafer

class DbConnectionError(Exception):
    pass

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

    # should add the values a user enters into our db
def _add_values(user_account):
    mapped = []
    for item in user_account:
        mapped.append({
            "User_ID" : item[0],
            "User_Name" : item[1],
            "Name_User" : item[2],
            "Email_Address" : item[3]
        })
    return mapped
# `User_ID` int NOT NULL UNIQUE AUTO_INCREMENT,
# `User_Name` varchar(50) NOT NULL,
# `Name_User` varchar(50) NOT NULL,
# `Email_Address

def verify_login(user_id,username,name_user, email_address):
    try: 
        db_name = 'user_info'
        db_connection = create_db_connection(host_name, user_name, user_password, db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            SELECT *
            FROM Wish_List
            WHERE User_ID = '{}' and User_Name = '{}'
            and Name_User = '{}' and Email_Address = '{}'""".format(user_id,username,name_user,email_address)

        cur.execute(query)

        result = (
            cur.fetchall()
        )
        rowcount = len(result)

        if rowcount == 0:
            answer = False
        else:
            answer = _add_values(result)

        cur.close()
        return answer

    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
