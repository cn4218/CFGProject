
import mysql.connector
from mysql.connector import Error

class dbConnection:
    def __init__(self,password,db_name="CFG_Project",tb_name="user_info",user='root',host='localhost'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.tb_name = tb_name
        self.conn()


    def conn(self):
        try:
            db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                db= self.db_name,
            )
            self.db = db
            print("MySQL Database Connection is Successful!!!")
        except Error as er:
            print("Error: '{}' ".format(er))

    def _add_values(self,user_account):
        mapped = []
        for item in user_account:
            mapped.append({
                "User_ID" : item[0],
                "User_Name" : item[1],
                "Name_User" : item[2],
                "Email_Address" : item[3]
            })
        return mapped

    def verify_login(self, username,emailaddress):

        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""
                SELECT *
                FROM User_Info
                WHERE User_Name = '{}'
                and Email_Address = '{}';""".format(username, emailaddress))

            result = cur.fetchall()
            print(result)
            rowcount = len(result)
            if rowcount == 0:  ## user doesnt exist
                answer = {"verify": False}
            elif rowcount == 1:  ##user exists
                user_id = result[0][0]
                answer = {"verify": True, "user_id": user_id}
            elif rowcount > 1:  ## duplicate users
                answer = 'Duplicate users'
            cur.close()
            print(answer)
            print('here i am')
            return answer

        except Exception as e:
            raise Error("Failed to read data from DB", e)
        finally:
            if self.conn:
                self.db.close()
                print("DB connection is closed")

    def add_user(self, user_name, name_user, email_address):
        """
        Function that firstly checks if email address has been given in a format containing '@' and '.' then verifies if a user account with username, name and email already exist. 
        If not, then the new user is added to the sql table, wherea user ID is given.
        Parameters
        -----------
        user_name: str
            username of user
        name_user: str
            name of user
        email_addres: str
            email of user

        Returns
        ---------
        Either:
        Issue: str
            if theres an issue addng new user, either:
                1. 'Your email address has NOT been given in the requested format'
                2. 'User details already exist, try again with a new username'
        OR:
        True: bool
            if user is successfully added

        """
        try:
            if '@' not in email_address or '.' not in email_address:
                issue = 'Your email address has NOT been given in the requested format'    ### raises issue if email doesnt have @ or . in thr string
                return issue
            answer = self.verify_login(user_name,email_address)
            if answer['verify']== False:
                self.conn()
                cur = self.db.cursor()

                record = (user_name, name_user, email_address)
                cur.execute("INSERT INTO user_info (User_Name, Name_User, Email_Address) VALUES (%s, %s, %s)", record)
                self.db.commit()
                print("User has been successfully inserted to user_info table")
                return True
            elif answer['verify']==True:
                issue = 'User details already exist, try again with a new username'
                print(issue)
                return issue
        except Error as err:
            err = str(err)
            print("Failed to insert data into MySQL table '{}'", err)
            return err
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
            result = self._add_values(result)
            cur.close()
        except Error as err:
            print("Failed to get data from Database", err)
        finally:
            if self.conn:
                self.db.close()
                print("Database connection is closed")
        return result





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


    # new delete - seems to work
    def delete_user(self, user_id):
        """
        Function that deletes user from sql table
        Parameters
        -----------
        user_id: int
            id of user
        Returns
        -------
        answer: str
            Either:
            1. "Account successfully deleted for username {}".format(user_name)
            2. "Unsuccessful deleting account for username {},{}".format(user_name,err)
            3. 'No entry in database corresponding to given user ID: {}'.format(user_id)
        """
        try:

            dict = self._get_user(user_id)
            if len(dict) == 0:
                raise UnboundLocalError

            user_name = dict[0]['User_Name']
            self.conn()
            cur = self.db.cursor()

            cur.execute("""DELETE FROM user_info WHERE user_id = {}""" .format(user_id))

            self.db.commit()
            answer = "Account successfully deleted for username {}".format(user_name)
            cur.close()

    
        except UnboundLocalError as err:
            return 'No entry in database corresponding to given user ID: {}'.format(user_id)
        except Error as err:
            print("Failed to read data from Database", err)
            answer = err
        except Exception as err:
            answer = "Unsuccessful deleting account for username {},{}".format(user_name,err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")
        return answer




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

 #had to change because I was getting syntax errors 



cd = dbConnection('blu3bottl3')
result = cd.verify_login('Ayesha11','ayesha@live.com')
