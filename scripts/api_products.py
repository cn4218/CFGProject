## app.py ---  API UI/products SQL DB
from flask import Flask, jsonify, request
# from products_data import products
from db_utils_products import get_all_products, get_proper_ingredients_list, get_products_containing, get_products_ingt_in_nth_position # search_product, get_productID

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/')
def index():
    return app.send_static_file('index.html')

# GET to retrieve data
# Endpoint to get all the products
@app.route("/products/")
def get_products():
    products = get_all_products()
    return jsonify(products)

# GET to retrieve data
# Endpoint to get a product with a specific ingredient
@app.route("/products/<ingredient>")
def get_product_with_ingredient(ingredient):
    list_products = get_products_containing(ingredient)
    return jsonify(list_products)

# GET to retrieve data
# Endpoint to get a product with a specific ingredient in Nth position
@app.route("/products/<ingredient>/<n>")
def get_product_with_ingredient_nth_position(ingredient,n):
    list_products = get_products_ingt_in_nth_position(ingredient,n)
    return jsonify(list_products)

# ### Received request format:
# dict_ = {
# 	'filter': 'ordered',
# 	'data': {'1': ['water', True],
# 	         '2': ['glycerin ', False],
# 	         '3': ['alcohol', True],
# 	         '4': ['parfum', True],
# 	         '5': ['', True]
# 	         }
# }

# MULTI-CRITERIA ENDPOINT
@app.route("/products/<ing1>/<n1>/<ing2>/<n2>/<ing3>/<n3>>/<ing4>/<n4>/<ing5>/<n5>")  # ??????
def get_product_multi_criteria(_dict):
    list_products = get_proper_ingredients_list(_dict)
    return jsonify(list_products)


# # GET to retrieve data
# # Endpoint to get a product with a specific productID
# @app.route("/products/<productID>")
# def get_product_by_id(productID):
# 	product = search_product(productID, products)
# 	return jsonify(product)


# # POST to add data
# @app.route("/products", methods=["POST"])
# def add_product():
# 	product = request.get_json()
# 	# validate_product(product)  # some sort of data validation to force json keys
# 	products.append(product)
# 	return product
#
# # PUT to update data
# @app.route("/products/<productID>", methods=["PUT"])
# def update_product(productID):
# 	product_to_update = request.get_json()
# 	index = get_index(productID, products)
# 	products[index] = product_to_update
# 	return jsonify(products[index])
#
# # DELETE to remove data
# @app.route("/products/<productID>", methods=["DELETE"])
# def delete_product(productID):
# 	index = get_index(productID, products)
# 	deleted = products.pop(index)
# 	return jsonify(deleted)


if __name__ == '__main__':
    app.run(debug=True)