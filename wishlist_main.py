import requests
import json
from wishlist_db_utils import _map_values

"""
This file serves to test the wishlist  and mock test input
"""

def add_new_wishlist():

    wishlistdict = {"username": "sarah123",
                    "User_ID": 1,
                    "wishlist": {
                        "productID": 6,
                        "code": "62263436",
                        "product_name": "Huile'' de massage larnica",
                        "ingredients_text": "helianthus 'annuus' (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles",
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

    return result.json()

def _get_wish_list_individual(User_ID, productID):
    result = requests.get(
        "http://127.0.0.1:5001/wishlist/{}/{}".format(User_ID, productID),
        # headers restrict the type of data to be received
        headers={"content-type": "application/json"},
    )
    return result.json()

def _get_wish_list_all(User_ID):
    result = requests.get(
        "http://127.0.0.1:5001/wishlist/{}/".format(User_ID),
        headers={"content-type": "application/json"},
    )
    return result.json()

def delete_wishlist_item(User_ID, productID):
    result = requests.get(
        "http://127.0.0.1:5001/delete/{}/{}".format(User_ID, productID),
        headers={"content-type": "application/json"},
    )
    return result.json()

def delete_wishlist(User_ID):
    result = requests.get(
        "http://127.0.0.1:5001/delete/{}/".format(User_ID),
        headers={"content-type": "application/json"},
    )
    return result.json()


def welcome_message():
    print("############################")
    print("Hello, welcome to Cosmo")
    print("############################")
    print()


def verify_wish_list_item():
    User_ID = input('What is your User ID ')
    productID = input('What is your product ID? ')
    data = (_get_wish_list_individual(User_ID, productID))
    data_dict = json.loads(data)['User_ID']['productID']
    # data_string = json.dumps(data_dict)
    # convert single-entry dictionaries to tuples
    data_2 = [list(data_dict.items())[0] for data in data_dict]
    # filter the courses based on the condition
    filtered_data = list(filter(lambda data: data[1] > 5, data_2))
    return filtered_data


def verify_wish_list():
    User_ID = input('What is your User ID ')
    data = (_get_wish_list_all(User_ID))
    data_dict = json.loads(data)
    data_string = json.dumps(data_dict)
    return data_string


def deleting_wishlist_item():
    User_ID = input('What is your User ID')
    productID = input('What is your product ID? ')
    dict = delete_wishlist_item(User_ID, productID)
    if dict == {}:
        print('Wishlist item successfully deleted')
    return dict


def deleting_wishlist(self):
    User_ID = input('What is your User ID ')
    dict = delete_wishlist(User_ID)
    if dict == {}:
        print('Wishlist item successfully deleted')
    return dict




def run():
    welcome_message()
    while True:
        answer_wishlist_add = input('Do you want to add to the wishlist? y/n ')
        if answer_wishlist_add == 'y':
            add_new_wishlist()
        answer_wishlist_item = input('Do you wish to get a wishlist item? y/n ')
        if answer_wishlist_item == 'y':
            verify_wish_list_item()
        answer_wishlist = input('Do you wish to retrieve the wishlist? y/n ')
        if answer_wishlist == 'y':
            verify_wish_list()
        answer_delete_wishlist_item = input('Do you wish to delete a wishlist item? y/n' )
        if answer_delete_wishlist_item == 'y':
            deleting_wishlist_item()
        answer_delete_wishlist = input('Do you wish to delete the entire wishlist? y/n ')
        if answer_delete_wishlist == 'y':
            deleting_wishlist()
            break
        break

if __name__ == '__main__':
    # add_new_wishlist()
    run()

