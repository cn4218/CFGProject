import requests
import json

"""
This file serves to test the wishlist  and mock test input
"""

def add_new_wishlist():

    wishlistdict = {'username': 'sarah123',
                    'User_ID': 3,
                    'wishlist': {
                        'productID': 6,
                        'code': '62263436',
                        'product_name': 'Huile de massage larnica',
                        'ingredients_list': 'helianthus annuus (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles',
                        'quantity': '100 ml',
                        'brands': 'Weleda',
                        'brands_tags': 'weleda',
                        'categories': 'Skincare',
                        'categories_tags': r'en:body,en:body-oils,fr:huile-de-massage',
                        'categories_en': r'Body,Body-oils,fr:huile-de-massage',
                        'countries': 'France',
                        'countries_tags': 'en:france',
                        'countries_en': 'France',
                        'image_url': 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg',
                        'image_small_url': 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg',
                        'image_ingredients_url': '',
                        'image_ingredients_small_url': '',
                        'image_nutrition_url': '',
                        'image_nutrition_small_url': ''
                    }}

    result = requests.post(
        "http://127.0.0.1:5001/wishlist/add",

        headers={"content-type": "application/json"},
        data=json.dumps(wishlistdict),
    )

    return result.json()

def _get_wish_list_individual(User_ID, productID):
    result = requests.get(
        "http://127.0.0.1:500/wishlist/{}/{}".format(User_ID, productID),
        # headers restrict the type of data to be received
        headers={"content-type": "application/json"},
    )
    return result.json()

def _get_wish_list_all(User_ID):
    result = requests.get(
        "http://127.0.0.1:500/wishlist/{}/".format(User_ID),
        headers={"content-type": "application/json"},
    )
    return result.json()

def delete_wishlist_item(User_ID, productID):
    result = requests.get(
        "http://127.0.0.1:500/delete/{}/{}".format(User_ID, productID),
        headers={"content-type": "application/json"},
    )
    return result.json()

def delete_wishlist(User_ID):
    result = requests.get(
        "http://127.0.0.1:500/delete/{}/".format(User_ID),
        headers={"content-type": "application/json"},
    )
    return result.json()


class MockFrontEnd:
    def welcome_message(self):
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()

    def verify_wish_list_item(self):
        self.User_ID = input('What is your User ID')
        self.productID = input('What is your product ID?')
        verify_wishlist_item = _get_wish_list_individual(self.User_ID, self.productID)
        return verify_wishlist_item

    def verify_wish_list(self):
        self.User_ID = input('What is your User ID')
        verify_wishlist = _get_wish_list_all(self.User_ID)
        return verify_wishlist


    def deleting_wishlist_item(self):
        self.User_ID = input('What is your User ID')
        self.productID = input('What is your product ID?')
        dict = delete_wishlist_item(self.User_ID, self.productID)
        if dict == {}:
            print('Wishlist item successfully deleted')
        return dict

    def deleting_wishlist(self):
        self.User_ID = input('What is your User ID')
        dict = delete_wishlist(self.User_ID)
        if dict == {}:
            print('Wishlist item successfully deleted')
        return dict


def run():
    mock = MockFrontEnd()
    mock.welcome_message()
    while True:
        answer_wishlist_add = input('Do you want to add to the wishlist? y/n')
        if answer_wishlist_add == 'y':
            add_new_wishlist()
            continue
        answer_wishlist_item = input('Do you wish to get a wishlist item? y/n')
        if answer_wishlist_item == 'y':
            mock.verify_wish_list_item()
            continue
        answer_wishlist = input('Do you wish to retrieve the wishlist? y/n')
        if answer_wishlist == 'y':
            mock.verify_wish_list()
            continue
        answer_delete_wishlist_item = input('Do you wish to delete a wishlist item? y/n')
        if answer_delete_wishlist_item == 'y':
            mock.deleting_wishlist_item()
            continue
        answer_delete_wishlist = input('Do you wish to delete the entire wishlist? y/n')
        if answer_delete_wishlist == 'y':
            mock.deleting_wishlist()
            break
        break

if __name__ == '__main__':
    run()
