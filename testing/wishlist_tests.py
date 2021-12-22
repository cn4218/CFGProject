from unittest.mock import patch
from mock import patch
from unittest import TestCase, main
from wishlist_config import USER, PASSWORD, HOST
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

class TestWishListApiDb(unittest.TestCase):
test_add_wish_list(self)
test_get_wish_list_item_if_not_exists(self)
test_get_wish_list_all_if_not_exists(self)
test_delete_wish_list_item_if_not_exists(self)
test_delete_wish_list_all_if_not_exists(self)
test_get_wish_list_item_if_exists(self)
test_get_wish_list_all_if_exists(self)

class TestWishListApiDbDeletingUsers(unittest.TestCase):
test_delete_wish_list_item(self)
test_delete_wish_list_all(self)
"""

"""
Comments:
Remember to add test at the beginning of function names or the test will not run e.g. test_get_wish_list_item rather
than get_wish_list_item()

Make sure to add dummy data through the dummy data file as these functions rely on the dummy data, please run the
dummy data SQL file before running this file

Please have your cursor located at the bottom of this file before running:
https://stackoverflow.com/questions/52472091/how-to-run-unittest-test-cases-in-the-order-they-are-declared
"""

"""
This following class tests the actual API and runs unit tests on the functions of the wishlist API
"""

class TestWishListApiDb(unittest.TestCase):

    def test_add_wish_list(self):
        self.ProductID = 4
        self.Code_Wish = 702
        self.Product_name = "xyz"
        self.Ingredients_Text = "xyz"
        self.Quantity = "xyz"
        self.Brands = "xyz"
        self.Brands_tags = "xyz"
        self.Categories = "xyz"
        self.Categories_Tags = "xyz"
        self.Categories_En = "xyz"
        self.Countries = "xyz"
        self.Countries_Tags = "xyz"
        self.Countries_en = "xyz"
        self.Image_url = "xyz"
        self.Image_Small_url = "xyz"
        self.Image_Ingredients_url = "xyz"
        self.Image_Ingredients_Small_url = "xyz"
        self.Image_Nutrition_url = "xyz"
        self.Image_Nutrition_Small_url = "xyz"
        self.UserID = 2
        add_wish_list(self.ProductID,
                      self.Code_Wish,
                      self.Product_name,
                      self.Ingredients_Text,
                      self.Quantity,
                      self.Brands,
                      self.Brands_tags,
                      self.Categories,
                      self.Categories_Tags,
                      self.Categories_En,
                      self.Countries,
                      self.Countries_Tags,
                      self.Countries_en,
                      self.Image_url,
                      self.Image_Small_url,
                      self.Image_Ingredients_url,
                      self.Image_Ingredients_Small_url,
                      self.Image_Nutrition_url,
                      self.Image_Nutrition_Small_url,
                      self.UserID)
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        expected = [{"User_ID": 2,
                     "brands": "xyz",
                     "brands_tags": "xyz",
                     "categories": "xyz",
                     "categories_en": "xyz",
                     "categories_tags": "xyz",
                     "code": 702,
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
                     "productID": 4,
                     "product_name": "xyz",
                     "quantity": "xyz"}]
        self.assertEqual(expected, result)

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

"""
This following class tests mocked input derived from my wishlist_main file to test the wishlist functions

Notes on whats going on:
Must use setUp to initialize this class for mocking input rather than __init__ as this will overrwrite __init__ and is
not allowed. Whenever initializing test classes you must use the setUp function.

The patch function temporarily replaces the target object with a different object during the test. The @patch decorator 
accepts a big amount of arguments. As I will talk only about mocking inputs, our target is the builtin function input, 
and the target for the patch decorator is ‘builtins.input’.

The side_effect argument can accept a function to be called when the mock is called, an iterable or an Exception. 
Passing in an iterable is very useful to mock multiple inputs inside the testing function, because it will yield the 
next value everytime it’s called. When using side_effects, put mock_inputs as your second argument.

The return_value configure the value returned when the mock is called. It will always return the same value when the 
mock is called.

When to use side_effect or return_value: I use side_effect when the function I’m testing has more than one call to 
input(). The return_value is good to functions that call input() once.
"""

class TestMockFrontEnd(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")

    def test_add_new_wishlist(self):
        self.mock.add_new_wishlist()
        result = _get_wish_list_individual(1, 6)
        expected = [{"User_ID": 1,
                     "productID": 6,
                     "code": 62263436,
                     "product_name": "Huile'' de massage larnica",
                     "ingredients_text": "helianthus '''annuus' (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles",
                     "quantity": "100 ml",
                     "brands": "Weleda",
                     "brands_tags": "weleda",
                     "categories": "Skincare",
                     "categories_tags": r'en:body,en:body-oils,fr:huile-de-massage',
                     "categories_en": r'Body,Body-oils,fr:huile-de-massage',
                     "countries": "France",
                     "countries_tags": "en:france",
                     "countries_en": "France",
                     "image_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg",
                     "image_small_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg",
                     "image_ingredients_url": "",
                     "image_ingredients_small_url": "",
                     "image_nutrition_url": "",
                     "image_nutrition_small_url": ""
                        }]
        self.assertEqual(expected, result)

    @patch('builtins.input', side_effect=[1, 2])
    def test_verify_wish_list_item(self, mock_inputs):
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
        result = self.mock.verify_wish_list_item()
        self.assertEqual(expected, result)

    @patch('builtins.input', side_effect=[3])
    def test_verify_wish_list(self, mock_inputs):
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
        result = self.mock.verify_wish_list()
        self.assertEqual(expected, result)

    # this is my only test so far that i cant get to work, currently working on it

    @patch("wishlist_main.MockFrontEnd.add_new_wishlist")
    def test_add_new_wishlist_mocked_values(self, mock_wish_list_dict):
        wishlistdict = {"username": "sarah",
                        "User_ID": 1,
                        "wishlist": {
                            "productID": 4,
                            "code": "62263436",
                            "product_name": "Huile'' de massage larnica",
                            "ingredients_text": "helianthus '''annuus' (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles",
                            "quantity": "100 ml",
                            "brands": "Weleda",
                            "brands_tags": "weleda",
                            "categories": "Skincare",
                            "categories_tags": r'en:body,en:body-oils,fr:huile-de-massage',
                            "categories_en": r'Body,Body-oils,fr:huile-de-massage',
                            "countries": "France",
                            "countries_tags": "en:france",
                            "countries_en": "France",
                            "image_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg",
                            "image_small_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg",
                            "image_ingredients_url": "",
                            "image_ingredients_small_url": "",
                            "image_nutrition_url": "",
                            "image_nutrition_small_url": ""
                        }}
        wishlistdict = mock_wish_list_dict.return_value
        wishlistdict = self.mock.add_new_wishlist.wishlistdict.return_value
        data = self.mock.add_new_wishlist()
        data()
        result = _get_wish_list_individual(1, 4)
        expected = [{"User_ID": 1,
                     "productID": 4,
                     "code": "62263436",
                     "product_name": "Huile'' de massage larnica",
                     "ingredients_text": "helianthus '''annuus' (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles",
                     "quantity": "100 ml",
                     "brands": "Weleda",
                     "brands_tags": "weleda",
                     "categories": "Skincare",
                     "categories_tags": r'en:body,en:body-oils,fr:huile-de-massage',
                     "categories_en": r'Body,Body-oils,fr:huile-de-massage',
                     "countries": "France",
                     "countries_tags": "en:france",
                     "countries_en": "France",
                     "image_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg",
                     "image_small_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg",
                     "image_ingredients_url": "",
                     "image_ingredients_small_url": "",
                     "image_nutrition_url": "",
                     "image_nutrition_small_url": ""
                        }]
        self.assertEqual(expected, result)

"""
I put the following code even though they are also testing the wishlist_main into a seperate class, as the tests don't 
seem to be running in order they are written so these functions were messing with other tests 

This following class tests mocked input derived from my wishlist_main file to test the wishlist functions
"""

class TestMockFrontEndDelete(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")

    @patch('builtins.input', side_effect=[2, 2])
    def test_delete_wish_list_item(self, mock_inputs):
        expected = "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}".format(
            2, 2, {})
        result = self.mock.deleting_wishlist_item()
        self.assertEqual(expected, result)

    @patch('builtins.input', side_effect=[3])
    def test_delete_wish_list_all(self, mock_inputs):
        expected = expected = "The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}".format(3, {})
        result = self.mock.deleting_wishlist()
        self.assertEqual(expected, result)

"""
The following class is to re-add data that was just deleted by testing delete functions from wishlist_main file
"""
class ReAddingData(unittest.TestCase):
    def test_re_add_mock_wish_list(self):
        self.ProductID = 2
        self.Code_Wish = 101
        self.Product_name = "xyz"
        self.Ingredients_Text = "xyz"
        self.Quantity = "xyz"
        self.Brands = "xyz"
        self.Brands_tags = "xyz"
        self.Categories = "xyz"
        self.Categories_Tags = "xyz"
        self.Categories_En = "xyz"
        self.Countries = "xyz"
        self.Countries_Tags = "xyz"
        self.Countries_en = "xyz"
        self.Image_url = "xyz"
        self.Image_Small_url = "xyz"
        self.Image_Ingredients_url = "xyz"
        self.Image_Ingredients_Small_url = "xyz"
        self.Image_Nutrition_url = "xyz"
        self.Image_Nutrition_Small_url = "xyz"
        self.UserID = 2
        add_wish_list(self.ProductID,
                      self.Code_Wish,
                      self.Product_name,
                      self.Ingredients_Text,
                      self.Quantity,
                      self.Brands,
                      self.Brands_tags,
                      self.Categories,
                      self.Categories_Tags,
                      self.Categories_En,
                      self.Countries,
                      self.Countries_Tags,
                      self.Countries_en,
                      self.Image_url,
                      self.Image_Small_url,
                      self.Image_Ingredients_url,
                      self.Image_Ingredients_Small_url,
                      self.Image_Nutrition_url,
                      self.Image_Nutrition_Small_url,
                      self.UserID)
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        expected = [{"User_ID": 2,
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
        self.assertEqual(expected, result)

    def test_re_add_mock_wish_list_all_if_exists(self):
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

"""
I put the following code even though they are also testing the API into a seperate class, as the tests don't seem to be
running in order they are written so these functions were messing with other tests 


This following class tests the actual API and runs unit tests related to deleting data such as deleting the individual
wishlist item and entire wishlist 

I readded the data after running the delete tests

"""

class TestWishListApiDbDeletingUsers(unittest.TestCase):
    def test_delete_wish_list_item(self):
        self.UserID = 2
        self.ProductID = 2
        expected = "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}".format(
            self.UserID, self.ProductID, {})
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

# the following test re-adds the data, I decided to do it as a test to make sure the right data was indeed re-added
    def test_re_add_wish_list(self):
        self.ProductID = 2
        self.Code_Wish = 101
        self.Product_name = "xyz"
        self.Ingredients_Text = "xyz"
        self.Quantity = "xyz"
        self.Brands = "xyz"
        self.Brands_tags = "xyz"
        self.Categories = "xyz"
        self.Categories_Tags = "xyz"
        self.Categories_En = "xyz"
        self.Countries = "xyz"
        self.Countries_Tags = "xyz"
        self.Countries_en = "xyz"
        self.Image_url = "xyz"
        self.Image_Small_url = "xyz"
        self.Image_Ingredients_url = "xyz"
        self.Image_Ingredients_Small_url = "xyz"
        self.Image_Nutrition_url = "xyz"
        self.Image_Nutrition_Small_url = "xyz"
        self.UserID = 2
        add_wish_list(self.ProductID,
                      self.Code_Wish,
                      self.Product_name,
                      self.Ingredients_Text,
                      self.Quantity,
                      self.Brands,
                      self.Brands_tags,
                      self.Categories,
                      self.Categories_Tags,
                      self.Categories_En,
                      self.Countries,
                      self.Countries_Tags,
                      self.Countries_en,
                      self.Image_url,
                      self.Image_Small_url,
                      self.Image_Ingredients_url,
                      self.Image_Ingredients_Small_url,
                      self.Image_Nutrition_url,
                      self.Image_Nutrition_Small_url,
                      self.UserID)
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        expected = [{"User_ID": 2,
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
        self.assertEqual(expected, result)

    def test_delete_wish_list_all(self):
        self.UserID = 3
        expected = "The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}".format(
            self.UserID, {})
        result = delete_wishlist(self.UserID)
        self.assertEqual(expected, result)

# the following test re-adds the data, I decided to do it as a test to make sure the right data was indeed re-added
    def test_re_add_wish_list_all_if_exists(self):
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

