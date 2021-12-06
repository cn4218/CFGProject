from flask import Flask, jsonify, request
from wishlist_db_utils import _get_wish_list_all, add_wish_list, _get_wish_list_individual, delete_wishlist_individual, delete_wishlist


app = Flask(__name__)

## function that connects to db utils and retrieves list of dictionaries of products in a wishlist for a user id 
@app.route('/wishlist/<int:user_id>', methods=['GET'])
def get_wishlist(user_id):
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist)  ##returns list of dictionaries

## function that connects to db utils and retrieves one specific product from wishlist using user id and product id
@app.route('/wishlist/<int:user_id>/<int:product_id>', methods=['GET'])   ## not too sure if need /<int:product_id> in the url here, depends on ui
def get_wishlist_item(user_id, product_id):
    wishlist_item = _get_wish_list_individual(user_id, product_id)
    return jsonify(wishlist_item)  ##returns one dicionary


## function that formats dictionary as entries to put in db utils function, this adds an item to a users wishlist
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

    return jsonify(wishlist_dict)   ## dictionary containing all above values

## deletes specific product from a users wishlist using db utils
@app.route('/wishlist/<int:user_id>', methods=['DELETE'])
def delete_wislist_item(user_id,product_id):
    empty_wishlist_item = delete_wishlist_individual(user_id,product_id)
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist)

## app route that deletes entire wishlist for user
@app.route('/wishlist/<int:user_id>', methods = ['DELETE'])
def delete_entire_wishlist(user_id):
    empty_user_wishlist = delete_wishlist(user_id)
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist) ## this should be an empty list so can just return an empty list instead 


if __name__ == '__main__':
    app.run(debug=True)
