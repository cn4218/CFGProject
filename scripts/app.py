from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from obf_db_utils import get_proper_ingredients_list, get_productids_containing , get_products_by_ids
from wishlist_db_utils import _get_wish_list_all, add_wish_list, delete_wishlist_item
from user_db_utils import add_user, _get_user, delete_user, verify_login, update_user



app = Flask(__name__)
CORS(app) # Cross Origin Resource Sharing   # Required for the to frontend send requests
list_ = []

#OBF 
##################################################################################################

# @app.route("/")
# def serve_home_page():
#     return render_template("home.html")



@app.route("/Search", methods=['POST'])
def find_products():
    """
    The front end sends a post request to the /Search endpoint and this post request also contains 
    data (the ingredient input). This is then passed to the get_proper_ingredients_list function 
    which returns a list of product dictionaries which is returned to the sender (frontend) as a
    "response"
    """
    ingredient_input = request.get_json()
    print(ingredient_input)
    
    list_of_products = get_proper_ingredients_list(ingredient_input)
    list_.clear()
    list_.append(list_of_products)

    # store_results(list_of_products)

    return jsonify(list_of_products)


@app.route("/Search", methods=['GET']) 
def return_list():
    """
    Returns a list of one element and that element is a list of dictionaries
    """
    return jsonify(list_)


@app.route("/results", methods=['GET'])
def get_results():
    """
    This function calls an obf_db_utils function, fetch_results() that returns a list of product results 
    and returns a jsonified version of it to the frontend 
    """


##########################################################################################################################################################
# At the moment, wishlist code will not work unless you have the dummy data in the user_info table:
# 10234,'sample_name','sample_user','sample@gmail.com'


new_list = []
# Need to make sure product_id going in here  
#string for now because we don't yet know
@app.route('/wishlist/add/<int:user_id>/<string:product_id>',methods = ['GET']) #now we know we are getting information
def add_wish_list_func(user_id,product_id):
    # user_product_id_dict =  request.get_json()

    


    # print(user_product_id_dict)
    # print(user_product_id_dict['user_id'])
    # print(user_product_id_dict['product_id'])

    # user_id = user_product_id_dict['user_id']
    # product_id = user_product_id_dict['product_id']
    # new_list.clear()
    # new_list.append(user_product_id_dict)

    try:
        print("I am here")
        product_id = int(product_id.strip())
        user_id = int(user_id) #check if there is any situation where user ID wouldn't be an int 
    
    except ValueError:
        return jsonify("Error")
    
    except Exception:
        return jsonify("Error")
    else:
        product = (get_products_by_ids([product_id]))[0]
        print(product)

        
        print(type(product_id))
        wishlist_dict = {}
        wishlist_dict['UserID'] = user_id
        wishlist_dict['wishlist'] = product 
        ## { "UserId": number , "wishlist": { product info dictionary }}
        print(wishlist_dict)

        add_wish_list(
            ProductID = wishlist_dict['wishlist']['productID'], 
            Code_Wish = wishlist_dict['wishlist']['code'], 
            Product_name = wishlist_dict['wishlist']['product_name'], 
            Ingredients_Text = wishlist_dict['wishlist']['ingredients_text'], 
            Quantity = wishlist_dict['wishlist']['quantity'],
            Brands = wishlist_dict['wishlist']['brands'], 
            Brands_tags = wishlist_dict['wishlist']['brands_tags'], 
            Categories = wishlist_dict['wishlist']['categories'], 
            Categories_Tags = wishlist_dict['wishlist']['categories_tags'], 
            Categories_En = wishlist_dict['wishlist']['categories_en'],
            Countries = wishlist_dict['wishlist']['countries'],
            Countries_Tags = wishlist_dict['wishlist']['countries_tags'],
            Countries_en = wishlist_dict['wishlist']['countries_en'],
            Image_url = wishlist_dict['wishlist']['image_url'], 
            Image_Small_url = wishlist_dict['wishlist']['image_small_url'], 
            Image_Ingredients_url = wishlist_dict['wishlist']['image_ingredients_url'],
            Image_Ingredients_Small_url = wishlist_dict['wishlist']['image_ingredients_small_url'], 
            Image_Nutrition_url = wishlist_dict['wishlist']['image_nutrition_url'], 
            Image_Nutrition_Small_url = wishlist_dict['wishlist']['image_nutrition_small_url'],
            UserID = wishlist_dict['UserID']

        )
        return jsonify("Added")





# @app.route('/wishlist/add', methods=['GET']) 
# def return_short_dict():
#     return jsonify("Added") 

# @app.route('/wishlist', methods=['POST'])   # {"user_id: user_id"}
# def get_wishlist():
#     """
#     This function fetches all the wishlist items corresponding to one
#     particluar user and returns a jsonified list of dictionaries when a 
#     request is made to this endpoint
#     """

#     user_id_input = request.get_json()
#     print(type(user_id_input))
#     user_id = user_id_input["user_id"]
#     wishlist = _get_wish_list_all(user_id)
#     print("I am now printin")
#     print(wishlist)
#     return jsonify(wishlist)



@app.route('/wishlist/<int:user_id>', methods=['GET'])   # {"user_id: user_id"}
def get_wishlist(user_id):
    """
    This function fetches all the wishlist items corresponding to one
    particluar user and returns a jsonified list of dictionaries when a 
    request is made to this endpoint
    """

    # user_id_input = request.get_json()
    # print(type(user_id_input))
    # user_id = user_id_input["user_id"]
    wishlist = _get_wish_list_all(user_id)
    print("I am now printin")
    # print(wishlist)
    return jsonify(wishlist)



@app.route('/wishlist/delete/<int:user_id>/<int:product_id>', methods=['GET'])
def delete_wislist_individual(user_id, product_id):
    empty_wishlist_item = delete_wishlist_item(user_id,product_id)
    return jsonify(empty_wishlist_item)



#USER INFO ENDPOINTS
###############################################################################################################################
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    """ gets the profile for one user"""
    user = _get_user(user_id)
    return jsonify(user[0]) #Chizu: now it returns a single dictionary instead of list with one element that is a dictionary 



@app.route("/login/<string:username>/<string:email>", methods=["GET"])
def verify_login_api(username,email):
    login_dict = request.get_json()

    answer = verify_login( #answer is either {"verify": False}, {"verify": True, "user_id": user_id} or Duplicate users
        username = username,
        email_address = email
    )

    return jsonify(answer)





if __name__ == '__main__':
    app.run(debug=True, port=5001)








#pass the ingredient input into the function that finds the list of product dictionaries 
#then pass that list as a response to the sender of the post (your client)
#since the function in question has issues at the moment, so fix it first 


