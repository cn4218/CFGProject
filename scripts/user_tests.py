import unittest
from unittest.mock import patch
from unittest import TestCase, main
from user_main import get_profile_by_id, add_new_user, delete_user_func, user_login
from user_db_utils import _get_user


class TestUserApiDb(unittest.TestCase):
    def test_new_user(self):
        expected = {'Email_Address': 'owen@gmail.com', 'Name_User': 'Owen', 'User_ID': 4, 'User_Name': 'owen123'}
        result = add_new_user(4,'owen123','Owen','owen@gmail.com')
        self.assertEqual(expected,result)

    def test_new_user_2(self):
        expected = {'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang', 'User_ID': 1, 'User_Name': 'fang123'}
        result = add_new_user(1,'fang123','Fang','fang@gmail.com')
        self.assertEqual(expected,result)
        expected = [{'Email_Address': 'fang@gmail.com', 'Name_User': 'Fang', 'User_ID': 1, 'User_Name': 'fang123'}]
        result = get_profile_by_id(1)
        self.assertEqual(expected,result)


    def test_new_user_has_been_added(self):
        add_to_db = add_new_user(5,'Holly123','Holly','holly@gmail.com')
        expected = [{'User_ID': 5, 'User_Name': 'Holly123', 'Name_User': 'Holly', 'Email_Address': 'holly@gmail.com'}]
        result = _get_user(5)  ##calls new input from database
        self.assertEqual(expected,result)

    def test_deleting_user(self):
        result = delete_user_func(4)
        expected = {}
        self.assertEqual(expected,result)
        expected = []
        result = get_profile_by_id(4)
        self.assertEqual(expected,result)
    

    def test_user_login(self):
        result = user_login(1,'fang123','Fang','fang@gmail.com')
        expected = True
        self.assertEqual(expected,result)

    def test_user_login_false(self):
        result = user_login(1,'wronguser','Fang','fang@gmail.com')
        expected = False
        self.assertEqual(expected,result)

if __name__ == "__main__":
    main()

