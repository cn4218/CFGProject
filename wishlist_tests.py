from unittest.mock import patch
from unittest import TestCase, main
from wishlist_main import MockFrontEnd
from wishlist_db_utils import DbConnectionError, _connect_to_db, exception_handler, exception_handler_wish, exception_record_exists, _map_values, add_wish_list, _get_wish_list_individual, _get_wish_list_all, delete_wishlist_item, delete_wishlist


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
"""

class TestWishListApiDb(TestCase):
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

    def test_delete_wish_list_item(self):
        self.UserID = 1
        self.ProductID = 2
        expected = 'The wish list item for User ID: {} and  Product ID: {}, has now been deleted. This wishlist record is now empty: {}'.format(self.UserID, self.ProductID, {}))
        result = delete_wishlist_item(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_delete_wish


    def test_get_wish_list_item_if_exists(self):
        expected = [
  {
    "User_ID": 1,
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
        self.UserID = 1
        self.ProductID = 2
        result = _get_wish_list_individual(self.UserID, self.ProductID)
        self.assertEqual(expected, result)

    def test_get_wish_list_all(self):
        expected = [
  {
    "User_ID": 1,
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
  },
  {
    "User_ID": 1,
    "brands": "Weleda",
    "brands_tags": "weleda",
    "categories": "Skincare",
    "categories_en": "Body,Body-oils,fr:huile-de-massage",
    "categories_tags": "en:body,en:body-oils,fr:huile-de-massage",
    "code": 62263436,
    "countries": "France",
    "countries_en": "France",
    "countries_tags": "en:france",
    "image_ingredients_small_url": "",
    "image_ingredients_url": "",
    "image_nutrition_small_url": "",
    "image_nutrition_url": "",
    "image_small_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg",
    "image_url": "https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg",
    "ingredients_text": "helianthus 'annuus' (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *compos\u00e9 pr\u00e9sent dans les huiles essentielles naturelles",
    "productID": 6,
    "product_name": "Huile'' de massage larnica",
    "quantity": "100 ml"
  }
]
        self.UserID = 1
        result = _get_wish_list_all(self.UserID)
        self.assertEqual(expected, result)



if __name__ == "__main__":
    main()