import requests
import json

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from CFGProject.scripts.wishlist_db_utils import _connect_to_db, DbConnectionError
from CFGProject.scripts.config import USER, PASSWORD, HOST


"""
FUNCTIONS CONTAINED IN THIS FILE:
class MockFrontEnd:
__init__(self, db_name)
add_new_wishlist(self)
get_wish_list_individual(self, User_ID, productID)
_get_wish_list_all(self, User_ID)
delete_wishlist_item(self, User_ID, productID)
delete_wishlist(self, User_ID)
welcome_message(self)
verify_wish_list_item(self)
verify_wish_list(self)
deleting_wishlist_item(self)
deleting_wishlist(self)

run()
"""


class MockFrontEnd:

    def __init__(self, db_name):
        """
        Inititiates
        Parameters
        ----------
        db_name: str
            Identifier to search the MySQL database to find the name of the database to form the connection. db_name is the
            name of the database.
        """
        self.db_name = db_name
        self.db_utils = _connect_to_db(self.db_name)

    def add_new_wishlist(self):
        """
        Mocks API endpoint for add new wishlist function
        Returns
        -------
        result.json() : Either:
        wishlist: dict
            wishlist dictionary for the new wishlist item that's been added
        OR:
        answer: str
            string containing message on why the wishlist item hasn't been added
        """
        wishlistdict = {"username": "sarah",
                        "User_ID": 1,
                        "wishlist": {
                        "productID": 6,
                        "code": "62263436",
                        "product_name": "Huile de massage à l'arnica",
                        "ingredients_text": "helianthus annuus (sunflower) seed oil, olea europaea ' '(olive) fruit oil, fragrance*, arnica montana flower ' 'extract, betula alba leaf extract, limonene*,  ' 'linaloo*, geraniol*, coumarin* *compose present dans ' 'les huiles essentielles naturelles",
                        "quantity": "100 ml",
                        "brands": "Weleda",
                        "brands_tags": "weleda",
                        "categories": "Corps,Huiles pour le corps,Huile de massage",
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

        result = requests.get(
            "http://127.0.0.1:5001/wishlist/add/{}/{}".format(wishlistdict["User_ID"], (wishlistdict["wishlist"]["productID"]),

            headers={"content-type": "application/json"},
            data=json.dumps(wishlistdict),
        ))
        print(result)

        return result.json()

    def _get_wish_list_individual(self, User_ID, productID):
        """
        Function with API endpoint that retrieves the specific wishlist item for given user and product id using
         _get_wish_list_individual from wishlist_db_utils
        Parameters
        ----------
        user_id : int
            id of user
        product_id : int
            id of product to be retrieved
        Returns
        -------
        wishlist_item : list or str
            Either:
            1 - list conaining product dictionary from wishlist
            2 - string detailing why the product dictionary hasn't been retrieved
        """
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/{}/{}".format(User_ID, productID),
            # headers restrict the type of data to be received
            headers={"content-type": "application/json"},
        )
        return result.json()

    def _get_wish_list_all(self, User_ID):
        """
        This function fetches all the wishlist items corresponding to one
        particluar user and returns a jsonified list of dictionaries when a
        request is made to this endpoint
        Parameters
        ----------
        user_id : int
            id of user
        Returns
        --------
        wishlist : list or str
            1 - list of product dictionaries within wishlist
            2 - string returned for when wishlist is empty
        """
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/{}".format(User_ID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def delete_wishlist_item(self, User_ID, productID):
        """
        Function API endpoint that deletes an individual product item within a wishlist by calling the delete_wishlist_item in wishlist_db_utils
        Parameters
        ----------
        user_id : int
            id of user
        product_id : int
            id of product to be deleted
        Returns
        -------
        wishlist_item : str
            string containig description of whether the item has been successfully deleted from the sql wish_list table or not
        """
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/delete/{}/{}".format(User_ID, productID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def delete_wishlist(self, User_ID):
        """
        API endpoint that uses delete_wishlist from wishlist_db_utils to delete all products within a wishlist for an user
        Parameters
        ----------
        user_id : int
            id for user
        Returns
        -------
        empty_user_wishlist : str
            string containig information detailing whether the wishlist has been deleted or if there is an issue deleting it
        """
        result = requests.get(
            "http://127.0.0.1:5001/wishlist/delete/{}".format(User_ID),
            headers={"content-type": "application/json"},
        )
        return result.json()

    def welcome_message(self):
        """
        Prints a welcome message
        """
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()

    def verify_wish_list_item(self):
        """
        Function that uses an UserID and ProductID that was mocked into this function to search the wishlist
        table in the MySQL database for a wishlist item, so as to retrieve it, that exists so as to make sure the
        wishlist item is printed back to the user in a readable format.
               ----------
        User_ID : int
            id for user
        productID : int
            product is
        Returns
        -------
        data : list
            List containing the dictionary corresponding to that wishlist item
        """
        self.User_ID = input('What is your User ID ')
        self.productID = input('What is your product ID? ')
        self.data = self._get_wish_list_individual(self.User_ID, self.productID)
        return self.data

    def verify_wish_list(self):
        """
        Function that uses an UserID that was mocked into this function to search the wishlist table in the MySQL
        database for an entire wishlist, so as to retrieve it, that exists so as to make sure the entire wishlist is
        printed back to the user in a readable format.
               ----------
        User_ID : int
            id for user
        Returns
        -------
        data : list
            List containing the dictionary corresponding to that wishlist
        """
        self.User_ID = input('What is your User ID ')
        self.data = self._get_wish_list_all(self.User_ID)
        return self.data

    def deleting_wishlist_item(self):
        """
        This function deletes a wishlist item using the delete function from the wishlist_main file. Uses an UserID and
        ProductID that is mocked into this function to search the wishlist table in the MySQL database for a wishlist
        item, so as to delete it, that exists so as to make sure the correct statement is printed back to the user to
        signify that a wishlist item has indeed been deleted.
               ----------
        User_ID : int
            id for user
        productID : int
            product is
        Returns
        -------
        dict : dictionary
            Dictionary corresponding to the deleted wishlist item
        """
        self.User_ID = input('What is your User ID ')
        self.productID = input('What is your product ID? ')
        self.dict = self.delete_wishlist_item(self.User_ID, self.productID)
        if self.dict == {}:
            print('Wishlist item successfully deleted')
        return self.dict

    def deleting_wishlist(self):
        """
        This function deletes an entire wishlist using the delete function from the wishlist_main file. Uses an UserID
        that is mocked into this function to search the wishlist table in the MySQL database for a wishlist, so as to
        delete it, that exists so as to make sure the correct statement is printed back to the user to signify that a
        wishlist has indeed been deleted.
               ----------
        User_ID : int
            id for user
        Returns
        -------
        dict : dictionary
            Dictionary corresponding to the deleted wishlist item
        """
        self.User_ID = input('What is your User ID ')
        self.dict = self.delete_wishlist(self.User_ID)
        if self.dict == {}:
            print('Wishlist item successfully deleted')
        return self.dict


def run():
    """
    Run function that mocks the UI. It takes in the MockFrontEnd class and gives it the database name 'cfg_project'
    and then mocks the UI.
    """
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


