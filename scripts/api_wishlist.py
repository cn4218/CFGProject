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
def add_wish_list():
    wishlist = request.get_json()
    add_wish_list(
        UserID = wishlist['UserID'], 
        ProductID = wishlist['ProductID'], 
        Code_Wish = wishlist['Code_Wish'], 
        Product_name = wishlist['Product_name'], 
        Quantity = wishlist['Quantity'],
        Brands = wishlist['Brands'], 
        Brands_tags = wishlist['Brands_tags'], 
        Categories_Tags = wishlist['Categories_Tags'], 
        Countries_en = wishlist['Countries_en'], 
        Ingredients_Text = wishlist['Ingredients_Text'], 
        Image_url = wishlist['Image_url'], 
        Image_Small_url = wishlist['Image_Small_url'], 
        Image_Ingredients_url = wishlist['Image_Ingredients_url'],
        Image_Ingredients_Small_url = wishlist['Image_Ingredients_Small_url'], 
        Image_Nutrition_url = wishlist['Image_Nutrition_url'], 
        Image_Nutrition_Small_url = wishlist['Image_Nutrition_Small_url']

    )

    return wishlist
