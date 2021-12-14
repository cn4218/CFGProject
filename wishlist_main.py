import requests
import json

"""
This file serves to test the wishlist  and mock test input
"""

def add_new_wishlist():

    wishlistdict = {'username': 'sarah123',
                    'UserID': 3,
                    'wishlist': {
                        'ProductID': 6,
                        'Code_Wish': '62263436',
                        'Product_name': 'Huile de massage larnica',
                        'Quantity': '100 ml',
                        'Brands': 'Weleda',
                        'Brands_tags': 'weleda',
                        'Categories': 'Skincare',
                        'Categories_Tags': r'en:body,en:body-oils,fr:huile-de-massage',
                        'categories_en': r'Body,Body-oils,fr:huile-de-massage',
                        'countries': 'France',
                        'Countries_Tags': 'en:france',
                        'Countries_en': 'France',
                        'Ingredients_Text': 'helianthus annuus (sunflower) seed oil, olea europaea (olive) fruit oil, fragrance*, arnica montana flower extract, betula alba leaf extract, limonene*,  linaloo*, geraniol*, coumarin* *composé présent dans les huiles essentielles naturelles',
                        'Image_url': 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.400.jpg',
                        'Image_Small_url': 'https://static.openbeautyfacts.org/images/products/000/006/226/3436/front_fr.3.200.jpg',
                        'Image_Ingredients_url': '',
                        'Image_Ingredients_Small_url': '',
                        'Image_Nutrition_url': '',
                        'Image_Nutrition_Small_url': ''
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

# if __name__ == '__main__':
#     add_new_wishlist()