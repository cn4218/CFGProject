"""MOST OF THIS IS NIKITAS CODE BUT I JUST MADE A FEW CHANGES SO IT ALL RUNS SMOOTHLY!!!"""
import mysql.connector
from mysql.connector import Error
from config import USER, PASSWORD, HOST


# not sure if we need to turn this a class and use OOP - just leaving here for now, do this later!
# #

class DbConnectionError(Exception):
    pass

def _create_db_connection(db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host= HOST,
            user= USER,
            password= PASSWORD,
#
            database=db_name,
        )
        print("MySQL Database Connection is Successful")
    except Error as er:
        print(f"Error: '{er}'")
    return connection

result = _create_db_connection("CFG_Project")
print(result)
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


    # return info for one user using their name  - can change to user ID if better?
def _get_user(User_ID):
    user = {}
    try:
        db_name = "CFG_Project"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT * FROM User_Info 
        WHERE User_ID = '{}'""".format(User_ID)

        cur.execute(query)

        result = (cur.fetchall())
        user = _add_values(result)
        cur.close()
    except Exception as err:
        print(err)
        raise Error("Failed to get data from Database", err)
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection is closed")
    return user


def add_user(User_Name, Name_User, Email_Address):
    try:
        db_name = "CFG_Project"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            INSERT INTO user_info (User_Name, Name_User, Email_Address) VALUES ( %s, %s, %s) """
        record = (User_Name, Name_User, Email_Address)
        cur.execute(query, record)
        db_connection.commit()
        print("User has been successfully inserted to user_info table")

    except mysql.connector.Error as err:
        print("Failed to insert data into MySQL table {}".format(err))

    finally:
        if db_connection:
            db_connection.close()
            print("MySQL connection is closed")


# also added except errors but i've done them in 3 different ways
# - wanted advise on what the best way to handle the error is?

#  not sure if this is needed but adding here just in case?
#
def delete_user(User_ID):
    try:
        users = {}
        db_name = "CFG_Project"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        dict = _get_user(User_ID)
        user_name = dict[0]['User_Name']
        print("Connected to DB: %s" % db_name)

        query = """
        DELETE FROM user_info WHERE user_id = {} """.format(User_ID)

        cur.execute(query)
        db_connection.commit()

        answer = "Account successfully deleted for username {}".format(user_name)
        cur.close()
    except Exception as err:
        answer = "Unsuccessful deleting account for username {}".format(user_name)
        raise DbConnectionError("Failed to read data from Database", err)
    finally:
        if db_connection:
            db_connection.close()
    return answer


# in case a user wants to update their user_name - not sure this works or if it's right, will need to fix!
# also this is not necessary just thought it would be good to add? Ignore if needed
def update_user(User_ID, Old_User_Name, New_User_Name):
    result = False
    try:
        db_name = "CFG_Project"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        cur.execute("""SELECT user_name FROM user_info WHERE user_id = {}""".format(User_ID))
        result = cur.fetchall()
        old_user = cur.fetchone()
        old_user_check = result[0][0]
        if Old_User_Name == old_user_check:
            cur.execute("""UPDATE user_info SET user_name = '{}' WHERE user_id = {}""".format(New_User_Name, User_ID))
            db_connection.commit()
            result = True
        else:
            print("The current user_name is incorrect")
            result = False
    except Exception as err:
        raise DbConnectionError("Failed to read data from Database", err)
    finally:
        if db_connection:
            db_connection.close()
            cur.close()
    return result

# result = update_user(1,'fang123','fang12')

def verify_login(username,name_user, email_address):
    try: 
        db_name = 'CFG_Project'
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            SELECT *
            FROM User_Info
            WHERE User_Name = '{}'
            and Name_User = '{}' and Email_Address = '{}'""".format(username,name_user,email_address)

        cur.execute(query)

        result = (
            cur.fetchall()
        )
        print(result)
        rowcount = len(result)

        if rowcount == 0:
            answer = False
        elif rowcount == 1:
            answer = True
        elif rowcount>1:
            answer = 'Duplicate users'

        cur.close()
        return answer

    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def get_user_id(username,name,email):
    try:
        db_name = "CFG_Project"
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)
        # 
        cur.execute("""SELECT user_id FROM user_info 
        WHERE user_name = '{}' and name_user = '{}' and email_address = '{}'""".format(username,name,email))
        result = cur.fetchall()
        number_users = len(result)
        if number_users == 1:
            userid = result[0][0]
            answer = userid
        elif number_users == 0:
            print('User not found')
            answer = False
        else:
            print("Issue finding unique user id")
            answer = False
        cur.close()
        return answer

    except Exception as err:
        raise DbConnectionError("Failed to read data from Database", err)
    finally:
        if db_connection:
            db_connection.close()
            cur.close()

