from flask import Flask, jsonify, request
from wishlist_db_utils import _get_wish_list_all, add_wish_list, _get_wish_list_individual, delete_wishlist_item, delete_wishlist


app = Flask(__name__)




@app.route('/wishlist/<int:user_id>', methods=['GET'])   ##success
def get_wishlist(user_id):
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist)


@app.route('/wishlist/<int:user_id>/<int:product_id>', methods=['GET'])  ##success
def get_wishlist_item(user_id, product_id):
    wishlist_item = _get_wish_list_individual(user_id,product_id)
    return jsonify(wishlist_item)


@app.route('/wishlist/add',methods = ['POST'])
def add_wish_list_func():
    wishlist_dict = request.get_json()
    add_wish_list(
        ProductID=wishlist_dict['wishlist']['productID'],
        Code_Wish=wishlist_dict['wishlist']['code'],
        Product_name=wishlist_dict['wishlist']['product_name'],
        Ingredients_Text=wishlist_dict['wishlist']['ingredients_text'],
        Quantity=wishlist_dict['wishlist']['quantity'],
        Brands=wishlist_dict['wishlist']['brands'],
        Brands_tags=wishlist_dict['wishlist']['brands_tags'],
        Categories=wishlist_dict['wishlist']['categories'],
        Categories_Tags=wishlist_dict['wishlist']['categories_tags'],
        Categories_En=wishlist_dict['wishlist']['categories_en'],
        Countries=wishlist_dict['wishlist']['countries'],
        Countries_Tags=wishlist_dict['wishlist']['countries_tags'],
        Countries_en=wishlist_dict['wishlist']['countries_en'],
        Image_url=wishlist_dict['wishlist']['image_url'],
        Image_Small_url=wishlist_dict['wishlist']['image_small_url'],
        Image_Ingredients_url=wishlist_dict['wishlist']['image_ingredients_url'],
        Image_Ingredients_Small_url=wishlist_dict['wishlist']['image_ingredients_small_url'],
        Image_Nutrition_url=wishlist_dict['wishlist']['image_nutrition_url'],
        Image_Nutrition_Small_url=wishlist_dict['wishlist']['image_nutrition_small_url'],
        UserID=wishlist_dict['User_ID']

    )

    return wishlist_dict

# use PUT for UPDATE options
# write a route for PUT

@app.route('/wishlist/delete/<int:user_id>/<int:product_id>')
def delete_wishlist_individual(user_id, product_id):
    empty_wishlist_item = delete_wishlist_item(user_id,product_id)
    return jsonify(empty_wishlist_item)


## app route that deletes entire wishlist for user
@app.route('/wishlist/delete/<int:user_id>')
def delete_entire_wishlist(user_id):
    empty_user_wishlist = delete_wishlist(user_id)
    return jsonify(empty_user_wishlist) ## this should be an empty list so can just return an empty list instead


if __name__ == '__main__':
    app.run(port = 5001,debug=True)