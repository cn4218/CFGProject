import mysql.connector
from mysql.connector import Error

class dbConnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "skittle1"
        self.db_name = "CFG_Project"
        self.tb_name = "user_info"
        self.conn()


    def add_user(self, user_id):
        try:
            self.conn()
            print('Enter your username: ')
            user_name = input()
            print('Enter your name: ')
            name_user = input()
            print('Enter your email address: ')
            email_address = input()

            cur = self.db.cursor()

            record = (user_id, user_name, name_user, email_address)
            cur.execute("INSERT INTO user_info (User_ID, User_Name, Name_User, Email_Address) VALUES (%s, %s, %s, %s);", record)
            self.db.commit()
            print("User has been successfully inserted to user_info table")
        except Error as err:
            print("Failed to insert data into MySQL table '{}'", err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")


    def _get_user(self, user_id):
        user = {}
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("SELECT * FROM user_info WHERE user_id = '{}';".format(user_id))
            result = (cur.fetchall())
            for x in result:
                print(x)
            cur.close()
        except Error as err:
            print("Failed to get data from Database", err)
        finally:
            if self.conn:
                self.db.close()
                print("Database connection is closed")
        return user

    #  leaving old update here - doesn't seem to work need to figure it out
    # def update_user(self, User_ID, Old_User_Name, New_User_Name):
    #     result = False
    #     try:
    #         self.conn()
    #         cur = self.db.cursor()
    #
    #         cur.execute(""" SELECT user_name FROM user_info WHERE user_id= {}""".format(User_ID))
    #         result = cur.fetchall()
    #         old_user = cur.fetchone()
    #         old_user_check = result[0][0]
    #         if Old_User_Name == old_user_check:
    #             cur.execute("""UPDATE user_info SET user_name=%s WHERE user_id={}""".format(New_User_Name, User_ID))
    #             self.db.commit()
    #             result = True
    #             cur.close()
    #         else:
    #             print("The current user_name is incorrect")
    #             result = False
    #     except Error as err:
    #         raise Error("Failed to read data from Database", err)
    #     finally:
    #         if self.conn:
    #             self.db.close()
    #     return result



    #  new update function

    def update_user(self):
        try:
            print('Search User by id: ')
            id = input()

            print('Edit Username: ')
            username = input()

            if username == " ":
                print("Please do not leave username blank. Doing so will update the value to empty")
            cur = self.db.cursor()

            cur.execute("UPDATE user_info SET User_Name= %s WHERE user_id = %s;", (username, id))
            self.db.commit()
        except Error as err:
            print("Failed to update data into MySQL table", err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")


    #  for some reason this function will not work ?
    def delete_user(self):
        try:
            print("Search by id to delete user: ")
            id = input()
            cur = self.db.cursor()
            cur.execute("DELETE FROM user_info WHERE user_id =%s ;""", (id))
            self.db.commit()
            cur.close()
        except Error as err:
            print("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")

    def verify_login(self, user_id, username, name_user, email_address):
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""
                SELECT *
                FROM User_Info
                WHERE User_ID = '{}' and User_Name = '{}'
                and Name_User = '{}' and Email_Address = '{}';""".format(user_id, username, name_user, email_address))

            result = cur.fetchall()
            print(result)
            rowcount = len(result)
            if rowcount == 0:
                answer = False
            else:
                answer = True
            cur.close()
            return answer

        except Exception as e:
            raise Error("Failed to read data from DB", e)
        finally:
            if self.conn:
                self.db.close()
                print("DB connection is closed")


    # if the username/ name/ email don't match it returns the second elif statement and may be good to have a print to get the user's info back from the id
    def get_user_id(self, username, name, email):
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""SELECT user_id FROM user_info 
            WHERE user_name = '{}' and name_user = '{}' and email_address = '{}';""".format(username, name, email))
            result = cur.fetchall()
            number_users = len(result)
            if number_users == 1:
                userid = result[0][0]
                answer = userid
                print(answer, username, name, email)
            elif number_users == 0:
                print('There are no users with the same user info')
                answer = False
            else:
                print("Issue finding unique user id")
                answer = False
            cur.close()
            return answer
        except Exception as err:
            raise Error("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()

    def conn(self):
        db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db= self.db_name,
        )
        self.db = db


c = dbConnection()
# c.add_user('1')
# c._get_user('1')
# c.update_user()
c.delete_user()
# c.verify_login('2', 'niki123', 'nikita', 'nik@mail.com')
# c.get_user_id('niki123', 'kit', 'kit@mail.com')