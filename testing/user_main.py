import requests
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent)) 

from CFGProject.scripts.user_db_utils import dbConnection
from CFGProject.scripts.config import PASSWORD, USER, HOST
"""
In this script:
MockFrontEnd : class
run : function

"""

class MockFrontEnd:
    """
    Class that mocks app.py for user api functions using user API and user db utils. 
    This includes mocking creating a new user, changing username, changing email, displaying user details and deleting user account.
    Functions:
    get_profile_by_id(self,user_id)
    add_new_user(self,user_name,name,email)
    delete_user_func(self,user_id)
    user_login(self,user_name,email)
    change_username(self,userID, prev_username, updated_username)
    change_email(self,userID, prev_email, updated_email)
    welcome_message(self)
    enter_details(self)
    verify_account_added(self)
    displaying_user(self)
    deleting_account(self)

    """
    def __init__(self,pass_word= PASSWORD, user_=USER, host_=HOST):
        """
        Inititiates 

        Parameters
        ----------
        password : str
            password for mysql workbench account, by default = PASSWORD
        user : str
            user for mysql workbench account, by default USER
        host : str
            host for mysql workbench account, by default HOST
        """
        self.db_utils = dbConnection(password=pass_word, user=user_, host=host_)

        
    def get_profile_by_id(self,user_id):
        """
        Mocks API endpoint for get_users function

        Parameters
        ----------
        user_id : int
            User ID for user

        Returns
        -------
        result.json() : list
            list of dictionary for corresponding user in this format:
            [
            {
                "Email_Address": "sarah@gmail.com", 
                "Name_User": "sarah,", 
                "User_ID": 3, 
                "User_Name": "sarah2000"
            }
            ]
            empty if there is not corresponding user id
        """
        result = requests.get(
            "http://127.0.0.1:5001/profile/{}".format(user_id),
            headers = {"content_type": "application/json"},

        )
        #results = _map_values(result)
        return result.json()

    def add_new_user(self,user_name,name,email):
        """
        Mocks API endpoint for user_acc function

        Parameters
        ----------
        user_name : str
            username for user
        name : str
            name for user
        email : str
            email for user

        Returns
        -------
        result.json() : Either:
        user: dict
            user dictionary for the new user that's been added
        OR:
        answer: str
            string containing message on why the user hasn't been added
        """

        user = {
            "User_Name": user_name,
            "Name_User": name,
            "Email_Address":email

        }
        result = requests.post(
            "http://127.0.0.1:5001/register",
            headers={"content_type":"application/json"},
            data = json.dumps(user),
        )
        print(result)
        return result.json()



    def delete_user_func(self,user_id):
        """
        Mocks API endpoint for delete_user_

        Parameters
        ----------
        user_id : int
            id for user
        Returns
        --------
            1. "Account successfully deleted for username niki123"
                    It will return this statement if an account is deleted successfully and will update the SQL database by removing the user
            2. "No entry in database corresponding to given user ID: 2"
                    It will return this statement if you attempt to delete a user which doesn't exist in the SQL database/ if they've already
                    been removed.
        """
        result = requests.get(
            "http://127.0.0.1:5001/delete/{}".format(user_id),
            headers= {"content_type": "application/json"}
        )
        print(result)
        return result.json()


    def user_login(self,user_name,email):
        """
        Mocks API endpoint for get request for verify_login_api function 

        Parameters
        ----------
        user_name : str
            name for user
        email : str
            email for user
        Returns
        ---------
           Either:
            1. {
                "user_id": 3,
                "verify": true
                }
                    if the user exists and the username & email can be verified in the SQL database it will return the True boolean and dict above.
            2. {
                "verify": false
                }
                    if the user's username/ email is incorrect or the user does not exist in the SQL database it will return False and the dict above.

        """

        result = requests.get(
            "http://127.0.0.1:5001/login/{}/{}".format(user_name,email),
            headers = {"content_type":"application/json"},
        )
        return result.json()

    def change_username(self,userID, prev_username, updated_username):
        """
        Mocks API endpoint for get request for change_user_name function 

        Parameters
        ----------
        userID : int
            user id
        prev_username : str
            users current username
        updated_username : str
            the username user wants to change to

        Returns
        -------
        results.json()
            Either: bool
                if user updated or not
            Or: str
                'No user with corresonding userID'
        """

        result = requests.get(
            "http://127.0.0.1:5001/profile/change/{}/{}/{}".format(userID,prev_username,updated_username),
            headers = {"content_type":"application/json"},
        )
        return result.json()

    def change_email(self,userID, prev_email, updated_email):
        """
        Mocks API endpoint for get request for change_user_email function

        Parameters
        ----------
        userID : int
            user id
        prev_email : str
            users current email
        updated_email : str
            the email user wants to change to

        Returns
        -------
        return.json()
            return from change_user_email
        """
        result = requests.get(
            "http://127.0.0.1:5001/profile/change/email/{}/{}/{}".format(userID,prev_email,updated_email),
            headers = {"content_type":"application/json"},
        )
        return result.json()

    def welcome_message(self):
        """
        Function that prints welcome message for mocking front end

        Returns
        -------
        answer : str
            Either the answer inputted by the user or string 'Too many tries inputting the incorrect format' if email input is wrong

        Raises
        ------
        Exception
            Exception raised when answer input is not 'y' or 'n'
        """

        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()
        i = 0
        while i<=2:
    
        ### put exception handling here!!!
            try:
                answer = input('Would you like to make an account, y/n? ')
                print(answer)
                if answer != 'y' and answer !='n':
                    raise Exception
            except:
                print('Your answer has NOT been given in the requested format')
                i+=1

            finally:
                if answer == 'y' or answer=='n':
                    return answer

        answer = 'Too many tries inputting the incorrect format'
        return answer


    def enter_details(self):
        """
        Mocks entering details for new user

        Returns
        -------
        result : str or dict
            str : if theres reasn why user hasn't been added
            dict : if user successfully added
        """

        self.username = input('Enter your username: ')
        self.nameuser = input('Enter your name: ')
        self.emailaddress = input('Enter your email address: ')

        result = self.add_new_user(self.username,self.nameuser,self.emailaddress)

        return result

    def verify_account_added(self):
        """
        Function that verifies if account has been added and retrieves 
        Returns
        -------
        verify_account : dict
            dict containing information about wether user added
        """
        self.user_id = self.db_utils.get_user_id(self.username,self.nameuser,self.emailaddress)
        verify_account = self.user_login(self.username,self.emailaddress)
        return verify_account

    def displaying_user(self):
        """
        Function that mocks displaying user details

        Returns
        -------
        display_user_details : list
            list of dictionary displaying user details
        """
        print('Account has been created successfully')
        display_user_details = self.get_profile_by_id(self.user_id)  
        return display_user_details

    def deleting_account(self):
        """
        Function that mocks deleting user account and displaying message

        Returns
        -------
        issue : str
            if error with input string
        ans : str
            answer input from deleting account questions
        result : str
            string detailing if account has been deleted
        

        Raises
        ------
        Exception
            Error with input string format
        """
        ans = input('Would you like to delete your account, y/n? ')
        try: 
            if ans != 'y' and ans !='n':
                issue = 'Your answer has NOT been given in the requested format'
                raise Exception(issue)
            elif ans == 'y':
                result = self.delete_user_func(self.user_id)
                if result == "Account successfully deleted for user {}".format(self.user_id):
                    print('Account successfully deleted') 
                    return 'Account successfully deleted'

            elif ans == 'n':
                return ans
            return result
        except:
            return issue
    


def run():
    """
    Uses MockFrontEnd to create a series of messages to mock a user page for user. Including input functions for user to enter answers and details.
    Parameters
    -----------
    pass_word : str
        SQL password to connect to database

    Returns
    -------
    result : str or dict
        str : if theres reasn why user hasn't been added
        dict : if user successfully added
    ans : str
        result to input function
    str : 
        'Account has not been added to database'
        'Goodbye!'

    """
    mock = MockFrontEnd()
    issue = None

    ans = 'Issue with run function'

    answer = mock.welcome_message()
    if answer == 'y':
        try:
            result = mock.enter_details()
            print(result)
            if isinstance(result,str):
                return result
            else:
                verify_account = mock.verify_account_added()
                print(verify_account)
                if verify_account['verify'] == False:
                    return 'Account has not been added to database'
                    
                else:
                    user_details = mock.displaying_user()
                    print(result)
                    ans = mock.deleting_account()
                    if ans == 'n':
                        return result
                    else:
                        return ans

        except Exception as err:
            ans = err
            return err

    else:
        return 'Goodbye!'


if __name__ =='__main__':
    output = run()

