import requests
import json
from wishlist_db_utils import _connect_to_db, DbConnectionError
import config

"""
This file serves to test the wishlist  and mock test input
"""

class MockFrontEnd:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_utils = _connect_to_db(self.db_name)

    def add_new_wishlist(self):

        wishlistdict = {"username": "sarah",
                        "User_ID": 1,
                        "wishlist": {
                            "productID": 6,
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

        result = requests.post(
            "http://127.0.0.1:5001/wishlist/add",

            headers={"content-type": "application/json"},
            data=json.dumps(wishlistdict),
        )
        print(result)

        return result.json()

    def _get_wish_list_individual(self, User_ID, productID):
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/{}/{}".format(User_ID, productID),
            # headers restrict the type of data to be received
            headers={"content-type": "application/json"},
        )
        return result.json()

    def _get_wish_list_all(self, User_ID):
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/{}".format(User_ID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def delete_wishlist_item(self, User_ID, productID):
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/delete/{}/{}".format(User_ID, productID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def delete_wishlist(self, User_ID):
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/delete/{}".format(User_ID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def welcome_message(self):
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()

    def verify_wish_list_item(self):
        self.User_ID = input('What is your User ID ')
        self.productID = input('What is your product ID? ')
        data = self._get_wish_list_individual(self.User_ID, self.productID)
        return data

    def verify_wish_list(self):
        self.User_ID = input('What is your User ID ')
        data = self._get_wish_list_all(self.User_ID)
        return data

    def deleting_wishlist_item(self):
        self.User_ID = input('What is your User ID ')
        self.productID = input('What is your product ID? ')
        dict = self.delete_wishlist_item(self.User_ID, self.productID)
        if dict == {}:
            print('Wishlist item successfully deleted')
        return dict

    def deleting_wishlist(self):
        self.User_ID = input('What is your User ID ')
        dict = self.delete_wishlist(self.User_ID)
        if dict == {}:
            print('Wishlist item successfully deleted')
        return dict




def run():
    mock = MockFrontEnd('cfg_project')
    mock.welcome_message()
    while True:
        answer_wishlist_add = input('Do you want to add to the wishlist? y/n ')
        if answer_wishlist_add == 'y':
            res = mock.add_new_wishlist()
            print(res)
        answer_wishlist_item = input('Do you wish to get a wishlist item? y/n ')
        if answer_wishlist_item == 'y':
            res2 = mock.verify_wish_list_item()
            print(res2)
        answer_wishlist = input('Do you wish to retrieve the wishlist? y/n ')
        if answer_wishlist == 'y':
            res3 = mock.verify_wish_list()
            print(res3)
        answer_delete_wishlist_item = input('Do you wish to delete a wishlist item? y/n ' )
        if answer_delete_wishlist_item == 'y':
            res4 = mock.deleting_wishlist_item()
            print(res4)
        answer_delete_wishlist = input('Do you wish to delete the entire wishlist? y/n ')
        if answer_delete_wishlist == 'y':
            res5 = mock.deleting_wishlist()
            print(res5)
        break

if __name__ == '__main__':
    run()
