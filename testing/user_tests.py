from unittest.mock import patch
from unittest import TestCase, main
from user_main import MockFrontEnd, run

from user_db_utils import _get_user, get_user_id


class TestUserApiDb(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()

    def test_new_user(self):
        expected = {'Email_Address': 'zita@gmail.com', 'Name_User': 'zita', 'User_Name': 'zita123'}
        result = self.mock.add_new_user('zita123','zita','zita@gmail.com')
        self.assertEqual(expected,result)

    def test_new_user_2(self):
        expected = {'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang','User_Name': 'fang123'}
        result = self.mock.add_new_user('fang123','Fang','fang@gmail.com')
        self.assertEqual(expected,result)
        self.user_id_fang = get_user_id('fang123','Fang','fang@gmail.com')
        expected = [{'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang', 'User_ID': self.user_id_fang, 'User_Name': 'fang123'}]
        result = self.mock.get_profile_by_id(self.user_id_fang)
        self.assertEqual(expected,result)


    def test_new_user_has_been_added(self):
        add_to_db = self.mock.add_new_user('Holly123','Holly','holly@gmail.com')
        self.user_id_holly = get_user_id('Holly123','Holly','holly@gmail.com')
        expected = [{'User_ID': self.user_id_holly, 'User_Name': 'Holly123', 'Name_User': 'Holly', 'Email_Address': 'holly@gmail.com'}]
        result = _get_user(self.user_id_holly)  ##calls new input from database
        self.assertEqual(expected,result)


    def test_deleting_user(self):
        self.user_id_holly = get_user_id('Holly123','Holly','holly@gmail.com')
        result =  self.mock.delete_user_func(self.user_id_holly)
        expected = "Account successfully deleted for username {}".format('Holly123')
        self.assertEqual(expected,result)
        expected = []
        result =  self.mock.get_profile_by_id(self.user_id_holly)
        self.assertEqual(expected,result)


    def test_user_login(self):
        result =  self.mock.user_login('fang123','fang@gmail.com')
        expected = True
        result = result['verify']
        self.assertEqual(expected,result)

    def test_user_login_false(self):
        result =  self.mock.user_login('wronguser','fang@gmail.com')
        expected = {'verify': False}
        self.assertEqual(expected,result)

    def test_delete_non_existing_user(self):
        result = self.mock.delete_user_func(9999)
        expected = "No entry in database corresponding to given user ID: 9999"
        self.assertEqual(expected,result)

    
class TestMockFrontEnd(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()

    input_string = 'y'
    @patch('builtins.input', return_value = input_string)
    def test_positive_input(self, mock_input):
        result = self.mock.welcome_message()
        self.assertEqual(result,'y')

    @patch('builtins.input', return_value = 'n')
    def test_positive_input(self, mock_input):
        result = self.mock.welcome_message()
        self.assertEqual(result,'n')

    @patch('builtins.input',side_effect=[6,7,8])
    def test_wrong_input(self, mock_inputs):
        result = self.mock.welcome_message()
        self.assertEqual(result,'Too many tries inputting the incorrect format') 


    @patch('builtins.input',side_effect = ['sophie1998','Sophie','sophiehotmail.com'])
    def test_incorrect_email(self, mock_inputs):
        result = self.mock.enter_details()
        self.assertEqual(result,'Your email address has NOT been given in the requested format')
    
    @patch('builtins.input',side_effect = ['sophie1998','Sophie','sophie@hotmailcom'])
    def test_incorrect_email_2(self, mock_inputs):
        result = self.mock.enter_details()
        self.assertEqual(result,'Your email address has NOT been given in the requested format')

    
    @patch('builtins.input', side_effect = ['sophie1998','Sophie','sophie@hotmail.com'])
    def test_adding_user(self,mock_inputs):
        result = self.mock.enter_details()
        self.assertEqual(result, {'Email_Address': 'sophie@hotmail.com', 'Name_User': 'Sophie', 'User_Name': 'sophie1998'})


class TestRunFunction(TestCase):
        
    @patch('builtins.input', side_effect = ['y', 'sally123','sal','sally@gmailcom'])
    def test_incorrect_email_3(self,mock_inputs):
        result = run()
        self.assertEqual(result,'Your email address has NOT been given in the requested format') 

    @patch('builtins.input', side_effect = ['y','Ayesha11','Ayesha','ayesha@live.com','n'])
    def test_creating_user(self,mock_inputs):
        result = run()
        self.assertEqual(result, {'Email_Address': 'ayesha@live.com', 'Name_User': 'Ayesha', 'User_Name': 'Ayesha11'})


    @patch('builtins.input',side_effect = ['y','annie20','Annie','annie@gmail.com','y'])
    def test_deleting_user(self,mock_inputs):
        result = run()
        self.assertEqual(result, 'Account successfully deleted for username {}'.format('annie20'))


    @patch('builtins.input', side_effect = ['y','Ayesha11','Ayesha','ayesha@live.com'])
    def test_creating_user2(self,mock_inputs):
        result = run()
        self.assertEqual(result, 'User details already exist, try again with a new username')

    @patch('builtins.input', side_effect = ['y','zita123','zita','zita@gmail.com'])
    def test_creating_user2(self,mock_inputs):
        result = run()
        self.assertEqual(result, 'User details already exist, try again with a new username')

    @patch('builtins.input',return_value = 'n')
    def test_goodbye(self,mock_input):
        result = run()
        self.assertEqual(result,'Goodbye!')

class TestDeleteUsersCreated(TestCase):
    def setUp(self):
        self.mock = MockFrontEnd()

    def test_delete_zita_user(self):
        zita_id = get_user_id('zita123','zita','zita@gmail.com')
        result = self.mock.delete_user_func(zita_id)
        expected = "Account successfully deleted for username {}".format('zita123')
        self.assertEqual(expected,result)

    def test_delete_fang_user(self):
        fang_id = get_user_id('fang123','Fang','fang@gmail.com')
        result = self.mock.delete_user_func(fang_id)
        expected = "Account successfully deleted for username {}".format('fang123')
        self.assertEqual(expected,result)

    def test_delete_sophie_user(self):
        sophie_id = get_user_id('sophie1998','Sophie','sophie@hotmail.com')
        result = self.mock.delete_user_func(sophie_id)
        expected = "Account successfully deleted for username {}".format('sophie1998')
        self.assertEqual(expected,result)


    def test_delete_ayesha_user(self):
        ayesha_id = get_user_id('Ayesha11','Ayesha','ayesha@live.com')
        print(ayesha_id)
        result = self.mock.delete_user_func(ayesha_id)
        print(result)
        expected = "Account successfully deleted for username {}".format('Ayesha11')
        self.assertEqual(expected,result)

    def test_delete_unknown_id(self):
        result = self.mock.delete_user_func(9999)
        expected = "No entry in database corresponding to given user ID: 9999"
        self.assertEqual(expected,result)

    



    
    

if __name__ == "__main__":
    main()
