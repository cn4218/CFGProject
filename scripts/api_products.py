## app.py ---  API UI/products SQL DB
from flask import Flask, jsonify, request
from products_data import products
from db_utils_products import search_product, get_productID

app = Flask(__name__)

# GET to retrieve data
# Endpoint to get all the products
@app.route("/products/")
def get_products():
	return jsonify(products)

# GET to retrieve data
# Endpoint to get a product with a specific productID
@app.route("/products/<int:id>")
def get_product_by_id(id):
	product = search_product(productID, products)
	return jsonify(product)

# To get product 555
# http://127.0.0.1:5000/products/555


# POST to add data
@app.route("/products", methods=["POST"])
def add_product():
	product = request.get_json()
	# validate_product(product)  # some sort of data validation to force json keys
	products.append(product)
	return product

# PUT to update data
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
	product_to_update = request.get_json()
	index = get_index(productID, products)
	products[index] = product_to_update
	return jsonify(products[index])

# DELETE to remove data
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
	index = get_index(productID, products)
	deleted = products.pop(index)
	return jsonify(deleted)


if __name__ == '__main__':
	app.run(debug=True)