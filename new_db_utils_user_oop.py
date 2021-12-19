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


    def add_user(self, user_id, user_name, name_user, email_address):
        try:
            self.conn()
            cur = self.db.cursor()

            record = (user_id, user_name, name_user, email_address)
            cur.execute("INSERT INTO user_info (User_ID, User_Name, Name_User, Email_Address) VALUES (%s, %s, %s, %s)", record)
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
            cur.execute("SELECT * FROM user_info WHERE user_id = %s" % user_id)
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



    #  new update func
    def update_user_name(self, user_id, old_user_name, new_user_name):
        result = False
        try:
            cur = self.db.cursor()
            cur.execute("""SELECT user_name FROM user_info WHERE user_id=%s""" % user_id)
            user = cur.fetchone()
            print(user)
            if user[0] == old_user_name:
                cur.execute("""UPDATE user_info SET user_name= '%s' WHERE user_id=%s""" %(new_user_name, user_id))
                self.db.commit()
                result = True
            else:
                print("The current username is incorrect")
                result = False
        except Error as err:
            raise Error("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
        return result


    #  email update
    def update_user_email(self, user_id, old_email, new_email):
        result = False
        try:
            cur = self.db.cursor()
            cur.execute("""SELECT email_address FROM user_info WHERE user_id=%s""" % user_id)
            email = cur.fetchone()
            print(email)
            if email[0] == old_email:
                cur.execute("""UPDATE user_info SET email_address= '%s' WHERE user_id=%s""" % (new_email, user_id))
                self.db.commit()
                result = True
            else:
                print("The current email address is incorrect")
                result = False
        except Error as err:
            raise Error("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
        return result


    # function to change name if we want to use?
    def update_name(self, user_id, old_name, new_name):
        result = False
        try:
            cur = self.db.cursor()
            cur.execute("""SELECT name_user FROM user_info WHERE user_id=%s""" % user_id)
            name = cur.fetchone()
            print(name)
            if name[0] == old_name:
                cur.execute("""UPDATE user_info SET name_user= '%s' WHERE user_id=%s""" % (new_name, user_id))
                self.db.commit()
                result = True
            else:
                print("The current name is incorrect")
                result = False
        except Error as err:
            raise Error("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
        return result

    # had to redo this code in order for it to work just leaving old one here - couldn't figure out how to make this work
    # def delete_user(self, user_id):
    #     try:
    #         users = {}
    #         cur = self.db.cursor()
    #         dict = self._get_user(user_id)
    #         user_name = dict[0]['User_Name']
    #         cur.execute("DELETE FROM user_info WHERE user_id =%s ;""" %(user_id))
    #         self.db.commit()
    #         answer = "Account successfully deleted for username {}".format(user_name)
    #         cur.close()
    #     except Error as err:
    #         answer = ("Unsuccessful deleting account for username {}".format(user_name))
    #         print("Failed to read data from Database", err)
    #     finally:
    #         if self.conn:
    #             self.db.close()
    #             print("MySQL connection is closed")
    #     return answer

    # new delete - seems to work
    def delete_user(self, user_id):
        try:
            cur = self.db.cursor()
            cur.execute("""DELETE FROM user_info WHERE user_id =%s """ % user_id)
            self.db.commit()
            rows = cur.fetchall()
            if user_id not in rows:
                answer = print("Account successfully deleted for user with id {}".format(user_id))
            else:
                answer = print("Unsuccessful deleting account for user with id {}".format(user_id))
            cur.close()
        except Error as err:
            print("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")
        return answer



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
        except Error as err:
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
# c.add_user('1', 'ki123', 'nikita', 'k1@mail.com')
# c._get_user('1')
# c.update_user_name('3', 'ki123','nik12')
# c.update_user_email('1', 'nik@mail.com', 'niki"mail.com')
# c.delete_user('1')
# c.verify_login('2', 'niki123', 'nikita', 'nik1@mail.com')
# c.get_user_id('nik12', 'nikita', 'k1@mail.com')