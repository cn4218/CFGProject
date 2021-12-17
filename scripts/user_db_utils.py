"""MOST OF THIS IS NIKITAS CODE BUT I JUST MADE A FEW CHANGES SO IT ALL RUNS SMOOTHLY!!!"""
import mysql.connector
from mysql.connector import Error
from config import USER, PASSWORD, HOST


# not sure if we need to turn this a class and use OOP - just leaving here for now, do this later!
# #

# Chizu: At the moment I am not sure if its the user id or the name_user I should use as a form of identification. Will ask nasian after 
# after I am done implementing functionality on the front end


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
        print("Error: '{}' ".format(er)) #had to change because I was getting syntax errors 
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

## returns list containing dictionary containing information for user, given the user_id 
## e.g. [
#   {
#     "Email_Address": "zita@gmail.com", 
#     "Name_User": "zita,", 
#     "User_ID": 2, 
#     "User_Name": "zitazee"
#   }
# ]
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

## adds user to database, returns none atm
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


## deletes user by user_id returns string describing if deleting user has been successful or not
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


## checks old user name and updates to a new one
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

# verifies if user exists in database, mainly useful for the main.py file and testing





def verify_login(username,email_address): #this needs to be restructured . the file needs an exception handler function
# if someone had a username like: marc'del, would it break this code?
    try: 
        db_name = 'CFG_Project'
        db_connection = _create_db_connection(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            SELECT *
            FROM User_Info
            WHERE User_Name = '{}'
            and Email_Address = '{}'
            """.format(username,email_address)

        cur.execute(query)

        result = (
            cur.fetchall()
        )
        print(result)
        rowcount = len(result)
        print(len(result))
        if rowcount:
            print(result[0][0]) #this will give you the user id 
            user_id = result[0][0]

        if rowcount == 0:   ## user doesnt exist
            answer = {"verify": False} #Chizu: I changed this 
        elif rowcount == 1:   ##user exists
            answer = {"verify": True, "user_id": user_id} #Chizu: I changed this as well because the front end needs the userID
        elif rowcount>1:  ## duplicate users
            answer = 'Duplicate users' #Chizu: If it is more than one, and it is duplicate users, what do we do on the front end? like do we let the user login or not ?

        cur.close()
        print(answer)
        return answer

    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")




 ## finds out user id given the username,name and email
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


if __name__ == '__main__':
    verify_login("sample_nambe","sample@gmail.com")
    
