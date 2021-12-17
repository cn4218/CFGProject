# @app.route('/wishlist/add',methods = ['POST'])  #Ask Georgia how she is going to pass the user Id to me 
# def add_wish_list_func():
#     """
#     This function makes sure the product_id is vald 
#     It then takes the user_id  and product_id data passed via the equest made by the client.
#     It then uses the product ID to search for the corresponding product info in the OBF database 
#     and its returned output (a dictionary) along with the user_id,is fed to the add_wish_list() function
#     that will then add this "new wishlist item" to the wishlist table. It will only add it if it doesn't already exist. 

#     """
#     #check if it is a valid product ID first 
#     # Test tomorrow (Wed)
#     #The keys from line 91 to 110 don't match up (syntax errors) so I now have to debugging them one by one 
#     print("Now trying to add to")
#     user_product_id_dict = request.get_json() # eg  {"user_id": 10234 , "product_id": 78 }
#     print(user_product_id_dict)
#     user_id = user_product_id_dict["user_id"]
#     product_id = user_product_id_dict["product_id"]
#     try:
#         product_id = int(product_id.strip())
    
#     except ValueError:
#         raise Exception("Invalid product_Id")
#         return jsonify("Error")
    
#     except Exception:
#         return jsonify("Error")
#     else: #meaning the product id is valid 
    
#         print("In else block")
#         product = (get_products_by_ids([product_id]))
#         print(product)
#         wishlist_dict = {}
#         wishlist_dict['UserID'] = user_id 
#         wishlist_dict['wishlist'] = product

        # add_wish_list(
        #     ProductID = wishlist_dict['wishlist']['productID'], 
        #     Code_Wish = wishlist_dict['wishlist']['code'], 
        #     Product_name = wishlist_dict['wishlist']['product_name'], 
        #     Ingredients_Text = wishlist_dict['wishlist']['ingredients_list'], 
        #     Quantity = wishlist_dict['wishlist']['quantity'],
        #     Brands = wishlist_dict['wishlist']['brands'], 
        #     Brands_tags = wishlist_dict['wishlist']['brands_tags'], 
        #     Categories = wishlist_dict['wishlist']['categories'], 
        #     Categories_Tags = wishlist_dict['wishlist']['categories_tags'], 
        #     Categories_En = wishlist_dict['wishlist']['categories_en'],
        #     Countries = wishlist_dict['wishlist']['countries'],
        #     Countries_Tags = wishlist_dict['wishlist']['countries_tags'],
        #     Countries_en = wishlist_dict['wishlist']['countries_en'],
        #     Image_url = wishlist_dict['wishlist']['image_url'], 
        #     Image_Small_url = wishlist_dict['wishlist']['image_small_url'], 
        #     Image_Ingredients_url = wishlist_dict['wishlist']['image_ingredients_url'],
        #     Image_Ingredients_Small_url = wishlist_dict['wishlist']['image_ingredients_small_url'], 
        #     Image_Nutrition_url = wishlist_dict['wishlist']['image_nutrition_url'], 
        #     Image_Nutrition_Small_url = wishlist_dict['wishlist']['Iimage_nutrition_small_url'],
        #     UserID = wishlist_dict['UserID']
        

        # )

        # return jsonify("Added") #to let the front end know that you successfully added an item to wishlist 



# @app.route('/wishlist/delete/<int:user_id>/<int:product_id>')
# def delete_wislist_individual(user_id, product_id):
#     """
#     This product uses the user_id and product_id to identify a wishlist item and deletes it from the wishlist table IF EXISTS.
#     """
#     empty_wishlist_item = delete_wishlist_item(user_id,product_id)
#     return jsonify(empty_wishlist_item)





# @app.route('/wishlist/<int:user_id>', methods=['GET'])   
# def get_wishlist(user_id):
#     """This function fetches all the wishlist items corresponding to one
#        particluar user and returns a jsonified list of dictionaries when a 
#        request is made to this endpoint
#     """
#     wishlist = _get_wish_list_all(user_id)
#     return jsonify(wishlist)