from flask import Flask, jsonify, request
from wishlist_db_utils import _get_wish_list_all, add_wish_list, _get_wish_list_individual


app = Flask(__name__)


@app.route('/wishlist/<int:user_id>', methods=['GET'])
def get_wishlist(user_id):
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist)

@app.route('/wishlist/<int:user_id>/<int:product_id>', methods=['GET'])
def get_wishlist_item(user_id, product_id):
    wishlist_item = _get_wish_list_individual(user_id, product_id)
    return jsonify(wishlist_item)



@app.route('/wishlist',methods = ['PUT'])
def add_wish_list_put():
    wishlist_dict = request.get_json()
    add_wish_list(
        Username = wishlist_dict['username'],
        UserID = wishlist_dict['UserID'], 
        ProductID = wishlist_dict['wishlist']['ProductID'], 
        Code_Wish = wishlist_dict['wishlist']['Code_Wish'], 
        Product_name = wishlist_dict['wishlist']['Product_name'], 
        Quantity = wishlist_dict['wishlist']['Quantity'],
        Brands = wishlist_dict['wishlist']['Brands'], 
        Brands_tags = wishlist_dict['wishlist']['Brands_tags'], 
        Categories_Tags = wishlist_dict['wishlist']['Categories_Tags'], 
        Countries_en = wishlist_dict['wishlist']['Countries_en'], 
        Ingredients_Text = wishlist_dict['wishlist']['Ingredients_Text'], 
        Image_url = wishlist_dict['wishlist']['Image_url'], 
        Image_Small_url = wishlist_dict['wishlist']['Image_Small_url'], 
        Image_Ingredients_url = wishlist_dict['wishlist']['Image_Ingredients_url'],
        Image_Ingredients_Small_url = wishlist_dict['wishlist']['Image_Ingredients_Small_url'], 
        Image_Nutrition_url = wishlist_dict['wishlist']['Image_Nutrition_url'], 
        Image_Nutrition_Small_url = wishlist_dict['wishlist']['Image_Nutrition_Small_url']

    )

    return wishlist_dict
