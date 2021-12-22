from flask import Flask, jsonify, request, render_template
from config import USER, PASSWORD, HOST
from flask_cors import CORS
from obf_db_utils import get_proper_ingredients_list, get_productids_containing , get_products_by_ids, fetch_results, store_results ,verify_product_id
from wishlist_db_utils import _get_wish_list_all, add_wish_list, delete_wishlist_item
from user_db_utils import dbConnection #importing the class only since all the methods are contained within it 
from pprint import pp 


app = Flask(__name__)
CORS(app) # Cross Origin Resource Sharing   # Required for the to frontend send requests
list_ = []

#OBF 
##################################################################################################

# @app.route("/")
# def serve_create_account_page():
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
    if isinstance(list_of_products,Exception):
        return jsonify('Query returns no search results')
    
    list_.append(list_of_products)

    store_results(list_of_products)
   
    return jsonify(list_of_products)


@app.route("/Search", methods=['GET']) 
def return_list():
    """
    Returns a list of one element and that element is a list of dictionaries
    """
    print("I am inside return list")
   
    return jsonify(list_)



@app.route("/Results", methods=['GET'])
def send_results():
    """
    Retrieves ssearch results for given search id
    """
    
    list_of_products = fetch_results(1)
    if isinstance(list_of_products,Exception):
        return jsonify([])

    return jsonify(list_of_products)


#Wishlist endpoints 
##########################################################################################################################################################
# At the moment, wishlist code will not work unless you have the dummy data in the user_info table:
# 10234,'sample_name','sample_user','sample@gmail.com'


new_list = []

@app.route('/wishlist/add/<int:user_id>/<string:product_id>',methods = ['GET']) #now we know we are getting information
def add_wish_list_func(user_id,product_id):
    
    try:
        
        product_id = int(product_id.strip())
        verify_product_id(product_id)
        user_id = int(user_id) 
        
    except ValueError:
        
        return jsonify("Error")
    
    except Exception:
        print("I am here")
        return jsonify("Error")
    else:
        product = (get_products_by_ids([product_id]))[0] #a single dictionary of product info 
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




@app.route('/wishlist/<int:user_id>', methods=['GET'])   
def get_wishlist(user_id):
    """
    This function fetches all the wishlist items corresponding to one
    particluar user and returns a jsonified list of dictionaries when a 
    request is made to this endpoint
    """
    wishlist = _get_wish_list_all(user_id)
    return jsonify(wishlist)



@app.route('/wishlist/delete/<int:user_id>/<int:product_id>', methods=['GET'])
def delete_wislist_individual(user_id, product_id):
    empty_wishlist_item = delete_wishlist_item(user_id,product_id)
    return jsonify(empty_wishlist_item)

#### used in wishlist_main.py
@app.route('/wishlist/<int:user_id>/<int:product_id>', methods=['GET'])  ##success
def get_wishlist_item(user_id, product_id):
    wishlist_item = _get_wish_list_individual(user_id,product_id)
    return jsonify(wishlist_item)

## app route that deletes entire wishlist for user
@app.route('/wishlist/delete/<int:user_id>')
def delete_entire_wishlist(user_id):
    empty_user_wishlist = delete_wishlist(user_id)
    return jsonify(empty_user_wishlist) ## this should be an empty list so can just return an empty list instead







#USER INFO ENDPOINTS
###############################################################################################################################
db_utils = dbConnection(PASSWORD) 
#creating instance of the dbConnection class in the user_db_utils.py file 


@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    """ gets the profile for one user"""
    user = db_utils._get_user(user_id)
    return jsonify(user[0]) #returns a single dictionary with user_info 



@app.route("/login/<string:username>/<string:email>", methods=["GET"])
def verify_login_api(username,email):
    login_dict = request.get_json()

    answer = db_utils.verify_login( #answer is either {"verify": False}, {"verify": True, "user_id": user_id} or Duplicate users
        username = username,
        emailaddress = email
    )

    return jsonify(answer)

#### used in user_main.py

## route that changes username 
## added old user name so that they can verify its the write person
@app.route('/profile/change/<int:user_id>/<old_user_name>/<new_user_name>')
def change_user_name(user_id,old_user_name, new_user_name):
    result = db_utils.update_user_name(user_id,old_user_name,new_user_name)
    return jsonify(result)   ##return boolean TRUE or FALSE if user details have been updated

@app.route('/profile/change/email/<int:user_id>/<old_user_email>/<new_user_email>')
def change_user_email(user_id, old_user_email, new_user_email):
    result = db_utils.update_user_email(user_id, old_user_email, new_user_email)
    return jsonify(result)

## api endpoint that adds new user by inputing dictionary in form of
# user_dict = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
## user_id is added in the database code so no need to input it
@app.route('/register', methods=['POST'])
def user_acc():
    """
    API endpoint that registers a user into the sql table. Takes in a dictionary, user in formtat:
    user = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
    Returns
    --------
    Either:
    user: dict
        user dictionary for the new user thats been added
    OR:
    answer: str
        string containing message on why the user hasn't been added
    
    """
    user = request.get_json()

    answer = db_utils.add_user(
        user_name=user['User_Name'],
        name_user=user['Name_User'],
        email_address=user['Email_Address']
    )
    if answer == True:
        return user
    else:
        return jsonify(answer)

# deleting a user using the user id
@app.route('/delete/<int:user_id>')

def delete_user_(user_id):
    wish = delete_wishlist(user_id)  ## deletes everything in wishlist too otherwise foregin key restraint
    user = db_utils.delete_user(user_id)
    print(user)
    return jsonify(user)




if __name__ == '__main__':
    app.run(debug=True, port=5001)






