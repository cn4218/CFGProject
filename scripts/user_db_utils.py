import mysql.connector
from mysql.connector import Error


class dbConnection:
    def __init__(self, password, db_name="CFG_Project", tb_name="user_info", user='root', host='localhost'):
        """
            This is a simple mysql connection class. The function is used to establish a connection to our SQL database.
            Parameters
            -----------
            password: str
                password for SQL workbench of user
            db_name: str
                name of database in SQL
            tb_name: str
                name of table in SQL
            user: str
                username of SQL workbench
            host: str
                host of SQL workbench
        """
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.tb_name = tb_name
        self.conn()

    def conn(self):
        """
            This function takes the arguments in __init__ class. And uses the arguments in it to make a connection to the SQL database.
            If the connection is successful the function will print "MySQL Database Connection is Successful!!!"
            Otherwise, it will raise an error.
        """
        try:
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db_name,
            )
            self.db = db
            print("MySQL Database Connection is Successful")

        except Error as er:
            print("Error: '{}' ".format(er))

    def _add_values(self, user_account):
        """
            This function takes the user_id, user_name, name_user and email_address and turns the output into
            a list of dictionaries.
            Parameters
            -----------
            user_id: int
                user id of user
            user_name: str
                username for user
            name_user: str
                name of user
            email_address: str
                email of user
            Returns
            ---------
            Returns mapped values
                List of dictionaries are returned with the user_account parameters
        """
        mapped = []
        for item in user_account:
            mapped.append({
                "User_ID": item[0],
                "User_Name": item[1],
                "Name_User": item[2],
                "Email_Address": item[3]
            })
        return mapped

    def verify_login(self, user_name, email_address):
        """
            This function is used to verify a user with the use of their username and email. This function will first check
            whether a user with a particular username & email address matches any records we have saved within our SQL database.
            If the function has a rowcount of 0 that means that no user with that username & email_address exists. If the function
            has a rowcount of 1 that means the user exists and if it's more than 1 then it means this is a duplicate entry.
            Parameters
            -----------
            username: str
                username of user
            email_address: str
                email of user
            Returns
            ---------
            Either:
                1. {"verify": False}
                    if the user doesn't exist, it will return a dict with the key 'verify' and False
                2. {"verify": True}
                    if the user does exist, the function will return the dict key 'verify' and True, with another dict containing the key 'user_id'
                    with the id number associated with that user
                3. Duplicate users
                    if the user's detail are already within th database the function will return that it's a duplicate user
        """
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""
                SELECT *
                FROM User_Info
                WHERE User_Name = '{}'
                and Email_Address = '{}';""".format(user_name, email_address))

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
            Function that firstly checks if email address has been given in a format containing '@' and '.' then verifies
            if a user account with username, name and email already exist. If not, then the new user is added to the sql
            table, where a user ID is given.
            Parameters
            -----------
            user_name: str
                username of user
            name_user: str
                name of user
            email_address: str
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
                issue = 'Your email address has NOT been given in the requested format'  ### raises issue if email doesnt have @ or . in thr string
                return issue
            answer = self.verify_login(user_name, email_address)
            if answer['verify'] == False:
                self.conn()
                cur = self.db.cursor()

                record = (user_name, name_user, email_address)
                cur.execute("INSERT INTO user_info (User_Name, Name_User, Email_Address) VALUES (%s, %s, %s)", record)
                self.db.commit()
                result = (cur.fetchall())
                user = self._add_values(result)
                print("User has been successfully inserted to user_info table")
                return True
            elif answer['verify'] == True:
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
        """
            This function is used get a particular user with a specified user_id from the SQL database.
            It with fetchall the users with the user_id that's being searched for and it will print the results
            and then use the add_values function to see if the user exists within the database.
            Parameters
            -----------
            user_id: int
                user id of user
            Returns
            ---------
            1. results
                the function will return all the information associated with a user
        """
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
        """
            This function is used to update a specific users username using their
            user_id to locate and update the user_name associated with the user. It
            takes in the id, old username & the new username they want to update to
            in order to change this within the SQL database. The function also checks whether
             the username retrieved from the SQL database matches the old username specified.
             If it does, then it will allow the user to update their username. Otherwise it will
             throw an error.
            Parameters
            -----------
            user_id: str
                user id of user
            old_user_name: str
                old username of user
            new_user_name: str
                new username the user wants
            Returns
            ---------
            Either:
                1. "The username has been updated"
                    returns result as True if the username is successfully updated and prints this statement
                2. "The current username is incorrect"
                    returns this statement if the old_user_name does not match with the record in SQL
                    and will not update the record for the specified user_id.
        """
        result = False
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""SELECT user_name FROM user_info WHERE user_id=%s""" % user_id)
            user = cur.fetchone()
    
            if user == None:
                return Exception('No user with corresonding userID')
            elif user[0] == old_user_name:
                # cur = self.db.cursor()
                # # cur = self.db.cursor()
                cur.execute("""UPDATE user_info SET user_name= '%s' WHERE user_id=%s""" % (new_user_name, user_id))
                self.db.commit()
                print("The username has been updated")
                result = True
            else:
                print("The current username is incorrect")
                result = False

        except Error as err:
            return Error("Failed to read data from Database", err)
        finally:
            if self.conn:
                self.db.close()
        return result

    #  email update
    def update_user_email(self, user_id, old_email, new_email):
        """
            This function is used to update a specific users email address using their
            user_id to locate and update the email_address associated with the user. It
             takes in the id, old email & the new email they want to update to,
             in order to change this within the SQL database. The function also checks whether
             the email address retrieved from the SQL database matches the old email specified.
             If it does, then it will allow the user to update their email. Otherwise it will
             throw an error.
             Parameters
             -----------
             user_id: str
                 user id of user
             old_email: str
                 old email of user
             new_email: str
                 new email the user wants
             Returns
             ---------
             Either:
                 1. "The email address has been updated"
                     returns result as True if the email address is successfully updated and prints this statement
                 2. "The current email address is incorrect"
                     returns result as False and this statement if the old email address does not match with the
                     record in SQL and will not update the record for the specified user_id.
        """
        result = False
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""SELECT email_address FROM user_info WHERE user_id=%s""" % user_id)
            email = cur.fetchone()
            print(email)
            if email[0] == old_email:
                cur.execute("""UPDATE user_info SET email_address= '%s' WHERE user_id=%s""" % (new_email, user_id))
                self.db.commit()
                print("The email address has been updated")
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
        """
            This function is used to update a specific users name using their
            user_id to locate and update the name associated with the user. It
            takes in the id, old name & the new name they want to update to,
            in order to change this within the SQL database. The function also checks whether
            the name retrieved from the SQL database matches the old name specified.
            If it does, then it will allow the user to update their name. Otherwise it will
            throw an error.
            Parameters
            -----------
            user_id: str
                user id of user
            old_name: str
                old name of user
            new_name: str
                new name the user wants
            Returns
            ---------
            Either:
                1. "The name has been updated"
                    returns result as True if the name is successfully updated and prints this statement
                2. "The current name is incorrect"
                    returns result as False and this statement if the old name does not match with the
                    record in SQL and will not update the record for the specified user_id.
        """
        result = False
        try:
            self.conn()
            cur = self.db.cursor()
            cur.execute("""SELECT name_user FROM user_info WHERE user_id=%s""" % user_id)
            name = cur.fetchone()
            print(name)
            if name[0] == old_name:
                cur.execute("""UPDATE user_info SET name_user= '%s' WHERE user_id=%s""" % (new_name, user_id))
                self.db.commit()
                print("The name has been updated")
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

            cur.execute("""DELETE FROM user_info WHERE user_id = {}""".format(user_id))

            self.db.commit()
            answer = "Account successfully deleted for username {}".format(user_name)
            cur.close()

        except UnboundLocalError as err:
            return 'No entry in database corresponding to given user ID: {}'.format(user_id)
        except Error as err:
            print("Failed to read data from Database", err)
            answer = err
        except Exception as err:
            answer = "Unsuccessful deleting account for username {},{}".format(user_name, err)
        finally:
            if self.conn:
                self.db.close()
                print("MySQL connection is closed")
        return answer

    # if the username/ name/ email don't match it returns the second elif statement and may be good to have a print to get the user's info back from the id
    def get_user_id(self, username, name, email):
        """
            This function takes a users username, name and email in order to identify the useR_id of that specific user
            if the function returns 1 user which has all three element which match a record in the SQL database it will
            return the user_id for that user and print their id, username, name & email. If it has 0 records matching it
            will say no user matching these element are found within the database else it will simply print that there
            was an issue finding a unique user_id.
            Parameters
            -----------
            username: str
                user_name of user
            name: str
                name of user
            email: str
                email_address of the user
            Returns
            ---------
            Either:
                1. print(answer, username, name, email)
                    if 1 user with a matching username, name & email is found it will return that information along with their user_id
                2. 'There are no users with the same user info'
                    if 0 users have that username, name & email the statement above will print
                3. "Issue finding unique user id"
                    else it will print that there was an issue finding any records with a user_id matching those elements
        """
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
