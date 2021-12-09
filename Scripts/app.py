from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from obf_db_utils import get_proper_ingredients_list



app = Flask(__name__)
CORS(app) #cross origin resource sharing 
list_ = []

#OBF 
##################################################################################################

@app.route("/")
def serve_home_page():
    return render_template("home.html")



@app.route("/Search", methods=['POST'])  # ??????
def find_products():
    ingredient_input = request.get_json()
    print(ingredient_input)
    
    list_of_products = get_proper_ingredients_list(ingredient_input)
    list_.clear()
    list_.append(list_of_products)
    return jsonify(list_of_products)


@app.route("/Search", methods=['GET']) 
def return_list():
    return jsonify(list_) #returns a list of one element and that element is a list of dictionaries 


#Wishlist 
#################################################################################################
@app.route("/Wishlist/<int:user_id>/<int:user_name>", methods=['GET'])
def send_wishlist(user_id,user_name):
    """This function fetches all the wishlist items corresponding to one
       particluar user and returns a jsonified list of dictionaries when a 
       request is made to this endpoint
    """

@app.route("/Wishlist/<int:user_id>/<int:user_name>/<int:product_id>", method=['PUT'])
def add_product_to_wishlist(user_id,user_name,product_id):
    """This function takes the user_id ,user_name and product_id data passed via the 
        request made by the client. It then uses the product ID to search for the corresponding 
        product info in the OBF database and its returned output (a dictionary) along with the user_id,
        is fed to another function (from db_utils) that will then add this "new wishlist item" to the wishlist table.
        It will only add it if it doesn't already exist. 

    """

@app.route("/Wishlist/<int:user_id>/<int:user_name>/<int:product_id>", method=['DELETE'])
def add_product_to_wishlist(user_id,user_name,product_id):
    """
    This product uses the user_id , user_name and product_id , and deletes it from the wishlist table IF EXISTS.
    """







if __name__ == '__main__':
    app.run(debug=True, port=5001)








#pass the ingredient input into the function that finds the list of product dictionaries 
#then pass that list as a response to the sender of the post (your client)
#since the function in question has issues at the moment, so fix it first 


