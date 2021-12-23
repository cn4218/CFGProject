from unittest.mock import patch
from unittest import TestCase, main
from user_main import MockFrontEnd, run

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent)) 
from CFGProject.scripts.user_db_utils import dbConnection
from CFGProject.scripts.config import PASSWORD, USER, HOST

"""
To run user tests:
1 - Install all the necessary modules:
unittest, sys, pathlib, json, requests, mysql.connector, flask, flask_cors, pprint
2 - run the user_info_and_wish_list_db.sql within the sql_scripts folder in the repository, to create the user table
3 - Run the user_db_utils.py within the scripts folder
4 - Run the app.py file within the scripts folder (keep this running whilst running the tests)
5 - Run the user_main.py file within the testing folder

"""

"""
In this script:
TestApiDb:
    test_add_new_user(self)
    test_add_new_user_2(self)
    test_get_fang_profile(self)
    test_add_new_user_has_been_added(self)
    test_deleting_user(self)
    test_user_login(self)
    test_user_login_false(self)
    test_delete_non_existing_user(self)

TestMockFrontEnd:
    test_positive_input(self, mock_input)
    test_negative_input(self, mock_input)
    test_wrong_input(self, mock_inputs)
    test_incorrect_email(self, mock_inputs)
    test_incorrect_email_2(self, mock_inputs)
    test_adding_user(self,mock_inputs)

TestRunFunction:
    test_incorrect_email_3(self,mock_inputs)
    test_creating_user(self,mock_inputs)
    test_deleting_user(self,mock_inputs)
    test_creating_user2_ayesha(self,mock_inputs)
    test_creating_user_zita(self,mock_inputs)
    test_goodbye(self,mock_input)

TestUsersChangeDetails:
    test_update_username(self)
    test_update_email(self)
    test_wrong_update_username(self)

TestUsersDelete:
    test_delete_zita_user(self)
    test_delete_fang_user(self)
    test_delete_sophie_user(self)
    test_delete_ayesha_user(self)
    test_delete_karma(self)
    test_delete_daisy(self)
    test_delete_unknown_id(self)

"""

class TestApiDb(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()
        self.db = dbConnection(password=PASSWORD,user = USER,host= HOST)

    def test_add_new_user(self):
        """
        Asserts that a new user has been added to database
        """
        expected = {'Email_Address': 'zita@gmail.com', 'Name_User': 'zita', 'User_Name': 'zita123'}
        result = self.mock.add_new_user('zita123','zita','zita@gmail.com')
        self.assertEqual(expected,result)

    def test_add_new_user_2(self):
        """
        Asserts that a new user has been added to database
        """
        expected = {'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang','User_Name': 'fang123'}
        result = self.mock.add_new_user('fang123','Fang','fang@gmail.com')
        self.assertEqual(expected,result)
    
    def test_get_fang_profile(self):
        """
        Uses get_user_id db_utils function to retrieve user from user_info table in SQL database and confirm that user has been added
        """
        self.user_id_fang = self.db.get_user_id('fang123','Fang','fang@gmail.com')
        expected = [{'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang', 'User_ID': self.user_id_fang, 'User_Name': 'fang123'}]
        result = self.mock.get_profile_by_id(self.user_id_fang)
        self.assertEqual(expected,result)


    def test_add_new_user_has_been_added(self):
        """
        Uses _get_user db_utils function to retrieve user from user_info table in SQL database and confirm that user has been added
        """
        add_to_db = self.mock.add_new_user('Holly123','Holly','holly@gmail.com')
        self.user_id_holly = self.db.get_user_id('Holly123','Holly','holly@gmail.com')
        expected = [{'User_ID': self.user_id_holly, 'User_Name': 'Holly123', 'Name_User': 'Holly', 'Email_Address': 'holly@gmail.com'}]
        result = self.db._get_user(self.user_id_holly)  ##calls new input from database
        self.assertEqual(expected,result)


    def test_deleting_user(self):
        """
        Asserts that frontend returns string confirming deletion of user and checks the row for that user id is empty in the user_info table
        """
        self.user_id_holly = self.db.get_user_id('Holly123','Holly','holly@gmail.com')
        result =  self.mock.delete_user_func(self.user_id_holly)
        expected = "Account successfully deleted for username {}".format('Holly123')
        self.assertEqual(expected,result)
        expected = []
        result =  self.mock.get_profile_by_id(self.user_id_holly)
        self.assertEqual(expected,result)


    def test_user_login(self):
        """
        Tests the login user route by using existing user login details and asserting returns True
        """
        result =  self.mock.user_login('fang123','fang@gmail.com')
        expected = True
        result = result['verify']
        self.assertEqual(expected,result)

    def test_user_login_false(self):
        """
        Test trying to login with incorrect login user details and asserts returns False
        """
        result =  self.mock.user_login('wronguser','fang@gmail.com')
        expected = {'verify': False}
        self.assertEqual(expected,result)

    def test_delete_non_existing_user(self):
        """
        Test trying to deleting non existent user and asserts string is returned
        """
        result = self.mock.delete_user_func(9999)
        expected = "No entry in database corresponding to given user ID: 9999"
        self.assertEqual(expected,result)

    
class TestMockFrontEnd(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()

    input_string = 'y'
    @patch('builtins.input', return_value = input_string)
    def test_positive_input(self, mock_input):
        """
        Tests MocKFrontEnd function runs a welcome message
        """
        result = self.mock.welcome_message()
        self.assertEqual(result,'y')

    @patch('builtins.input', return_value = 'n')
    def test_negative_input(self, mock_input):
        """
        Tests result of a MockFrontEnd function
        """
        result = self.mock.welcome_message()
        self.assertEqual(result,'n')

    @patch('builtins.input',side_effect=[6,7,8])
    def test_wrong_input(self, mock_inputs):
        """
        Tests inputting incorrect format to MockFrontEnd function
        """
        result = self.mock.welcome_message()
        self.assertEqual(result,'Too many tries inputting the incorrect format') 


    @patch('builtins.input',side_effect = ['sophie1998','Sophie','sophiehotmail.com'])
    def test_incorrect_email(self, mock_inputs):
        """
        Tests inputting incorrect email format into API route
        """
        result = self.mock.enter_details()
        self.assertEqual(result,'Your email address has NOT been given in the requested format')
    
    @patch('builtins.input',side_effect = ['sophie1998','Sophie','sophie@hotmailcom'])
    def test_incorrect_email_2(self, mock_inputs):
        """
        Tests inputting incorrect email format into API route
        """
        result = self.mock.enter_details()
        self.assertEqual(result,'Your email address has NOT been given in the requested format')

    
    @patch('builtins.input', side_effect = ['sophie1998','Sophie','sophie@hotmail.com'])
    def test_adding_user(self,mock_inputs):
        """
        Tests MockFrontEnd works with the API route for adding a new user
        """
        result = self.mock.enter_details()
        self.assertEqual(result, {'Email_Address': 'sophie@hotmail.com', 'Name_User': 'Sophie', 'User_Name': 'sophie1998'})


class TestRunFunction(TestCase):
        
    @patch('builtins.input', side_effect = ['y', 'sally123','sal','sally@gmailcom'])
    def test_incorrect_email_3(self,mock_inputs):
        """
        Tests incorrect email mock input when using run function
        """
        result = run()
        self.assertEqual(result,'Your email address has NOT been given in the requested format') 

    @patch('builtins.input', side_effect = ['y','Ayesha11','Ayesha','ayesha@live.com','n'])
    def test_creating_user(self,mock_inputs):
        """
        Tests mock inputting for adding a new user to SQL
         """
        result = run()
        self.assertEqual(result, {'Email_Address': 'ayesha@live.com', 'Name_User': 'Ayesha', 'User_Name': 'Ayesha11'})


    @patch('builtins.input',side_effect = ['y','annie20','Annie','annie@gmail.com','y'])
    def test_deleting_user(self,mock_inputs):
        """
        Tests mock input for deleting a user with the API endpoints, checks account is deleted with string assertion
        """
        result = run()
        self.assertEqual(result, 'Account successfully deleted for username {}'.format('annie20'))


    @patch('builtins.input', side_effect = ['y','Ayesha11','Ayesha','ayesha@live.com'])
    def test_creating_user2_ayesha(self,mock_inputs):
        """
        Tests mock input for attempting to create an user that already exists, checks that the user details are checked in table and a string returned
        """
        result = run()
        self.assertEqual(result, 'User details already exist, try again with a new username')

    @patch('builtins.input', side_effect = ['y','zita123','zita','zita@gmail.com'])
    def test_creating_user_zita(self,mock_inputs):
        """
        Tests mock input for attempting to create an user that already exists, checks that the user details are checked in table and a string returned
        """
        result = run()
        self.assertEqual(result, 'User details already exist, try again with a new username')

    @patch('builtins.input',return_value = 'n')
    def test_goodbye(self,mock_input):
        """
        Tests if customer doesn't want to engage with mockfrontend that Goodbye! string will be returned
        """
        result = run()
        self.assertEqual(result,'Goodbye!')

class TestUsersChangeDetails(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()
        self.db = dbConnection(password=PASSWORD,user = USER,host= HOST)

    def test_update_username(self):
        """
        Tests updating a users username from apple to oranges and then checks SQL user_info table to see if user exists with same userid but new username
        """
        user = self.mock.add_new_user('apple','karma','karma@gmail.com')
        karma_id = self.db.get_user_id('apple','karma','karma@gmail.com')
        result = self.mock.change_username(karma_id,'apple','oranges')
        answer = self.mock.get_profile_by_id(karma_id)
        karma_profile = [{'Email_Address': 'karma@gmail.com', 'Name_User': 'karma', 'User_ID': karma_id, 'User_Name': 'oranges'}]
        self.assertEqual(result,True)
        self.assertEqual(answer,karma_profile)

    def test_update_email(self):
        """
        Tests updating a users email address from daisy@gmail.com to daisy@live.com and checks SQL user_info table to see if user exists with same userid but new email address
        """
        user = self.mock.add_new_user('daisy123','daisy','daisy@gmail.com')
        daisy_id = self.db.get_user_id('daisy123','daisy','daisy@gmail.com')
        result = self.mock.change_email(daisy_id, 'daisy@gmail.com','daisy@live.com')
        answer = self.mock.get_profile_by_id(daisy_id)
        daisy_profile = [{'Email_Address': 'daisy@live.com', 'Name_User': 'daisy', 'User_ID': daisy_id, 'User_Name': 'daisy123'}]
        self.assertEqual(result,True)
        self.assertEqual(answer,daisy_profile)

    def test_wrong_update_username(self):
        """
        Tests trying to update a username with a non existant user id, checks if correct warning string is returned
        """
        result = self.mock.change_username(1000000,'wrong','test')
        answer = 'No user with corresonding userID'
        self.assertEqual(result,answer)
        
    


class TestUsersDelete(TestCase):
    """This class tests deleting every single user created in previous test classes and verifies if the user has been removed from the SQL table user_info within the cfg_project database"""

    def setUp(self):
        self.mock = MockFrontEnd()
        self.db = dbConnection('blu3bottl3')

    def test_delete_zita_user(self):
        zita_id = self.db.get_user_id('zita123','zita','zita@gmail.com')
        result = self.mock.delete_user_func(zita_id)
        expected = "Account successfully deleted for username {}".format('zita123')
        self.assertEqual(expected,result)

    def test_delete_fang_user(self):
        fang_id = self.db.get_user_id('fang123','Fang','fang@gmail.com')
        result = self.mock.delete_user_func(fang_id)
        expected = "Account successfully deleted for username {}".format('fang123')
        self.assertEqual(expected,result)

    def test_delete_sophie_user(self):
        sophie_id = self.db.get_user_id('sophie1998','Sophie','sophie@hotmail.com')
        result = self.mock.delete_user_func(sophie_id)
        expected = "Account successfully deleted for username {}".format('sophie1998')
        self.assertEqual(expected,result)


    def test_delete_ayesha_user(self):
        ayesha_id = self.db.get_user_id('Ayesha11','Ayesha','ayesha@live.com')
        print(ayesha_id)
        result = self.mock.delete_user_func(ayesha_id)
        print(result)
        expected = "Account successfully deleted for username {}".format('Ayesha11')
        self.assertEqual(expected,result)

    def test_delete_karma(self):
        karma_id = self.db.get_user_id('oranges','karma','karma@gmail.com')
        result = self.mock.delete_user_func(karma_id)
        expected = "Account successfully deleted for username {}".format('oranges')
        self.assertEqual(expected,result)

    def test_delete_daisy(self):
        daisy_id = self.db.get_user_id('daisy123','daisy','daisy@live.com')
        result = self.mock.delete_user_func(daisy_id)
        expected = "Account successfully deleted for username {}".format('daisy123')
        self.assertEqual(expected,result)

    def test_delete_unknown_id(self):
        result = self.mock.delete_user_func(9999)
        expected = "No entry in database corresponding to given user ID: 9999"
        self.assertEqual(expected,result)

    

if __name__ == "__main__":
    main()

