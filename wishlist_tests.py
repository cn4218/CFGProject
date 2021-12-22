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

Also besides one test, all these tests work the issue is they're not running in the right order lol
"""

"""
FUNCTIONS CONTAINED IN THIS FILE:

class TestWishListApiDb(TestCase)
test_1_add_wish_list(self)
test_2_get_wish_list_item_if_not_exists(self)
test_3_get_wish_list_all_if_not_exists(self)
test_4_delete_wish_list_item_if_not_exists(self)
test_5_delete_wish_list_all_if_not_exists(self)
test_6_get_wish_list_item_if_exists(self)
test_7_get_wish_list_all_if_exists(self)

class TestMockFrontEndDeleteDataFirst(TestCase):
setUp(self)
test_8_delete_wish_list_item_before_re_adding(self, mock_inputs)

class TestMockFrontEnd(TestCase):
test_8_add_new_wishlist(self)
test_9_verify_wish_list_item(self, mock_inputs)
test_10_verify_wish_list(self, mock_inputs)
test_11_add_new_wishlist_mocked_values(self, mock_wish_list_dict)

class TestMockFrontEndDelete(TestCase):
setUp(self)
test_12_delete_wish_list_item(self, mock_inputs)
test_13_delete_wish_list_all(self, mock_inputs)

class ReAddingData(TestCase):
test_14_re_add_mock_wish_list(self)
test_15_re_add_wish_list_1(self)
test_16_re_add_wish_list_2(self)

class TestWishListApiDbDeletingUsers(TestCase):
test_17_delete_wish_list_item(self):
test_18_re_add_wish_list(self):
test_19_delete_wish_list_all(self)
test_20_re_add_wish_list_1(self):
test_21_re_add_wish_list_2(self):
"""

"""
Comments:
Remember to add test at the beginning of function names or the test will not run e.g. test_get_wish_list_item rather
than get_wish_list_item()

Make sure to add dummy data through the dummy data file as these functions rely on the dummy data, please run the
dummy data SQL file before running this file

Please have your cursor located at the bottom of this file before running:
https://stackoverflow.com/questions/52472091/how-to-run-unittest-test-cases-in-the-order-they-are-declared

Tests are execute in alpahbetical order of the functions 
or string order so like
def test_1():
def test_2()
etc
so I have numbered the tests so they will run in this order
"""



"""
This following class tests the actual API and runs unit tests on the functions of the wishlist API
"""

class TestWishListApiDb(unittest.TestCase):

    def test_1_add_wish_list(self):
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
        # the following is to delete the record if it already exists then re-add
        delete_wishlist_item(self.UserID, self.ProductID)
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


    def test_2_get_wish_list_item_if_not_exists(self):
        self.UserID = 1500
        self.ProductID = 1500
        expected = "Wish list item for User_ID = {} and productID = {} does not exist ".format(self.UserID, self.ProductID)
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        self.assertEqual(expected, result)


    def test_3_get_wish_list_all_if_not_exists(self):
        self.UserID = 1500
        expected = "Wish list User_ID = {} is empty """.format(self.UserID)
        result = _get_wish_list_all(self.UserID)
        self.assertEqual(expected, result)


    def test_4_delete_wish_list_item_if_not_exists(self):
        self.UserID = 1500
        self.ProductID = 1500
        expected = ("Wishlist item for User_ID: {} and "
        "productID: {} does not exist").format(self.UserID, self.ProductID)
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)


    def test_5_delete_wish_list_all_if_not_exists(self):
        self.UserID = 1500
        expected = "Wishlist item for this User_ID: {} does not exist".format(self.UserID)
        result = delete_wishlist(self.UserID)
        self.assertEqual(expected, result)

    def test_6_get_wish_list_item_if_exists(self):
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


    def test_7_get_wish_list_all_if_exists(self):
        expected = [{'productID': 1,
                     'code': 101,
                     'product_name': 'xyz',
                     'ingredients_text': 'xyz',
                     'quantity': 'xyz',
                     'brands': 'xyz',
                     'brands_tags': 'xyz',
                     'categories': 'xyz',
                     'categories_tags': 'xyz',
                     'categories_en': 'xyz',
                     'countries': 'xyz',
                     'countries_tags': 'xyz',
                     'countries_en': 'xyz',
                     'image_url': 'xyz',
                     'image_small_url': 'xyz',
                     'image_ingredients_url': 'xyz',
                     'image_ingredients_small_url': 'xyz',
                     'image_nutrition_url': 'xyz',
                     'image_nutrition_small_url': 'xyz',
                     'User_ID': 2},
                    {'productID': 3,
                     'code': 101,
                     'product_name': 'xyz',
                     'ingredients_text': 'xyz',
                     'quantity': 'xyz',
                     'brands': 'xyz',
                     'brands_tags': 'xyz',
                     'categories': 'xyz',
                     'categories_tags': 'xyz',
                     'categories_en': 'xyz',
                     'countries': 'xyz',
                     'countries_tags': 'xyz',
                     'countries_en': 'xyz',
                     'image_url': 'xyz',
                     'image_small_url': 'xyz',
                     'image_ingredients_url': 'xyz',
                     'image_ingredients_small_url': 'xyz',
                     'image_nutrition_url': 'xyz',
                     'image_nutrition_small_url': 'xyz',
                     'User_ID': 2},
                    {'productID': 4,
                     'code': 702,
                     'product_name': 'xyz',
                     'ingredients_text': 'xyz',
                     'quantity': 'xyz',
                     'brands': 'xyz',
                     'brands_tags': 'xyz',
                     'categories': 'xyz',
                     'categories_tags': 'xyz',
                     'categories_en': 'xyz',
                     'countries': 'xyz',
                     'countries_tags': 'xyz',
                     'countries_en': 'xyz',
                     'image_url': 'xyz',
                     'image_small_url': 'xyz',
                     'image_ingredients_url': 'xyz',
                     'image_ingredients_small_url': 'xyz',
                     'image_nutrition_url': 'xyz',
                     'image_nutrition_small_url': 'xyz',
                     'User_ID': 2}]
        self.UserID = 2
        result = _get_wish_list_all(self.UserID)
        self.assertEqual(expected, result)


"""
The following test is to delete data first before later testing a function that adds data in the class after it.

I had to have this following function in a seperate class as for some reason when I test delete functions in the same
class as other functions such as add functions they interfere with each other and mess up the tests as they don't 
seem to run in the order they are written.
"""



class TestMockFrontEndDeleteDataFirst(unittest.TestCase):
    def setUp(self):
        self.mock = MockFrontEnd("cfg_project")


    @patch('builtins.input', side_effect=[1, 6])
    def test_8_delete_wish_list_item_before_re_adding(self, mock_inputs):
        expected = "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}".format(
            1, 6, {})
        result = self.mock.deleting_wishlist_item()
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


    def test_9_add_new_wishlist(self):
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
    def test_10_verify_wish_list_item(self, mock_inputs):
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
    def test_11_verify_wish_list(self, mock_inputs):
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
    def test_12_add_new_wishlist_mocked_values(self, mock_wish_list_dict):
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
    def test_13_delete_wish_list_item(self, mock_inputs):
        expected = "The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}".format(
            2, 2, {})
        result = self.mock.deleting_wishlist_item()
        self.assertEqual(expected, result)


    @patch('builtins.input', side_effect=[3])
    def test_14_delete_wish_list_all(self, mock_inputs):
        expected = expected = "The entire wishlist for User ID: {}, has now been deleted. The wishlist is now empty as such: {}".format(3, {})
        result = self.mock.deleting_wishlist()
        self.assertEqual(expected, result)

"""
The following class is to re-add data that was just deleted by testing delete functions from wishlist_main file
"""



class ReAddingData(unittest.TestCase):


    def test_15_re_add_mock_wish_list(self):
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

# The following code is to re-add two records as I deleted all of wishlist for user ID 3

    def test_16_re_add_wish_list_1(self):
        self.ProductID = 1
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
        self.UserID = 3
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
        expected = [{"User_ID": 3,
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
                     "quantity": "xyz"}]
        self.assertEqual(expected, result)


    def test_17_re_add_wish_list_2(self):
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
        self.UserID = 3
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
        expected = [{"User_ID": 3,
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

"""
I put the following code even though they are also testing the API into a seperate class, as the tests don't seem to be
running in order they are written so these functions were messing with other tests 


This following class tests the actual API and runs unit tests related to deleting data such as deleting the individual
wishlist item and entire wishlist 

I readded the data after running the delete tests

"""



class TestWishListApiDbDeletingUsers(unittest.TestCase):


    def test_18_delete_wish_list_item(self):
        self.UserID = 2
        self.ProductID = 2
        expected = ("Wishlist item for User_ID: {} and "
        "productID: {} does not exist").format(self.UserID, self.ProductID)
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

# The following test re-adds the data, I decided to do it as a test to make sure the right data was indeed re-added


    def test_19_re_add_wish_list(self):
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


    def test_20_delete_wish_list_all(self):
        self.UserID = 3
        expected = "Wishlist item for this User_ID: {} does not exist".format(self.UserID)
        result = delete_wishlist(self.UserID)
        self.assertEqual(expected, result)

# The following test re-adds the data, I decided to do it as a test to make sure the right data was indeed re-added


    def test_21_re_add_wish_list_1(self):
        self.ProductID = 1
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
        self.UserID = 3
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
        expected = [{"User_ID": 3,
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
                     "quantity": "xyz"}]
        self.assertEqual(expected, result)


    def test_22_re_add_wish_list_2(self):
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
        self.UserID = 3
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
        expected = [{"User_ID": 3,
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



"""
This following code will hopefully make my tests run in order
"""

if __name__ == '__main__':
    unittest.main()

