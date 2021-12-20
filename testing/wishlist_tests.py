from unittest.mock import patch
from unittest import TestCase, main
from wishlist_main import MockFrontEnd
from wishlist_db_utils import DbConnectionError, _connect_to_db, exception_handler, exception_handler_wish, exception_record_exists, _map_values, add_wish_list, _get_wish_list_individual, _get_wish_list_all, delete_wishlist_item, delete_wishlist
import unittest

"""
Note to Chizu:
This code is unfinished but I am finishing it today and tomorrow
"""

"""
Things to test:
Adding to the wishlist (this has to be done through mocking via the wishlist main file)
Getting an individual wishlist item (test through API, mocking and test what happens when a user doesn't exist)
Getting an entire wishlist (test through API, mocking and test what happens when a user doesn't exist)
Deleting a wishlist item (test through API, mocking and test what happens when a user doesn't exist)
Deleting an entire wishlist (test through API, mocking and test what happens when a user doesn't exist)
"""

"""
Functions contained in this file: 
class TestWishListApiDb(TestCase):
setUp(self)
test_get_wish_list_item(self)
test_get_wish_list_all(self)
"""

"""
Comments:
Remember to add test at the beginning of function names or the test will not run e.g. test_get_wish_list_item rather
than get_wish_list_item()

Make sure to add dummy data through the dummy data file as these functions rely on the dummy data
"""

class TestWishListApiDb(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")

    def test_get_wish_list_item_if_not_exists(self):
        self.UserID = 1500
        self.ProductID = 1500
        expected = "Wish list item for User_ID = {} and productID = {} does not exist ".format(self.UserID, self.ProductID)
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_get_wish_list_all_if_not_exists(self):
        self.UserID = 1500
        expected = "Wish list item for User_ID = {} does not exist ".format(self.UserID)
        result = _get_wish_list_all(self.UserID)
        self.assertEqual(expected, result)

    def test_delete_wish_list_item_if_not_exists(self):
        self.UserID = 1500
        self.ProductID = 1500
        expected = "Wishlist item for this User_ID: {} and productID: {} does not exist".format(self.UserID, self.ProductID)
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_delete_wish_list_all_if_not_exists(self):
        self.UserID = 1500
        expected = "Wishlist item for this User_ID: {} does not exist".format(self.UserID)
        result = delete_wishlist(self.UserID)
        self.assertEqual(expected, result)

    def test_get_wish_list_item_if_exists(self):
        expected = [{"User_ID": 1,
                     "brands": "xyz",
                     "brands_tags": "xyz",
                     "categories": "xyz",
                     "categories_en": "xyz",
                     "categories_tags": "xyz",
                     "code": 101,
                     "countries": "xyz",
                     "countries_en": "xyz",
                     "countries_tags": "xyz",
                     "image_ingredients_small_url": "xyz",
                     "image_ingredients_url": "xyz",
                     "image_nutrition_small_url": "xyz",
                     "image_nutrition_url": "xyz",
                     "image_small_url": "xyz",
                     "image_url": "xyz",
                     "ingredients_text": "xyz",
                     "productID": 2,
                     "product_name": "xyz",
                     "quantity": "xyz"}]
        self.UserID = 1
        self.ProductID = 2
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_get_wish_list_all_if_exists(self):
        expected = [
            {
                "User_ID": 3,
                "brands": "xyz",
                "brands_tags": "xyz",
                "categories": "xyz",
                "categories_en": "xyz",
                "categories_tags": "xyz",
                "code": 101,
                "countries": "xyz",
                "countries_en": "xyz",
                "countries_tags": "xyz",
                "image_ingredients_small_url": "xyz",
                "image_ingredients_url": "xyz",
                "image_nutrition_small_url": "xyz",
                "image_nutrition_url": "xyz",
                "image_small_url": "xyz",
                "image_url": "xyz",
                "ingredients_text": "xyz",
                "productID": 1,
                "product_name": "xyz",
                "quantity": "xyz"
            },

            {
                "User_ID": 3,
                "brands": "xyz",
                "brands_tags": "xyz",
                "categories": "xyz",
                "categories_en": "xyz",
                "categories_tags": "xyz",
                "code": 101,
                "countries": "xyz",
                "countries_en": "xyz",
                "countries_tags": "xyz",
                "image_ingredients_small_url": "xyz",
                "image_ingredients_url": "xyz",
                "image_nutrition_small_url": "xyz",
                "image_nutrition_url": "xyz",
                "image_small_url": "xyz",
                "image_url": "xyz",
                "ingredients_text": "xyz",
                "productID": 2,
                "product_name": "xyz",
                "quantity": "xyz"
            }
        ]
        self.UserID = 3
        result = _get_wish_list_all(self.UserID)
        self.assertEqual(expected, result)

class MockFrontEnd(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")

"""
I put the following code even though they are also testing the API into a seperate class, as the tests don't seem to be
running in order they are written so these functions were messing with other tests 
"""
class TestWishListApiDbDeletingUsers(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")

    def test_delete_wish_list_item(self):
        self.UserID = 2
        self.ProductID = 2
        expected = "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}".format(
            self.UserID, self.ProductID, {})
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_delete_wish_list_all(self):
        self.UserID = 3
        expected = "The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}".format(
            self.UserID, {})
        result = delete_wishlist(self.UserID)
        self.assertEqual(expected, result)



"""
This following code will hopefully make my tests run in order
"""

if __name__ == '__main__':
    import inspect


    def get_decl_line_no(cls):
        return inspect.getsourcelines(cls)[1]


    # get all test cases defined in this module
    test_case_classes = list(filter(lambda c: c.__name__ in globals(),
                                    unittest.TestCase.__subclasses__()))

    # sort them by decl line no
    test_case_classes.sort(key=get_decl_line_no)

    # make into a suite and run it
    suite = unittest.TestSuite(cls() for cls in test_case_classes)
    unittest.TextTestRunner().run(suite)

